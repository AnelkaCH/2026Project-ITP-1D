import json
from pathlib import Path

ACC_FILE = (Path(__file__).resolve().parent.parent/"data"/"account_info.json")
TICKET_FILE = (Path(__file__).resolve().parent.parent/"data"/"ticket_type.json")

def load_accounts():
    with open(ACC_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def load_ticket_types():
    with open(TICKET_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_accounts(accounts):
    with open(ACC_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)