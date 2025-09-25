import sqlite3

DB_NAME = "expense_splitter.db"

def get_conn():
    """Create a new database connection with foreign keys enabled"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # rows behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")  # enable FK constraints
    return conn


def init_db():
    """Initialize all tables (users, expenses, expense_shares, settlements)"""
    conn = get_conn()
    cur = conn.cursor()

    # Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Expenses table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            description TEXT,
            paid_by INTEGER NOT NULL,
            FOREIGN KEY (paid_by) REFERENCES users(id)
        )
    """)

    # Expense shares table (who owes how much)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS expense_shares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (expense_id) REFERENCES expenses(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Settlements table (for future feature: repayments)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS settlements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payer_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            FOREIGN KEY (payer_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(" Database initialized with tables: users, expenses, expense_shares, settlements")