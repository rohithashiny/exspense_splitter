 
  

# 💸 Expense Splitter
[![Badge displaying View on GitHub with the GitHub logo in black and white](https://img.shields.io/badge/View_on-GitHub-black?logo=github)](https://github.com/rohithashiny/exspense_splitter)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)  
![Flask](https://img.shields.io/badge/Flask-Backend-lightgrey?logo=flask)  
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)  
![Status](https://img.shields.io/badge/Project-Active-brightgreen)  

![Last Commit](https://img.shields.io/github/last-commit/rohithashiny/exspense_splitter?logo=git)  
![Issues](https://img.shields.io/github/issues/rohithashiny/exspense_splitter?logo=github)  
![Status](https://img.shields.io/badge/Project-Active-brightgreen)  
This is an internship project I’m building step by step while learning Flask, databases, and GitHub workflows.
---

A simple expense sharing application built with Flask + SQLite.
It allows users to add expenses, automatically split costs, track balances, and view settlements (like Splitwise basics).


---

🚀 Features

👤 Manage Users (Add/List)

💰 Add Expenses (auto-split across all users)

📊 View Balances (see who paid vs who owes)

🔗 Settlements (clear “who owes whom” instructions)

🗑 Delete Expenses (auto-remove related shares)



---

🛠 Tech Stack

Backend: Python, Flask

Database: SQLite

API Testing: Thunder Client / Postman

Version Control: Git + GitHub



---

## 🚀 Project Setup

### 1️⃣ Clone the repo
```bash
git clone https://github.com/rohitashiny/expense-splitter.git
cd expense-splitter

2️⃣ Install dependencies

pip install -r requirements.txt

> ⚡ Don’t have requirements.txt yet? Just run:

pip install flask sqlite3
pip freeze > requirements.txt



3️⃣ Run the server

python app.py

Server runs on 👉 http://127.0.0.1:5000/


---

📌 API Endpoints

### 👤 Users
- *Create User*
```http
POST /users

Body (JSON)

{
  "name": "Alice",
  "email": "alice@example.com"
}

List Users


GET /users


---

💸 Expenses

Add Expense


POST /expenses

Body (JSON)

{
  "user_id": 1,
  "amount": 500,
  "description": "Dinner with friends"
}

List Expenses


GET /expenses


---

🔀 Expense Shares

Add Expense Share (optional if not auto-split)


POST /expense_shares

Body (JSON)

{
  "expense_id": 1,
  "user_id": 2,
  "amount": 250
}

List Expense Shares


GET /expense_shares


---

📊 Balances

View Balances


GET /balances

Response Example

{
  "1": 250.0,
  "2": -250.0
}


---

❌ Delete Expense

Delete an Expense


DELETE /expenses/<expense_id>

---

This way:
- Every endpoint has *copy-paste ready examples*.  
- Recruiters/teammates don’t even need to guess the JSON body.  
- Looks professional like real open-source projects.

🧪 Testing

Use Thunder Client / Postman:

1. Add a few users


2. Add expenses


3. Check balances & settlements




---

📸 Screenshots