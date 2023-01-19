from ctypes import util
import os
from threading import activeCount
import psycopg2
from flask import Flask, render_template, request, url_for, redirect
from flask import jsonify
import utils
from my_db import My_db

app = Flask(__name__)

"""
BANK API ROUTE
"""

"""
 @apiDefine IdNotFoundError
  @apiError IdNotFound The id of the Account was not found.
  @apiErrorExample Error-Response:
     HTTP/1.1 422
     {
       'Unable to process the contained instructions. Request entities may be wrong.'
     }
"""
"""
 @apiDefine MissingRequestEntityError
  @apiError MissingRequestEntity Wrong request entity.
  @apiErrorExample Error-Response:
     HTTP/1.1 400
     {
       'Missing request entity, check documentation.'
     }
"""

"""
 @api {get} '/get_accounts' Get all account in Data Base.
 @apiName GetAccount
 @apiGroup Account

 @apiSuccess {String} name Name of the User.
 @apiSuccess {Number} amount  Money on the account.
 @apiSuccess {Number} account_id  Id of the account.
 @apiSuccess {Date} date_added  Date of the account creation.

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
    { 
        {
            1,
            "John Doe",
            "500",
            "676763",
            "Wed, 06 Apr 2022 00:00:00 GMT"
        },
        {
            2,
            "Branden Gibson",
            30,
            309309,
            "Wed, 06 Apr 2022 00:00:00 GMT"
        }
    }

 @apiError DataNotSet The DataBase has not been found.

 @apiErrorExample Error-Response:
     HTTP/1.1 404 Not Found
     {
       "error": "Database not set up!"
     }
"""


@app.route('/get_accounts')
def get_accounts():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        my_db.cur.execute('SELECT * FROM accounts;')
    except:
        return 'Database not set up!', 404
    accounts = my_db.cur.fetchall()
    my_db.close_conn()
    return jsonify(accounts), 200


"""
 @api {put} /deposit Deposit money on an account.
 @apiName Deposit
 @apiGroup Action

 @apiBody {Number} account_id Account unique ID.
 @apiBody {Number} deposit Amount of money for deposit.

 @apiSuccess {String} request_comment Comment about the deposit.

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "request_comment": "deposit done"
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/deposit', methods=['PUT'])
def deposit():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        account_id = request.form['account_id']
        deposit = request.form['deposit']
    except:
        return 'Missing request entity, check documentation.', 400
    try:
        my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                          (account_id,))
        prev_amount = my_db.cur.fetchall()
        utils.deposit_utils(prev_amount[0][0], deposit, account_id, my_db.cur)
        utils.write_history(my_db, account_id, 'Deposit : '+str(deposit))
    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.commit()
    my_db.close_conn()
    return {'request_comment': 'deposit done'}, 200


"""
 @api {put} /tranfert Tranfert money from an account to another.
 @apiName Transfer
 @apiGroup Action

 @apiBody {Number} account_id Account unique ID.
 @apiBody {Number} target_account_id Target account unique ID.
 @apiBody {Number} amount Amount of money for transfer.

 @apiSuccess {String} request_comment Comment about the tranfert

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "request_comment": "tranfert done"
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/transfer', methods=['PUT'])
def transfer():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        account_id = request.form['account_id']
        target_account_id = request.form['target_account_id']
        amount = request.form['amount']
    except:
        return 'Missing request entity, check documentation.', 400
    try:
        my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                          (account_id,))
        account_prev_amount = my_db.cur.fetchall()
        utils.withdraw_utils(
            account_prev_amount[0][0], amount, account_id, my_db.cur)
        my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                          (target_account_id,))
        target_prev_amount = my_db.cur.fetchall()
        utils.deposit_utils(
            target_prev_amount[0][0], amount, target_account_id, my_db.cur)
        utils.write_history(my_db, account_id, 'Tranfert to : ' +
                            str(target_account_id) + "account of " + str(amount))
        utils.write_history(my_db, target_account_id, 'Transfer from : ' +
                            str(account_id) + " account of " + str(amount))
    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.commit()
    my_db.close_conn()
    return {'request_comment': 'transfer done'}, 200


