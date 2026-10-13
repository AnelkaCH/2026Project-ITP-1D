from services.json_service import load_accounts, save_accounts
import hashlib

def register_account(email, password, salt):
    accounts = load_accounts()

    for account in accounts:
        if account["email"].lower() == email.lower():
            return False, "This email is already registered."

    accounts.append({
        "email": email,
        "password": password,
        "salt": salt,
        "tickets": []
    })

    save_accounts(accounts)

    return True, "Account created successfully! Please login now."

def login_account(email, password):
    accounts = load_accounts()
    for account in accounts:
        if account["email"].lower() == email.lower():
            hash_object = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(account["salt"]), 100000)
            if hash_object == bytes.fromhex(account["password"]):
                return True, "Login successful!"
            else:
                return False, "Invalid email or password."
    return False, "Invalid email or password."
