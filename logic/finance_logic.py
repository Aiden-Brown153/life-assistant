from storage.finance_store import load_transactions, save_transactions
from datetime import datetime

def get_transactions():
    return load_transactions()

def add_transaction(date, amount, category):
    transactions = load_transactions()
    transactions.append({
        "date": date,
        "amount": amount,
        "category": category
    })
    save_transactions(transactions)

def delete_transaction(index):
    transactions = load_transactions()
    if 0 <= index < len(transactions):
        transactions.pop(index)
        save_transactions(transactions)

def monthly_summary(year, month):
    transactions = load_transactions()
    income = 0
    expenses = 0
    for t in transactions:
        if t["date"].startswith(f"{year}-{month:02d}"):
            if t["amount"] > 0:
                income += t["amount"]
            else:
                expenses += abs(t["amount"])
    return income, expenses
