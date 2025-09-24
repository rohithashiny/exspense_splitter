import sqlite3

DB_NAME = "expense_splitter.db"

def show_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()


    # ---------------- SHOW TABLES ----------------
    print("\n Tables in DB:")
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())

    # ---------------- SCHEMA INFO ----------------
    print("\n Schema of users table:")
    cur.execute("PRAGMA table_info(users);")
    print(cur.fetchall())

    print("\n Schema of expenses table:")
    cur.execute("PRAGMA table_info(expenses);")
    print(cur.fetchall())

    print("\n Schema of expense_shares table:")
    cur.execute("PRAGMA table_info(expense_shares);")
    print(cur.fetchall())

    # ---------------- DATA CONTENT ----------------
    print("\n Users:")
    cur.execute("SELECT * FROM users;")
    print(cur.fetchall())

    print("\n Expenses:")
    cur.execute("SELECT * FROM expenses;")
    print(cur.fetchall())

    print("\n Expense Shares:")
    cur.execute("SELECT * FROM expense_shares;")
    print(cur.fetchall())

    cur.execute("DELETE FROM expense_shares;")
    print("\n Deleted all rows from expense_shares")

    cur.execute("DELETE FROM expenses;")
    print("\n Deleted all rows from expenses")
    conn.commit

    conn.close()


if __name__ == "__main__":
    show_db()