from flask import Flask, request, jsonify
from db import get_conn, init_db

app = Flask(__name__)

# Initialize database tables on startup
init_db()

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

@app.route('/users', methods=['GET'])
def list_users():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, email FROM users")
        rows = cur.fetchall()
        users = [{"id": row[0], "name": row[1], "email": row[2]} for row in rows]
        return jsonify(users), 200
    except Exception as e:
        print("Error in GET /users:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()

#EXPENSES 
@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.get_json()
    user_id = data.get("user_id")   # who paid
    amount = data.get("amount")
    description = data.get("description")

    if not user_id or not amount:
        return jsonify({"error": "user_id and amount are required"}), 400

    try:
        conn = get_conn()
        cur = conn.cursor()

        # 1. Insert expense into expenses table
        cur.execute(
            "INSERT INTO expenses (user_id, amount, description) VALUES (?, ?, ?)",
            (user_id, amount, description)
        )
        expense_id = cur.lastrowid

        # 2. Get all users
        cur.execute("SELECT id FROM users")
        users = cur.fetchall()

        if not users:
            return jsonify({"error": "No users found"}), 400

        # 3. Split amount equally among users
        share = round(amount / len(users), 2)

        # 4. Insert shares automatically
        for u in users:
            cur.execute(
                "INSERT INTO expense_shares (expense_id, user_id, amount) VALUES (?, ?, ?)",
                (expense_id, u[0], share)
            )

        conn.commit()

        return jsonify({
            "expense_id": expense_id,
            "paid_by": user_id,
            "amount": amount,
            "description": description,
            "auto_split": f"{len(users)} users, each owes {share}"
        }), 201

    except Exception as e:
        print("Error in POST /expenses:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()
@app.route('/expenses', methods=['GET'])
def list_expenses():
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, amount, description FROM expenses")
        rows = cur.fetchall()
        expenses = [{"id": row[0], "user_id": row[1], "amount": row[2], "description": row[3]} for row in rows]
        return jsonify(expenses), 200
    except Exception as e:
        print("Error in GET /expenses:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()

#EXPENSE SHARES
@app.route('/expense_shares', methods=['POST'])
def add_expense_share():
    data = request.get_json()
    expense_id = data.get("expense_id")
    user_id = data.get("user_id")
    amount = data.get("amount")

    if not expense_id or not user_id or not amount:
        return jsonify({"error": "expense_id, user_id, and amount are required"}), 400

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO expense_shares (expense_id, user_id, amount) VALUES (?, ?, ?)",
            (expense_id, user_id, amount),
        )
        conn.commit()
        new_id = cur.lastrowid
        return jsonify({
            "id": new_id,
            "expense_id": expense_id,
            "user_id": user_id,
            "amount": amount
        }), 201
    except Exception as e:
        print("Error in POST /expense_shares:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()
        

@app.route('/expense_shares', methods=['GET'])
def list_expense_shares():
    try:
        conn = get_conn()
        cur = conn.cursor()
        # Join expense_shares with users table to get the user name
        cur.execute("""
            SELECT es.id, es.expense_id, es.user_id, u.name, es.amount
            FROM expense_shares es
            JOIN users u ON es.user_id = u.id
        """)
        rows = cur.fetchall()

        shares = []
        for row in rows:
            shares.append({
                "id": row[0],
                "expense_id": row[1],
                "user_id": row[2],
                "user_name": row[3],   # New field
                "amount": row[4]
            })

        return jsonify(shares), 200
    except Exception as e:
        print("Error in GET /expense_shares:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()
#  BALANCES 
@app.route('/balances', methods=['GET'])
def list_balances():
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Get all users
        cur.execute("SELECT id, name FROM users")
        users = cur.fetchall()

        balances = {}
        for user in users:
            user_id, name = user

            # Calculate how much this user paid in expenses
            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id=?", (user_id,))
            paid = cur.fetchone()[0]

            # Calculate how much this user owes (their shares)
            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expense_shares WHERE user_id=?", (user_id,))
            owed = cur.fetchone()[0]

            balances[name] = paid - owed  # use name instead of user_id

        return jsonify(balances), 200

    except Exception as e:
        print("Error in GET /balances:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()


@app.route('/balances', methods=['POST'])
def post_balances():
    # POST behaves the same as GET here
    return list_balances()

@app.route('/settlements', methods=['GET'])
def settlements():
    try:
        conn = get_conn()
        cur = conn.cursor()

        # Get balances with names
        cur.execute("SELECT id, name FROM users")
        users = cur.fetchall()

        balances = []
        for user_id, name in users:
            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE user_id=?", (user_id,))
            paid = cur.fetchone()[0]

            cur.execute("SELECT COALESCE(SUM(amount), 0) FROM expense_shares WHERE user_id=?", (user_id,))
            owed = cur.fetchone()[0]

            balances.append({"name": name, "balance": paid - owed})

        # Split into payers (negatives) and receivers (positives)
        payers = [b for b in balances if b["balance"] < 0]
        receivers = [b for b in balances if b["balance"] > 0]

        settlements = []
        i, j = 0, 0

        # Match payers to receivers
        while i < len(payers) and j < len(receivers):
            payer = payers[i]
            receiver = receivers[j]

            amount = min(-payer["balance"], receiver["balance"])

            settlements.append(f"{payer['name']} owes {receiver['name']} ₹{amount:.2f}")

            payer["balance"] += amount
            receiver["balance"] -= amount

            if payer["balance"] == 0:
                i += 1
            if receiver["balance"] == 0:
                j += 1

        return jsonify(settlements), 200

    except Exception as e:
        print("Error in GET /settlements:", e)
        return jsonify({"error": "Internal server error"}), 500
    finally:
        conn.close()
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

# Users (Register new user) - REST + Signup alias
@app.route('/users', methods=['GET', 'POST'])
@app.route('/signup', methods=['POST'])  # alias for POST only
def users():
    conn = get_conn()
    cur = conn.cursor()

    if request.method == 'POST':
        data = request.get_json()

        # Insert with password now
        cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                    (data['name'], data['email'], data['password']))
        conn.commit()

        return jsonify({"message": "User registered successfully"}), 201

    else:  # GET -> list all users
        cur.execute("SELECT id, name, email FROM users")  # hide password
        users = [dict(row) for row in cur.fetchall()]
        return jsonify(users)
# ================== LOGIN ==================
@app.route('/login', methods=['POST'])
def login():
    conn = get_conn()
    cur = conn.cursor()




    data = request.get_json()

    cur.execute(
        "SELECT id, name, email FROM users WHERE email = ? AND password = ?",
        (data['email'], data['password'])
    )
    user = cur.fetchone()

    if user:
        return jsonify({
            "message": "Login successful",
            "user": dict(user)
        }), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401







if __name__ == '__main__':
    app.run(debug=True)