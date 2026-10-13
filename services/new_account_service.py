from services.json_service import load_accounts, save_accounts

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
