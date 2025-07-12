import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import json
import bcrypt
from datetime import datetime
import os

# Use absolute path to ensure file is created/read correctly
DATA_FILE = os.path.join(os.path.dirname(__file__), "bank_data.json")

# Load or initialize data
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({}, f)
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Bank System")
        self.root.geometry("500x500")
        self.data = load_data()
        self.current_user = None

        self.create_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Secure Bank", font=("Helvetica", 20, "bold")).pack(pady=20)

        tk.Button(self.root, text="Login", width=20, command=self.login_screen).pack(pady=10)
        tk.Button(self.root, text="Register", width=20, command=self.register_screen).pack(pady=10)

    def register_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Register New Account", font=("Helvetica", 16)).pack(pady=20)

        username = tk.Entry(self.root)
        password = tk.Entry(self.root, show="*")
        tk.Label(self.root, text="Username").pack()
        username.pack()
        tk.Label(self.root, text="Password").pack()
        password.pack()

        def register_action():
            uname = username.get().strip()
            pwd = password.get().strip()

            if uname == "" or pwd == "":
                messagebox.showerror("Error", "Username and password cannot be empty.")
                return

            if uname in self.data:
                messagebox.showerror("Error", "User already exists.")
                return
            hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()

            self.data[uname] = {
                "password": hashed,
                "balance": 0.0,
                "transactions": []
            }
            save_data(self.data)
            messagebox.showinfo("Success", "Account created successfully!")
            self.create_login_screen()

        tk.Button(self.root, text="Register", command=register_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_login_screen).pack()

    def login_screen(self):
        self.clear_window()
        tk.Label(self.root, text="Login", font=("Helvetica", 16)).pack(pady=20)

        username = tk.Entry(self.root)
        password = tk.Entry(self.root, show="*")
        tk.Label(self.root, text="Username").pack()
        username.pack()
        tk.Label(self.root, text="Password").pack()
        password.pack()

        def login_action():
            uname = username.get().strip()
            pwd = password.get().strip()

            if uname not in self.data:
                messagebox.showerror("Error", "User does not exist.")
                return
            stored_hash = self.data[uname]["password"].encode()

            if bcrypt.checkpw(pwd.encode(), stored_hash):
                self.current_user = uname
                self.dashboard_screen()
            else:
                messagebox.showerror("Error", "Incorrect password.")

        tk.Button(self.root, text="Login", command=login_action).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.create_login_screen).pack()

    def dashboard_screen(self):
        self.clear_window()
        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Helvetica", 16, "bold")).pack(pady=10)

        tk.Button(self.root, text="Deposit", width=20, command=self.deposit).pack(pady=5)
        tk.Button(self.root, text="Withdraw", width=20, command=self.withdraw).pack(pady=5)
        tk.Button(self.root, text="Check Balance", width=20, command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Transaction History", width=20, command=self.show_transactions).pack(pady=5)
        tk.Button(self.root, text="Logout", width=20, command=self.logout).pack(pady=10)

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter deposit amount:")
        if amount and amount > 0:
            self.data[self.current_user]["balance"] += amount
            self.record_transaction("Deposit", amount)
            save_data(self.data)
            messagebox.showinfo("Success", f"Deposited ₹{amount:.2f}")
        else:
            messagebox.showerror("Error", "Invalid amount.")

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter withdrawal amount:")
        if amount and amount > 0:
            if self.data[self.current_user]["balance"] >= amount:
                self.data[self.current_user]["balance"] -= amount
                self.record_transaction("Withdraw", amount)
                save_data(self.data)
                messagebox.showinfo("Success", f"Withdrawn ₹{amount:.2f}")
            else:
                messagebox.showerror("Error", "Insufficient funds!")
        else:
            messagebox.showerror("Error", "Invalid amount.")

    def check_balance(self):
        bal = self.data[self.current_user]["balance"]
        messagebox.showinfo("Balance", f"Your balance is ₹{bal:.2f}")

    def record_transaction(self, txn_type, amount):
        self.data[self.current_user]["transactions"].append({
            "type": txn_type,
            "amount": amount,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    def show_transactions(self):
        self.clear_window()
        tk.Label(self.root, text="Transaction History", font=("Helvetica", 16)).pack(pady=10)

        columns = ("Type", "Amount", "Time")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.pack(expand=True, fill="both")

        for txn in self.data[self.current_user]["transactions"]:
            tree.insert("", "end", values=(txn["type"], f"₹{txn['amount']:.2f}", txn["time"]))

        tk.Button(self.root, text="Back", command=self.dashboard_screen).pack(pady=10)

    def logout(self):
        self.current_user = None
        self.create_login_screen()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
