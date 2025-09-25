from flask import Flask, request, jsonify, render_template
from db import get_conn, init_db
import bcrypt
import sqlite3


app = Flask(__name__)

# Initialize database tables on startup
init_db()
def get_user_id(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name = ?", (username,))
    row = cur.fetchone()
    conn.close()
    return row["id"] if row else None

@app.route("/")
def home():
    return render_template("index.html")

# Serve Signup Page
@app.route('/signup-page')
def signup_page():
    return render_template("signup.html")

# Serve Login Page
@app.route('/login-page')
def login_page():
    return render_template("login.html")

# Serve Dashboard Page
@app.route('/dashboard')
def dashboard_page():
    return render_template("dashboard.html")






#USERS 
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        new_id = cur.lastrowid
        return jsonify({"id": new_id, "name": name, "email": email}), 201
    except Exception as e:
        print("Error in POST /users:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()
@app.route('/users', methods=['GET', 'POST'])
def users():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (data['name'], data['email'], data['password']))
        conn.commit()
        return jsonify({"message": "User added successfully"}), 201

    elif request.method == 'GET':
        cur.execute("SELECT id, name, email FROM users")
        users = [dict(row) for row in cur.fetchall()]
        return jsonify(users)



@app.route('/expenses', methods=['POST'])
def create_expense():
    data = request.get_json() or {}
    amount = data.get('amount')
    description = data.get('description', '')
    paid_by_name = data.get('paid_by')
    participants = data.get('participants', [])

    if not amount or not paid_by_name or not participants:
        return jsonify({"error": "amount, paid_by, and participants are required"}), 400

    try:
        amount = float(amount)
    except:
        return jsonify({"error": "amount must be a number"}), 400

    conn = get_conn()
    cur = conn.cursor()

    # Get payer ID
    cur.execute("SELECT id FROM users WHERE name = ?", (paid_by_name,))
    payer = cur.fetchone()
    if not payer:
        conn.close()
        return jsonify({"error": f"User '{paid_by_name}' not found"}), 404
    paid_by_id = payer['id']

    # Get participant IDs
    participant_ids = []
    for name in participants:
        cur.execute("SELECT id FROM users WHERE name = ?", (name,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return jsonify({"error": f"User '{name}' not found"}), 404
        participant_ids.append(row['id'])

    if not participant_ids:
        conn.close()
        return jsonify({"error": "No valid participants"}), 400

    # Insert into expenses
    cur.execute(
        "INSERT INTO expenses (amount, description, paid_by) VALUES (?, ?, ?)",
        (amount, description, paid_by_id)
    )
    expense_id = cur.lastrowid

    # Split equally among participants
    share = amount / len(participant_ids)
    for uid in participant_ids:
        cur.execute(
            "INSERT INTO expense_shares (expense_id, user_id, amount) VALUES (?, ?, ?)",
            (expense_id, uid, share)
        )

    conn.commit()
    conn.close()

    return jsonify({"message": "Expense added successfully", "expense_id": expense_id}), 201








@app.route('/expenses', methods=['GET'])
def list_expenses():
    conn = get_conn()
    cur = conn.cursor()

    # Get all expenses
    cur.execute("""
        SELECT e.id, e.amount, e.description, u.name AS paid_by
        FROM expenses e
        JOIN users u ON e.paid_by = u.id
    """)
    expenses = cur.fetchall()

    results = []
    for e in expenses:
        # Get participants for each expense
        cur.execute("""
            SELECT u.name, es.amount
            FROM expense_shares es
            JOIN users u ON es.user_id = u.id
            WHERE es.expense_id = ?
        """, (e["id"],))
        participants = cur.fetchall()

        results.append({
            "id": e["id"],
            "amount": e["amount"],
            "description": e["description"],
            "paid_by": e["paid_by"],
            "participants": [
                {"user": p["name"], "share": p["amount"]} for p in participants
            ]
        })

    conn.close()
    return jsonify(results), 200




#EXPENSE SHARES
@app.route('/expense_shares', methods=['GET'])
def list_expense_shares():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT es.id, e.id AS expense_id, u.name AS user, es.amount
        FROM expense_shares es
        JOIN expenses e ON es.expense_id = e.id
        JOIN users u ON es.user_id = u.id
    """)
    rows = cur.fetchall()
    conn.close()

    shares = []
    for r in rows:
        shares.append({
            "id": r["id"],
            "expense_id": r["expense_id"],
            "user": r["user"],
            "amount": r["amount"]
        })

    return jsonify(shares), 200


      
#  BALANCES 
@app.route('/balances', methods=['GET'])
def balances():
    conn = get_conn()
    cur = conn.cursor()

    # 1. Get all users
    cur.execute("SELECT id, name FROM users")
    users = {row["id"]: row["name"] for row in cur.fetchall()}

    # 2. Track net balances
    net = {uid: 0 for uid in users}

    # 3. Add expenses (payer gets positive balance)
    cur.execute("SELECT id, amount, paid_by FROM expenses")
    expenses = cur.fetchall()
    for e in expenses:
        net[e["paid_by"]] += e["amount"]

        # subtract each participant's share
        cur.execute("SELECT user_id, amount FROM expense_shares WHERE expense_id = ?", (e["id"],))
        for s in cur.fetchall():
            net[s["user_id"]] -= s["amount"]

    conn.close()

    # 4. Build human-readable debts
    results = []
    creditors = {uid: bal for uid, bal in net.items() if bal > 0}
    debtors = {uid: -bal for uid, bal in net.items() if bal < 0}

    for debtor_id, debt in debtors.items():
        for creditor_id, credit in list(creditors.items()):
            if debt == 0:
                break
            pay = min(debt, credit)
            results.append(f"{users[debtor_id]} owes {users[creditor_id]} {pay}")
            debt -= pay
            creditors[creditor_id] -= pay
            if creditors[creditor_id] == 0:
                del creditors[creditor_id]

    return jsonify(results), 200

@app.route('/settlements', methods=['GET'])
def list_settlements():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.id, u1.name AS payer, u2.name AS receiver, s.amount
        FROM settlements s
        JOIN users u1 ON s.payer_id = u1.id
        JOIN users u2 ON s.receiver_id = u2.id
    """)
    rows = cur.fetchall()
    conn.close()

    settlements = []
    for r in rows:
        settlements.append({
            "id": r["id"],
            "payer": r["payer"],
            "receiver": r["receiver"],
            "amount": r["amount"]
        })

    return jsonify(settlements), 200

@app.route('/settlements', methods=['POST'])
def create_settlement():
    data = request.get_json() or {}
    from_name = data.get('from') or data.get('payer')   # accept "from" or "payer"
    to_name = data.get('to') or data.get('receiver')    # accept "to" or "receiver"
    amount = data.get('amount')

    if not from_name or not to_name or amount is None:
        return jsonify({"error": "from, to and amount are required"}), 400

    try:
        amount = float(amount)
    except:
        return jsonify({"error": "invalid amount"}), 400

    conn = get_conn()
    cur = conn.cursor()

    # Look up user IDs
    cur.execute("SELECT id FROM users WHERE name = ?", (from_name,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return jsonify({"error": f"User '{from_name}' not found"}), 404
    payer_id = r['id']

    cur.execute("SELECT id FROM users WHERE name = ?", (to_name,))
    r = cur.fetchone()
    if not r:
        conn.close()
        return jsonify({"error": f"User '{to_name}' not found"}), 404
    receiver_id = r['id']

    # Insert settlement record (payer paid receiver amount)
    cur.execute(
        "INSERT INTO settlements (payer_id, receiver_id, amount) VALUES (?, ?, ?)",
        (payer_id, receiver_id, amount)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": f"{from_name} paid {to_name} {amount}"}), 201

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])


def delete_expense(expense_id):
    try:
        conn = get_conn()
        cur = conn.cursor()

        # First delete related shares
        cur.execute("DELETE FROM expense_shares WHERE expense_id=?", (expense_id,))

        # Then delete the expense itself
        cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()

        if cur.rowcount == 0:
            return jsonify({"error": "Expense not found"}), 404

        return jsonify({"message": f"Expense {expense_id} deleted successfully"}), 200

    except Exception as e:
        print("Error in DELETE /expenses:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()

# Delete a user by username
@app.route('/users/<string:username>', methods=['DELETE'])
def delete_user(username):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE name = ?", (username,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"User '{username}' deleted"}), 200









# Users (Register new user) - REST + Signup alias


@app.route('/signup', methods=['POST'])
def signup():
    conn = get_conn()
    cur = conn.cursor()

    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']

    # Hash password before saving
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                    (name, email, hashed_pw.decode('utf-8')))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()
# ================== LOGIN ==================
# Login (authenticate user)
@app.route('/login', methods=['POST'])
def login():
    conn = get_conn()
    cur = conn.cursor()

    data = request.get_json()
    cur.execute("SELECT * FROM users WHERE email = ?", (data['email'],))
    user = cur.fetchone()
    conn.close()

    if user:
        stored_password = user['password']

        # Ensure password is in bytes
        if isinstance(stored_password, str):
            stored_password = stored_password.encode('utf-8')

        # Check hashed password
        if bcrypt.checkpw(data['password'].encode('utf-8'), stored_password):
            return jsonify({
                "message": "Login successful",
                "user": {"id": user["id"], "name": user["name"], "email": user["email"]}
            }), 200

    return jsonify({"error": "Invalid email or password"}), 401

if __name__ == '__main__':
    app.run(debug=True)
@app.route("/")
def home():
    return "<h1>Welcome to Expense Splitter</h1><p>Go to <a href='/signup-page'>Signup</a> or <a href='/login-page'>Login</a></p>"
