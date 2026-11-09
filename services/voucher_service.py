from services.json_service import load_accounts, load_valid_vouchers

def is_voucher_used(email, voucher_id):
    accounts = load_accounts()
    account = next((u for u in accounts if u.get("email") == email), None)
 
    if account is None:
        return True  # unknown account: treat as not allowed
 
    used = [str(v) for v in account.get("used_voucher", [])]
    return str(voucher_id) in used


def apply_voucher(voucher_input, current_ticket, email):
    if not voucher_input or not voucher_input.strip():
        return False, None

    code = voucher_input.strip().lower()
    voucher = next(
        (v for v in load_valid_vouchers()
         if v["voucher_name"].strip().lower() == code),
        None
    )

    if voucher is None:
        return False, None

    # Ticket eligibility
    allowed_ids = {
        str(t.get("ticket_type_id"))
        for t in voucher.get("valid_type_for_voucher", [])
    }

    if str(current_ticket.get("id")) not in allowed_ids:
        return False, None

    # Already used by this account
    if is_voucher_used(email, voucher.get("voucher_id")):
        return False, None

    return True, voucher


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