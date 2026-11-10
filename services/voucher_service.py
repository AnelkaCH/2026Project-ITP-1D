from services.json_service import load_accounts, load_valid_vouchers
from datetime import date


def find_voucher(code):
    code = code.strip().lower()
    voucher = None
    for v in load_valid_vouchers():
        if v["voucher_name"].strip().lower() == code:
            voucher = v
            break
    return voucher

def check_voucher(voucher, ticket, email, visit_date):
    allowed_ids = {
        str(t.get("ticket_type_id"))
        for t in voucher.get("valid_type_for_voucher", [])
    }
    if str(ticket["id"]) not in allowed_ids:
        return "This voucher is not applicable to the selected ticket type."

    if not is_voucher_date_valid(voucher, visit_date):
        return f"This voucher is only valid from {voucher['valid_from']} to {voucher['valid_until']}."

    if is_voucher_used(email, voucher["voucher_id"]):
        return "This voucher has already been used by your account."

    return None


def apply_voucher(voucher_input, ticket, email, visit_date):
    if not voucher_input or not voucher_input.strip():
        return False, None, "Please input a voucher code."

    voucher = find_voucher(voucher_input)
    if voucher is None:
        return False, None, "Invalid voucher code."

    error = check_voucher(voucher, ticket, email, visit_date)
    if error:
        return False, None, error

    return True, voucher, "Voucher applied successfully."

def is_voucher_date_valid(voucher, visit_date):
    try:
        valid_from = date.fromisoformat(voucher["valid_from"])
        valid_until = date.fromisoformat(voucher["valid_until"])
    except (KeyError, ValueError):
        return False

    return valid_from <= visit_date <= valid_until

def is_voucher_used(email, voucher_id):
    accounts = load_accounts()
    account = None
    for u in accounts:
        if u.get("email") == email:
            account = u
            break
 
    if account is None:
        return True  # unknown account: treat as not allowed
 
    used = [str(v) for v in account.get("used_voucher", [])]
    return str(voucher_id) in used


def apply_voucher(voucher_input, ticket, email, visit_date):
    if not voucher_input or not voucher_input.strip():
        return False, None, "Please input a voucher code."

    voucher = find_voucher(voucher_input)
    if voucher is None:
        return False, None, "Invalid voucher code."

    error = check_voucher(voucher, ticket, email, visit_date)
    if error:
        return False, None, error

    return True, voucher, "Voucher applied successfully."


def calculate_discount(voucher, total_price):
    # to calculate discount
    if voucher is None:
        return round(total_price, 2)

    discount = voucher["amount_discounted"]

    if voucher.get("is_percentage", False):
        total_price = total_price * (1 - discount)
    else:
        total_price = max(0, total_price - discount)
 
    return round(total_price, 2)

 
def format_discount(voucher):
    # Readable discount label for the UI.
    amount = voucher["amount_discounted"]
    if voucher.get("is_percentage", False):
        return f"{amount:.0%} off"
    return f"${amount:.2f} off"