import app as lol
import pytest

@pytest.fixture()
def app():
    app = lol.app
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_request_example(client):
    response = client.get("/get_accounts")
    assert response.status_code == 200

def test_deposit(client):
    errors = []
    my_db = lol.My_db()
    my_db.get_db_connection()
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("500500",))
    prev_amount = my_db.cur.fetchall()
    response = client.put("/deposit", data={
        "account_id":"500500",
        "deposit":"42",
    })
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("500500",))
    new_amount = my_db.cur.fetchall()
    if response.status_code != 200:
        errors.append("Wrong status code.")
    if prev_amount[0][0] != new_amount[0][0]-42:
        errors.append("Wrong new amount.")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_wrong_deposit(client):
    response = client.put("/deposit", data={
        "account_id":"wrong",
        "deposit":"42",
    })
    assert response.status_code == 422

def test_missing_request_deposit(client):
    response = client.put("/deposit", data={
        "account_id":"500500",
    })
    assert response.status_code == 400


def test_withdraw(client):
    errors = []
    my_db = lol.My_db()
    my_db.get_db_connection()
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("500500",))
    prev_amount = my_db.cur.fetchall()
    response = client.put("/withdraw", data={
        "account_id":"500500",
        "withdraw":"42",
    })
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("500500",))
    new_amount = my_db.cur.fetchall()
    if response.status_code != 200:
        errors.append("Wrong status code.")
    if prev_amount[0][0] != new_amount[0][0]+42:
        errors.append("Wrong new amount.")
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_wrong_withdraw(client):
    response = client.put("/withdraw", data={
        "account_id":"wrong",
        "withdraw":"42",
    })
    assert response.status_code == 422

def test_missing_request_withdraw(client):
    response = client.put("/withdraw", data={
        "account_id":"500500",
    })
    assert response.status_code == 400


def test_transfer(client):
    errors = []
    my_db = lol.My_db()
    my_db.get_db_connection()
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("500500",))
    prev_amount = my_db.cur.fetchall()
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("309309",))
    target_prev_amount = my_db.cur.fetchall()
    print(prev_amount[0][0], target_prev_amount[0][0])
    response = client.put("/transfer", data={
        "account_id":"500500",
        "amount":"42",
        "target_account_id":"309309"
    })
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("500500",))
    new_amount = my_db.cur.fetchall()
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("309309",))
    target_new_amount = my_db.cur.fetchall()
    if response.status_code != 200:
        errors.append("Wrong status code.")
    if prev_amount[0][0] != new_amount[0][0]+42:
        errors.append("Wrong new amount.")
    if target_prev_amount[0][0] != target_new_amount[0][0]-42:
        errors.append("Wrong target new amount.")
    print("response:", new_amount[0][0], target_new_amount[0][0])
    assert not errors, "errors occured:\n{}".format("\n".join(errors))

def test_wrong_transfer(client):
    response = client.put("/transfer", data={
        "account_id":"wrong",
        "amount":"42",
        "target_account_id":"309309"
    })
    assert response.status_code == 422

def test_missing_request_transfer(client):
    response = client.put("/transfer", data={
        "account_id":"500500",
    })
    assert response.status_code == 400

def test_get_accounts_by_name(client):
    response = client.get("/get_accounts_by_name", data={
        "name": "Arisha Barron"
    })
    assert response.status_code == 200

def test_get_accounts_by_name_wrong(client):
    response = client.get("/get_accounts_by_name", data={
        "name": "wrong"
    })
    assert response.status_code == 422

def test_get_accounts_by_name_missing(client):
    response = client.get("/get_accounts_by_name", data={
        "wrong": "Arisha Barron"
    })
    assert response.status_code == 400

def test_get_amount(client):
    response = client.get("/get_amount", data={
        "account_id":"309309"
    })
    assert response.status_code == 200


def test_get_amount_wrong(client):
    response = client.get("/get_amount", data={
        "account_id":"wrong"
    })
    assert response.status_code == 422

def test_get_amount_missing(client):
    response = client.get("/get_amount", data={
        "wrong":"309309"
    })
    assert response.status_code == 400

def test_get_history(client):
    response = client.get("/get_history", data={
        "account_id":"309309"
    })
    assert response.status_code == 200

def test_get_history_missing(client):
    response = client.get("/get_history", data={
        "wrong":"309309"
    })
    assert response.status_code == 400

def test_get_history_wrong(client):
    response = client.get("/get_history", data={
        "account_id":"wrong"
    })
    assert response.status_code == 422


def test_create_account(client):
    my_db = lol.My_db()
    my_db.get_db_connection()
    response = client.post("/create_account", data={
        "account_id":"1",
        "name":"new_account",
        "amount":"300"
    })
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("1",))
    amount = my_db.cur.fetchall()
    assert response.status_code ==  200 and amount

def test_create_account_missing(client):
    response = client.post("/create_account", data={
        
        "wrong":"309309",
        "name":"new_account",
        "amount":"300"
    })
    assert response.status_code == 400

def test_create_account_wrong(client):
    response = client.post("/create_account", data={
        "account_id":"wrong",
        "name":"new_account",
        "amount":"300"
    })
    assert response.status_code == 422



def test_delete_account(client):
    my_db = lol.My_db()
    response = client.delete("/delete_account", data={
        "account_id":"1"
    })
    my_db.cur.execute('SELECT amount FROM accounts WHERE account_id = %s',
                        ("1",))
    amount = my_db.cur.fetchall()
    assert response.status_code ==  200 and not amount

def test_delete_account_missing(client):
    response = client.delete("/delete_account", data={
        "wrong":"309309"
    })
    assert response.status_code == 400

def test_delete_account_wrong(client):
    response = client.delete("/delete_account", data={
        "account_id":"wrong"
    })
    assert response.status_code == 422
