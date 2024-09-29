import sqlite3
import constants

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('legislations.db')
        db_path = '/data/database.sqlite'
        self.conn = sqlite3.connect(db_path)
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
    
    def create_sqlite_table(self, create_table_sql):
        """ create a table from the create_table_sql statement if it doesn't exist """
        try:
            # Modify the SQL to include 'IF NOT EXISTS'
            if 'IF NOT EXISTS' not in create_table_sql.upper():
                create_table_sql = create_table_sql.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS', 1)
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            print(e)
    
    @staticmethod
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
    
    def insert_legislation(self, legislation):
        """
        Insert a new legislation into the legislation table
        :param legislation: Legislation object to insert
        """
        sql = ''' INSERT INTO legislation(title, description, summary, region, status, type, index_pn, date, link)
              VALUES(?,?,?,?,?,?,?,?,?) '''
        try:
            self.cursor.execute(sql, legislation.to_tuple())
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error inserting legislation: {e}")

    def drop_sqlite_table(self, table_name):
        """ drop a table from the database """
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error dropping table {table_name}: {e}")

    def initialize_database(self):
        self.drop_sqlite_table("legislation")
        self.create_sqlite_table(self.create_legislation_sql())

        for legislation in constants.get_legislations():
            self.insert_legislation(legislation)




