import psycopg2
import os

class My_db:
    def __init__(self):
        self.conn = self.get_db_connection()
        self.cur = self.conn.cursor()
    def get_db_connection(self):
        conn = psycopg2.connect(host='localhost',
                                database='bank_db',
                                user=os.environ['DB_USERNAME'],
                                password=os.environ['DB_PASSWORD'])
        return conn
    def commit(self):
        self.conn.commit()
    def close_conn(self):
        self.cur.close()
        self.conn.close()