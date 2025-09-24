 
  

# 💸 Expense Splitter

[![GitHub Repo](https://img.shields.io/badge/View_on-GitHub-black?logo=github)](https://github.com/YOUR-USERNAME/expense-splitter)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)  
![Flask](https://img.shields.io/badge/Flask-Backend-lightgrey?logo=flask)  
![SQLite](https://img.shields.io/badge/Database-SQLite-blue?logo=sqlite)  
![Status](https://img.shields.io/badge/Project-Active-brightgreen)  

![Last Commit](https://img.shields.io/github/last-commit/YOUR-USERNAME/expense-splitter?logo=git)  
![Issues](https://img.shields.io/github/issues/YOUR-USERNAME/expense-splitter?logo=github)  
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

📂 Project Setup

1️⃣ Clone the repo

git clone https://github.com/rohithashiny/expense-splitter.git
cd expense-splitter

2️⃣ Install dependencies

pip install flask

3️⃣ Run the server

python app.py

Server runs on 👉 http://127.0.0.1:5000/


---

📌 API Endpoints

👤 Users

POST /users → Add a new user


{
  "name": "Nova",
  "email": "nova@example.com"
}

GET /users → List all users



---

💰 Expenses

POST /expenses → Add an expense (auto-split)


{
  "user_id": 1,
  "amount": 600,
  "description": "Dinner with friends"
}

GET /expenses → List all expenses

DELETE /expenses/<id> → Delete an expense



---

🔗 Expense Shares

GET /expense_shares → List all splits with user names



---

📊 Balances

GET /balances → Show net balance for each user


{
  "Nova": 300,
  "roni": -300
}


---

🤝 Settlements

GET /settlements → Show who owes whom


[
  "Rovi owes Nova ₹300"
]


---

🧪 Testing

Use Thunder Client / Postman:

1. Add a few users


2. Add expenses


3. Check balances & settlements




---

📸 Screenshots