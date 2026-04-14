import tkinter as tk
from tkinter import ttk, messagebox
from logic.finance_logic import get_transactions, add_transaction, delete_transaction, monthly_summary
from datetime import datetime

class FinanceUI:
    def __init__(self, root):
        self.root = root

        # ===== MAIN CONTAINER =====
        main = ttk.Frame(root, padding=20)
        main.pack(fill="both", expand=True)

        # ===== HEADER =====
        header = ttk.Label(
            main,
            text="Finance Tracker",
            font=("Segoe UI", 16, "bold")
        )
        header.pack(anchor="w", pady=(0, 15))

        # ===== CONTENT AREA =====
        content = ttk.Frame(main)
        content.pack(fill="both", expand=True)

        # LEFT: INPUTS
        input_frame = ttk.LabelFrame(content, text="Add Transaction", padding=15)
        input_frame.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(input_frame, text="Date (YYYY-MM-DD):").pack(anchor="w")
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.pack(pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(input_frame, text="Amount:").pack(anchor="w")
        self.amount_entry = ttk.Entry(input_frame, width=20)
        self.amount_entry.pack(pady=5)

        ttk.Label(input_frame, text="Category:").pack(anchor="w")
        self.category_entry = ttk.Entry(input_frame, width=20)
        self.category_entry.pack(pady=5)

        self.add_button = ttk.Button(
            input_frame,
            text="Add Transaction",
            command=self.add_transaction
        )
        self.add_button.pack(pady=(10, 0), fill="x")

        # RIGHT: LIST
        list_frame = ttk.LabelFrame(content, text="Transactions", padding=15)
        list_frame.pack(side="right", fill="both", expand=True)

        self.transaction_list = tk.Listbox(list_frame, height=15)
        self.transaction_list.pack(fill="both", expand=True)

        # ===== ACTION BAR =====
        actions = ttk.Frame(main)
        actions.pack(fill="x", pady=(10, 0))

        ttk.Button(actions, text="Monthly Summary", command=self.show_summary).pack(side="left")
        ttk.Button(actions, text="Delete", command=self.delete_transaction).pack(side="left", padx=5)

        # ===== STATUS BAR =====
        self.status_label = ttk.Label(main, text="", foreground="green")
        self.status_label.pack(fill="x", pady=(10, 0))

        # ===== LOAD TRANSACTIONS FROM STORAGE =====
        self.transactions = get_transactions()
        self.refresh_list()

    def add_transaction(self):
        date = self.date_entry.get().strip()
        amount = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()

        if not date or not amount or not category:
            messagebox.showwarning("Input error", "Please fill all fields.")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
            amount_val = float(amount)
        except ValueError:
            messagebox.showwarning("Input error", "Invalid date or amount format.")
            return

        add_transaction(date, amount_val, category)
        self.refresh_list()
        self.show_status("Transaction added!")

        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def refresh_list(self):
        self.transaction_list.delete(0, tk.END)
        self.transactions = get_transactions()
        for t in self.transactions:
            self.transaction_list.insert(
                tk.END,
                f"{t['date']} | {t['amount']:.2f} | {t['category']}"
            )

    def show_summary(self):
        now = datetime.now()
        income, expenses = monthly_summary(now.year, now.month)
        messagebox.showinfo(
            "Monthly Summary",
            f"Income: {income:.2f}\nExpenses: {expenses:.2f}"
        )

    def delete_transaction(self):
        selected = self.transaction_list.curselection()
        if not selected:
            messagebox.showwarning("Selection error", "Please select a transaction to delete.")
            return

        index = selected[0]
        delete_transaction(index)
        self.refresh_list()
        self.show_status("Transaction deleted!")

    def show_status(self, message):
        self.status_label.config(text=message)
        self.root.after(3000, lambda: self.status_label.config(text=""))  # Clear after 3 seconds
