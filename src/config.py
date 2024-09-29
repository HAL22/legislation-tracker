import sqlite3
import constants
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import pinecone
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain_openai import OpenAIEmbeddings
import os
import os
from pinecone import Pinecone, ServerlessSpec

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

def drop_sqlite_table(conn, table_name):
    """ drop a table from the database """
    try:
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {table_name}")
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

def create_sql_config():
    print("Creating SQLite database...")
    create_sqlite_database("legislations.db")

    conn = sqlite3.connect("legislations.db")

    #drop_sqlite_table(conn, "legislation")

    create_sqlite_table(conn, create_legislation_sql())

    for legislation in constants.get_legislations():
        insert_legislation(conn, legislation)

    conn.close()
    print("SQLite database created and populated.")
### Vector Database

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(
        text,
        disallowed_special=()
    )
    return len(tokens)

def split_text_into_chunks(text, chunk_size=500):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=20,  # number of tokens overlap between chunks
    length_function=tiktoken_len,
    separators=['\n\n', '\n', ' ', '']
    )

    text_chunks = text_splitter.split_text(text)

    docs = [Document(page_content=t) for t in text_chunks]

    return docs

def create_pinecone_index(index_name,text,embeddings):
    pc = Pinecone(
        api_key=os.environ.get("PINECONE_API_KEY")
    )

    if index_name not in pc.list_indexes().names():
      

        pc.create_index(
            name=index_name,
            dimension=1536, 
            metric='euclidean',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )

        docs = split_text_into_chunks(text)

        PineconeStore.from_documents(docs, embeddings, index_name=index_name)

def create_indexs():
    print("Creating Pinecone indexes...")
    embeddings=OpenAIEmbeddings(model="text-embedding-ada-002")

    for legislation in constants.get_legislations():
        create_pinecone_index(legislation.index_pn,legislation.description,embeddings)

    print("Pinecone indexes created.")


if __name__ == "__main__":
    create_sql_config()
    create_indexs()
 
 
 
 
 









