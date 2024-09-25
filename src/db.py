import sqlite3
import constants

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('legislations.db')
        """
        db_path = '/data/database.sqlite'
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        """
        self.cursor = self.conn.cursor()

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
    
    def create_sqlite_table(c, create_table_sql):
        """ create a table from the create_table_sql statement if it doesn't exist """
        try:
            # Modify the SQL to include 'IF NOT EXISTS'
            if 'IF NOT EXISTS' not in create_table_sql.upper():
                create_table_sql = create_table_sql.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS', 1)
            c.execute(create_table_sql)
        except sqlite3.Error as e:
            print(e)
    
    def create_legislation_sql():
        sql_create_legislation_table = """
        CREATE TABLE IF NOT EXISTS legislation (
            id integer PRIMARY KEY AUTOINCREMENT,
            title text NOT NULL,
            description text NOT NULL,
            summary text,
            region text NOT NULL,
            status text NOT NULL,
            type text NOT NULL,
            index_pn text NOT NULL,
            date text NOT NULL,
            link text NOT NULL
        );
        """
        return sql_create_legislation_table
    
    def insert_legislation(conn, legislation):
        """
        Insert a new legislation into the legislation table
        :param conn:
        :param legislation:
        """
        sql = ''' INSERT INTO legislation(title, description, summary, region, status, type, index_pn, date, link)
              VALUES(?,?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, legislation.to_tuple())
        conn.commit()

    def drop_sqlite_table(c, table_name):
        """ drop a table from the database """
        try:
            c.execute(f"DROP TABLE IF EXISTS {table_name}")
        except sqlite3.Error as e:
            print(e)

    def initialize_database(self):
        self.drop_sqlite_table(self.cursor,"legislation")
        self.create_sqlite_table(self.cursor,self.create_legislation_sql)

        for legislation in constants.get_legislations():
            self.insert_legislation(self.conn, legislation)

        



    