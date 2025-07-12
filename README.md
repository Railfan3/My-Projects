# My-Projects 


💰 Secure Bank System (GUI-Based in Python)
This is a simple, secure GUI-based banking system built using Python's tkinter module. It allows users to register, login, deposit, withdraw, view balance, and check transaction history, all securely handled with password hashing using bcrypt.

🛠️ Features
🧾 User Registration & Login

🔒 Password Security using bcrypt hashing

💵 Deposit & Withdraw Money

📊 Check Account Balance

📜 View Transaction History in a tabular format

💽 Data Persistence using JSON file (bank_data.json)

🧰 Tech Stack
Python 3

tkinter – GUI

bcrypt – Password Hashing

json – Data Storage

datetime – Timestamp for transactions

🚀 Getting Started
1. Install Python Requirements
Make sure you have Python 3 installed.

Install bcrypt if not already installed:

bash
Copy
Edit
pip install bcrypt
2. Run the App
bash
Copy
Edit
python your_script_name.py
(Replace your_script_name.py with the actual filename.)

📂 Project Structure
bash
Copy
Edit
├── bank_data.json        # JSON file for storing users and transactions
├── your_script_name.py   # Main GUI-based banking system code
└── README.md             # Project documentation
📌 Data Storage Format (bank_data.json)
Each user is stored as a dictionary with:

json
Copy
Edit
"username": {
  "password": "hashed_password",
  "balance": 1000.0,
  "transactions": [
    {
      "type": "Deposit",
      "amount": 100.0,
      "time": "2025-07-12 13:00:00"
    }
  ]
}
🛡️ Security
Passwords are never stored in plain text.

bcrypt is used to hash passwords securely before saving.

Login verifies credentials using bcrypt.checkpw().

📸 GUI Preview
You will be presented with:

Login/Register window

Dashboard with buttons for all banking operations

Transaction history displayed in a table (using ttk.Treeview)

🧑‍💻 Author
Mukul Chouhan
Electronics and Communication Engineering Student
GitHub: @Railfan3

