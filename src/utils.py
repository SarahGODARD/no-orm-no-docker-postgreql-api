def deposit_utils(prev_amount, deposit, account_id, cur):
    amount = prev_amount+int(deposit)
    cur.execute('UPDATE accounts SET amount = %s WHERE account_id = %s',
                (amount, account_id))


def withdraw_utils(prev_amount, withdraw, account_id, cur):
    amount = prev_amount-int(withdraw)
    cur.execute('UPDATE accounts SET amount = %s WHERE account_id = %s',
                (amount, account_id))

def write_history(my_db, account_id, msg):
    my_db.cur.execute('INSERT INTO history (account_id, history)'
                'VALUES (%s, %s)',
                (account_id,
                msg))