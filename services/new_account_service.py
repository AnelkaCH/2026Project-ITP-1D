import json
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent/"data"/"account_info.json"
)

def load_accounts():
    print("Loading from:", DATA_FILE)

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_accounts(accounts):
    print("Saving to:", DATA_FILE)
    print("Accounts to save:", accounts)

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)

    print("Save successful:", DATA_FILE.exists())


def register_account(email, password):
    accounts = load_accounts()

    for account in accounts:
        if account["email"].lower() == email.lower():
            return False, "This email is already registered."

    accounts.append({
        "email": email,
        "password": password,
        "tickets": []
    })

    save_accounts(accounts)

    return True, "Account created successfully! Please login now."

def login_account(email, password):
    accounts = load_accounts()

    for account in accounts:
        if account["email"].lower() == email.lower() and account["password"] == password:
            return True, "Login successful!"

    return False, "Invalid email or password."
