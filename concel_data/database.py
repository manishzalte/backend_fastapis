from psycopg2 import connect
from psycopg2.extras import RealDictCursor

# Connect to an existing database
def connect_to_db():
    try:
        conn = connect(host ='localhost', database= 'fastapis', user='postgres' ,password = '', cursor_factory=RealDictCursor)
        # Open a cursor to perform database operations
        cur = conn.cursor()
        print("db connected successfully \n \n Creating Table ")
        table = create_table()
        res = cur.execute(table)
        print("Created Table")
        return cur,conn
    except Exception as e:
        print("db connection failed : ",e)
        while True:
            conn = connect_to_db()
            if conn:
                break

def create_table():
    return f"""
    CREATE SEQUENCE IF NOT EXISTS posts_id_seq
    START WITH 100000
    INCREMENT BY 1;

    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER NOT NULL DEFAULT nextval('posts_id_seq') PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        content VARCHAR(255) NOT NULL,
        publish boolean NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    """