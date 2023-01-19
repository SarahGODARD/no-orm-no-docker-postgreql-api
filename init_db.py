import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="bank_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS accounts;')
cur.execute('DROP TABLE IF EXISTS history;')
cur.execute('CREATE TABLE accounts (id serial PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'amount integer NOT NULL,'
                                 'account_id integer NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('CREATE TABLE history (history varchar (150) NOT NULL,'
                                'account_id integer NOT NULL);')

cur.execute('INSERT INTO accounts (name, amount, account_id)'
            'VALUES (%s, %s, %s)',
            ('Arisha Barron',
             600,
             123123)
            )

cur.execute('INSERT INTO history (history, account_id)'
                'VALUES (%s, %s)',
                ('Initial deposit : 600',
                123123))

cur.execute('INSERT INTO accounts (name, amount, account_id)'
            'VALUES (%s, %s, %s)',
            ('Branden Gibson',
             30,
             309309)
            )

cur.execute('INSERT INTO history (history, account_id)'
                'VALUES (%s, %s)',
                ('Initial deposit : 30',
                309309))

cur.execute('INSERT INTO accounts (name, amount, account_id)'
            'VALUES (%s, %s, %s)',
            ('Rhonda Church',
             300,
             100100)
            )

cur.execute('INSERT INTO history (history, account_id)'
                'VALUES (%s, %s)',
                ('Initial deposit : 300',
                100100))

cur.execute('INSERT INTO accounts (name, amount, account_id)'
            'VALUES (%s, %s, %s)',
            ('Georgina Hazel',
             50,
             500500)
            )

cur.execute('INSERT INTO history (history, account_id)'
                'VALUES (%s, %s)',
                ('Initial deposit : 50',
                500500))

cur.execute('SELECT * FROM accounts')

conn.commit()
cur.close()
conn.close()