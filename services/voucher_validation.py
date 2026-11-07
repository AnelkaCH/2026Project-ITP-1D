import streamlit as st

from services.json_service import load_accounts, load_valid_vouchers

# initialise key for extracting ticket identifiers and names from voucher dictionaries
VOUCHER_TICKET_KEYS = ["id", "ticket_type_id", "name", "ticket_type_name"]

def normalize_allowed_ticket_values(value):
    """Return all valid ticket ids/names from a voucher field as lowercase strings."""
    if value is None:
        return set()

    # If the value is a dictionary, extract possible ticket identifiers and names
    if isinstance(value, dict):
        value = [value.get(key) for key in VOUCHER_TICKET_KEYS]

    # check if the ticket type is a list
    if isinstance(value, list):
        allowed = set()
        # loops through the set of dicts and then updates the dict into the set
        for item in value:
            # calls func again and extracts the id and the name of the voucher puts inside a dict
            # stops when there is an empty dict 
            allowed.update(normalize_allowed_ticket_values(item))
        return allowed

    #in the event of strings , but this will never happen as json is formatted as list of dicts
    cleaned = str(value).strip().lower()
    return {cleaned} if cleaned else set()

def validate_and_apply_voucher(voucher_input, confirm_voucher, current_ticket, total_price):
    #load valid vouchers 
    vouchers = load_valid_vouchers()
    # get id and name and clean them
    ticket_values = {
        str(current_ticket.get("id", "")).strip().lower(),
        str(current_ticket.get("name", "")).strip().lower(),
    }
    # sort ticket key in ascending order
    ticket_key = tuple(sorted(ticket_values))

    # when user confirms that he uses the voucher the and if the vouicher doesnt apply, discount is not applied
    if confirm_voucher:
        code = voucher_input.strip().lower()
        if st.session_state.get("applied_voucher_code") != code:
            st.session_state.pop("applied_voucher", None)
            st.session_state.pop("applied_voucher_code", None)
            st.session_state.pop("applied_voucher_ticket", None)

        # when the voucher is valid and break out of the loop
        voucher = None
        for item in vouchers:
            if item["voucher_name"].strip().lower() == code:
                voucher = item
                break

        # check if user changed the voucher code, clears previously applied discount so that it wont carry over
        if voucher is None:
            st.session_state.pop("applied_voucher", None)
            st.session_state.pop("applied_voucher_code", None)
            st.session_state.pop("applied_voucher_ticket", None)
            st.write("Invalid voucher")
            return st.session_state.get("applied_voucher"), total_price

        # gets the current valid type of voucher using a session state
        allowed_types = normalize_allowed_ticket_values(voucher.get("valid_type_for_voucher", []))
        
        # check if entered voucher code exists is applicable to the ticket type 
        if not ticket_values.intersection(allowed_types):
            st.session_state.pop("applied_voucher", None)
            st.session_state.pop("applied_voucher_code", None)
            st.session_state.pop("applied_voucher_ticket", None)
            st.info("This voucher does not apply to the selected ticket type.")
            return None, total_price

        # get current user
        account = None
        for user in load_accounts():
            if user.get("email") == st.session_state.current_account:
                account = user
                break
        
        voucher_name = voucher["voucher_name"].strip().lower()
        already_used = False

        # validate whether we used a voucher previously
        if account is not None:
            for order in account.get("tickets", []):
                order_voucher = order.get("voucher", "")
                if isinstance(order_voucher, dict):
                    order_voucher = order_voucher.get("voucher_name", "")
                if (order_voucher or "").strip().lower() == voucher_name:
                    already_used = True
                    break
        
        # if used set states to none and display voucher has been used
        if already_used:
            st.session_state.pop("applied_voucher", None)
            st.session_state.pop("applied_voucher_code", None)
            st.session_state.pop("applied_voucher_ticket", None)
            st.write("This voucher has been used!")
        else:
            st.session_state.applied_voucher = voucher
            st.session_state.applied_voucher_code = code
            st.session_state.applied_voucher_ticket = ticket_key

    voucher = st.session_state.get("applied_voucher")

    if voucher is not None:
        # check if voucher id is same, return total price
        if st.session_state.get("applied_voucher_ticket") != ticket_key:
            return voucher, total_price

        # check eligible types of voucher
        eligible_types = voucher.get("valid_type_for_voucher", [])
        allowed_types = normalize_allowed_ticket_values(eligible_types)
        # if the type of voucher is the same, can proceed to discount
        if ticket_values.intersection(allowed_types):
            discount = voucher["amount_discounted"]
            if voucher.get("is_percentage", False):
                total_price *= (1 - discount)
            else:
                # to handle negative total price
                total_price = max(0, total_price - discount)
        else:
            st.info("This voucher does not apply to the selected ticket type.")

    return voucher, total_price
