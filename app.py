from flask import Flask, jsonify
from db import init_db, get_conn
from flask import request
import sqlite3
app = Flask(__name__)
init_db()
@app.route('/')
def home():
    return "Expense Splitter is running!"

@app.route('/users', methods=['GET'])
def list_users():
    try:
        conn = get_conn()
        conn.row_factory = sqlite3.Row  # <-- this makes rows behave like dicts
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        conn.close()

        users = []
        for row in rows:
            users.append({"id": row["id"], "name": row["name"], "email": row["email"]})

        return jsonify(users)
    except Exception as e:
        print("Error in GET /users:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route('/users', methods=['POST'])
def add_user():

    try:
        data = request.get_json()  
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            return jsonify({"error": "Name and email are required"}), 400

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
        if conn:
            try:
                conn.close()
            except Exception:
                pass

if __name__ == '__main__':
    app.run(debug=True)