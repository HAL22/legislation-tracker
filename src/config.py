import sqlite3

def create_sqlite_database(filename):
    """ create a database connection to an SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print(sqlite3.sqlite_version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def create_sqlite_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement if it doesn't exist """
    try:
        c = conn.cursor()
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
        index text NOT NULL,
        date text NOT NULL
    );
    """
    return sql_create_legislation_table

def get_text_from_file(filename):
    with open(filename, 'r') as file:
        text = file.read()
    return text

def insert_legislation(conn, legislation):
    """
    Insert a new legislation into the legislation table
    :param conn:
    :param legislation:
    """
    sql = ''' INSERT INTO legislation(title, description, summary, region, status, type, index, date)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, legislation.to_tuple())
    conn.commit()

