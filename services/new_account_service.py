from services.json_service import load_accounts, save_accounts
import hashlib

def register_account(email, password, salt): #Defining the function for allowing the user to create an account
    accounts = load_accounts()

    for account in accounts: #Loads json file onto the variable
        if account["email"].lower() == email.lower(): #Making it so that email is not case sensitive
            return False, "This email is already registered."

    accounts.append({ #Adding the new users information into the 'accounts' 
        "email": email,
        "password": password,
        "salt": salt,
        "tickets": [],
        "used_voucher": []
    })

    save_accounts(accounts) #Adding the user information back into the Json file

    return True, "Account created successfully! Please login now." 

def login_account(email, password): #Defining a function to let the users login and hash it for data safety
    accounts = load_accounts()
    for account in accounts:
        if account["email"].lower() == email.lower():
            hash_object = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(account["salt"]), 100000)
            if hash_object == bytes.fromhex(account["password"]):
                return True, "Login successful!"
            else:
                return False, "Invalid email or password."
    return False, "Invalid email or password."
