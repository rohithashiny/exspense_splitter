 
  

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


📸 Screenshots

## 📸 API Screenshots

### 1) Users (POST /users, GET /users)
![Users API](https://raw.githubusercontent.com/rohithashiny/exspense_splitter/refs/heads/main/screenshots_splitter/users.png

)  
Create and list users.

---

### 2) Expenses (POST /expenses, GET /expenses)
![Expenses API](https://raw.githubusercontent.com/rohithashiny/exspense_splitter/refs/heads/main/screenshots_splitter/expenses.png)  
Add an expense and list all expenses.

---

### 3) Expense Shares (POST /expense_shares, GET /expense_shares)
![Expense Shares API](https://raw.githubusercontent.com/rohithashiny/exspense_splitter/refs/heads/main/screenshots_splitter/expenses_shares.png)  
Shows how expense shares are recorded (automatically split).

---

### 4) Balances (GET /balances)
![Balances API](https://raw.githubusercontent.com/rohithashiny/exspense_splitter/refs/heads/main/screenshots_splitter/balances.png)  
Balances per user after splitting expenses (who owes whom).

---

### 5) Settlements (POST /settlements, GET /settlements)
![Settlements API](https://raw.githubusercontent.com/rohithashiny/exspense_splitter/refs/heads/main/screenshots_splitter/settlements.png)  
Mark a settlement/payments between users.




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
<img width="1531" height="329" alt="Screenshot 2025-09-24 172455" src="https://github.com/user-attachments/assets/93669d03-f3d6-4010-866a-006ae4450720" />
<img width="1495" height="233" alt="Screenshot 2025-09-24 172431" src="https://github.com/user-attachments/assets/cd7fbc26-6dcb-40cb-bf0c-75070255a1aa" />
<img width="1442" height="453" alt="Screenshot 2025-09-24 172356" src="https://github.com/user-attachments/assets/77793ccc-9e33-4519-9e73-3d25148ab738" />

🧪 Testing

Use Thunder Client / Postman:

1. Add a few users


2. Add expenses


3. Check balances & settlements




---