"""
 @api {put} /withdraw Withdraw money from an account.
 @apiName Withdraw
 @apiGroup Action

 @apiBody {Number} account_id Account unique ID.
 @apiBody {Number} withdraw Amount of money for withdraw.

 @apiSuccess {String} request_comment Comment about the tranfert

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "request_comment": "withdraw done"
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/withdraw', methods=['PUT'])
def withdraw():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        account_id = request.form['account_id']
        withdraw = request.form['withdraw']
    except:
        return 'Missing request entity, check documentation.', 400
    try:
        my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                          (account_id,))
        prev_amount = my_db.cur.fetchall()
        print(prev_amount)
        print(prev_amount[0][0])
        utils.withdraw_utils(
            prev_amount[0][0], withdraw, account_id, my_db.cur)
        utils.write_history(my_db, account_id,  'Withdraw : '+str(withdraw))

    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.commit()
    my_db.close_conn()
    return {'request_comment': 'withdraw done'}, 200


"""
 @api {post} /create_account Create a new account in the Data Base.
 @apiName CreateAccount
 @apiGroup Account

 @apiBody {String} name Name of the account owner. May not be unique.
 @apiBody {Number} account_id Account unique ID.
 @apiBody {Number} amount Initial deposit.

 @apiSuccess {String} request_comment Comment about the tranfert

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "request_comment": "account created"
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/create_account', methods=['POST'])
def create_account():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        name = request.form['name']
        amount = request.form['amount']
        account_id = request.form['account_id']
    except:
        return 'Missing request entity, check documentation.', 400
    print(name, amount, account_id)
    try:
        my_db.cur.execute('INSERT INTO accounts (name, amount, account_id)'
                          'VALUES (%s, %s, %s)',
                          (name, amount, account_id))

        utils.write_history(my_db, account_id,  'Initial deposit : ' + amount)
    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.commit()
    my_db.close_conn()
    return {'request_comment': 'Account created'}, 200


"""
 @api {delete} /delete_account Delete an account in the Data Base.
 @apiName DeleteAccount
 @apiGroup Account

 @apiBody {Number} account_id Account unique ID.

 @apiSuccess {String} request_comment Comment about the tranfert

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "request_comment": "account deleted"
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        account_id = request.form['account_id']
    except:
        return 'Missing request entity, check documentation.', 400
    try:
        my_db.cur.execute('SELECT * FROM accounts WHERE account_id = %s',
                          (account_id,))
        if not my_db.cur.fetchall():
            return 'Unable to process the contained instructions. Request entities may be wrong.', 422
        my_db.cur.execute('DELETE FROM accounts WHERE account_id = %s',
                          (account_id,))
        utils.write_history(my_db, account_id,  'Account deleted.')
    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.commit()
    my_db.close_conn()
    return({'request comment': 'account deleted'}, 200)


"""
 @api {get} /get_history Get the history of an account.
 @apiName GetHistory
 @apiGroup History

 @apiBody {Number} account_id Account unique ID.

 @apiSuccess {String} history The history of the different action done on the account.

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
        {
            "Initial deposit : 50"
        },
        {
            "Withdraw : 100"
        },
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/get_history')
def get_history():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        account_id = request.form['account_id']
    except:
        return 'Missing request entity, check documentation.', 400
    try:
        my_db.cur.execute('SELECT history FROM history WHERE account_id = %s',
                          (account_id,))
        history = my_db.cur.fetchall()
        if not history:
            return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.close_conn()
    return jsonify(history), 200


"""
 @api {get} /get_amount Get the amount of money on an account.
 @apiName GetAmount
 @apiGroup Account

 @apiBody {Number} account_id Account unique ID.

 @apiSuccess {String} request_comment Comment about the tranfert

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "amount": "678"
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/get_amount')
def get_amount():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        account_id = request.form['account_id']
    except:
        return 'Missing request entity, check documentation.', 400
    try:
        my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                          (account_id,))
        amount = my_db.cur.fetchall()
        if not amount:
            return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.close_conn()
    return jsonify(amount[0]), 200


"""
 @api {get} /get_accounts_by_name Get all the accounts for a given name.
 @apiName GetAccountsByName
 @apiGroup Account

 @apiBody {String} name Name of the account owner. May not be unique.

 @apiSuccess {String} request_comment Comment about the tranfert

 @apiSuccessExample Success-Response:
     HTTP/1.1 200 OK
     {
       "request_comment": "account created"
     }

 @apiUse IdNotFoundError
 @apiUse MissingRequestEntityError
"""


@app.route('/get_accounts_by_name')
def get_accounts_by_name():
    my_db = My_db()
    my_db.get_db_connection()
    try:
        name = request.form['name']
    except:
        return 'Missing request entity, check documentation.', 400
    try:
        my_db.cur.execute('SELECT * FROM accounts WHERE name = %s',
                          (name,))
        amount = my_db.cur.fetchall()
        if not amount:
            return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    except:
        return 'Unable to process the contained instructions. Request entities may be wrong.', 422
    my_db.close_conn()
    return jsonify(amount), 200
