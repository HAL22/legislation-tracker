import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('legislations.db')

    def query(self, query,params=None):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            cursor.close()

    def get_legislationsByRegion(self, region):
        query = "SELECT * FROM legislation WHERE region = ?"
        return self.query(query, (region,))
        



    