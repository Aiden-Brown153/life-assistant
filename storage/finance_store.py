import json
import os

FILE_PATH = "storage/finance.json"

def load_transactions():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_transactions(transactions):
    with open(FILE_PATH, "w") as f:
        json.dump(transactions, f, indent=4)
