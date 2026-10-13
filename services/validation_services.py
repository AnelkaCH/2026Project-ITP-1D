import re

def is_valid_email(email):
    pattern = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"
    return re.match(pattern, email) is not None, "Please enter a valid email address."

def is_valid_password(password):
    has_number = False
    has_special_char = False
    has_uppercase = False
    if len(password) < 12:
        return False, "Password must be at least 12 characters long."

    for char in password:
        if char.isspace():
            return False, "Password cannot contain spaces."
        if char.isdigit():
            has_number = True
        if char in "!@#$%^&*()-_=+[]{}|;:',.<>?/":
            has_special_char = True
        if char.isupper():
            has_uppercase = True
    if not has_number:
            return False, "Password must contain at least one number."
    if not has_special_char:
            return False, "Password must contain at least one special character."
    if not has_uppercase:
            return False, "Password must contain at least one uppercase letter."

    return True, ""