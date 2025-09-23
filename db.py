import sqlite3 
DB_NAME = "expense_splitter.db"
def get_conn():
    return sqlite3.connect(DB_NAME) 
def init_db():
    conn = get_conn()
    cur = conn.cursor() 
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )''')   
    conn.commit()
    conn.close()