import streamlit as st
from datetime import date, datetime
from services.json_service import load_ticket_types, load_accounts, save_accounts, load_valid_vouchers

def show_order_tickets():
    #Initialize variables
    ticket_types = load_ticket_types()
    current_ticket = None

    # Loops through tickets types and get the id of each ticket, saves into memory
    for ticket in ticket_types:
        # Check if the current ticket id is the correct ticket
        if ticket["id"] == st.session_state.current_ticket_order:
            current_ticket = ticket
            break

    st.title("Order Tickets. Currently ordering:", current_ticket["name"])
    st.write(current_ticket["description"])

    st.write("When do you plan to visit the park? Please select a date below.")
    
    # Creates a UI calender popup, sees days before and days today and after
    selected_date = st.date_input(
        "Select a date",
        value=date.today(),
        min_value=date.today()
    )

    '''
    Creates table, with two columns
    Column 1 is the size of 2 columns merged together
    Column 2 is the size of 3 columns merged together
    '''
    t1col1, t1col2 = st.columns([2, 3])

    # Writes the number of tickets and price respectively    
    with t1col1:
        st.write("### Adult Tickets")
        st.write(f"Price: ${current_ticket['adult_price']} each")
    
    with t1col2:
        st.session_state.adults = st.number_input("Number of adults", min_value=0, max_value=10, step=1)

    st.divider()

    t2col1, t2col2 = st.columns([2, 3])

    with t2col1:
        st.write("### Child Tickets")
        st.write(f"Price: ${current_ticket['child_price']} each")

    with t2col2:
        st.session_state.children = st.number_input("Number of children", min_value=0, max_value=10, step=1)

    st.divider()

    # Calculate total price
    total_adult_price = st.session_state.adults * current_ticket["adult_price"]
    total_child_price = st.session_state.children * current_ticket["child_price"]

    total_price = total_adult_price + total_child_price
    
    # Show the voucher form in a narrow column.
    voucher_col, _ = st.columns([1, 2])
    with voucher_col:
        # Apply the voucher only when the button is clicked.
        with st.form("voucher_form"):
            voucher_input = st.text_input(
                "Voucher code",
                key=f"voucher_code_{current_ticket['id']}"
            )
            confirm_voucher = st.form_submit_button("Confirm Voucher")

        # Find the voucher when the form is submitted.
        vouchers = load_valid_vouchers()
        if confirm_voucher:
            # Clear the old voucher if the code changed.
            if st.session_state.get("applied_voucher_code") != voucher_input.strip().lower():
                st.session_state.pop("applied_voucher", None)
                st.session_state.pop("applied_voucher_code", None)

            voucher = None
            # Find a voucher with this code.
            for item in vouchers:
                if item["voucher_name"].strip().lower() == voucher_input.strip().lower():
                    voucher = item
                    break
            # Check whether this account has used the voucher before.
            if voucher is not None:
                users = load_accounts()
                account = None
                for user in users:
                    if user.get("email") == st.session_state.current_account:
                        account = user
                        break
                voucher_name = voucher["voucher_name"].strip().lower()
                already_used = False
                if account is not None:
                    # Check this account's past orders.
                    for order in account.get("tickets", []):
                        order_voucher = order.get("voucher", "")
                        # Support both old and new voucher formats.
                        if isinstance(order_voucher, dict):
                            order_voucher = order_voucher.get("voucher_name", "")
                        else:
                            order_voucher = order_voucher or ""

                        # Ignore letter case and extra spaces.
                        if order_voucher.strip().lower() == voucher_name:
                            already_used = True
                            break

                if already_used:
                    st.session_state.pop("applied_voucher", None)
                    st.session_state.pop("applied_voucher_code", None)
                    st.write("This voucher has been used!")
                else:
                    # Save the voucher so it remains applied after Streamlit reruns.
                    st.session_state.applied_voucher = voucher
                    st.session_state.applied_voucher_code = voucher_input.strip().lower()
            
            # Clear the applied voucher if the code is invalid.
            else:
                st.session_state.pop("applied_voucher", None)
                st.session_state.pop("applied_voucher_code", None)
                st.write("Invalid voucher")

        voucher = st.session_state.get("applied_voucher")
        if voucher is not None:
            # Check whether the voucher is allowed for the selected ticket type.
            eligible_types = None
            for key in ("ticket_types", "ticket_type_ids", "ticket_type_id", "ticket_type"):
                value = voucher.get(key)
                if value is not None and value != "":
                    eligible_types = value
                    break

            if eligible_types is None:
                # A voucher without an explicit ticket type restriction is invalid.
                voucher_applies = False
            else:
                # Gather allowed ticket IDs or names into a list for comparison.
                allowed_types = []

                # Check each allowed type, including values inside lists.
                # Start with the ticket types allowed by this voucher.
                pending_types = [eligible_types]
                for value in pending_types:
                    # check if the value is a dict
                    if isinstance(value, dict):
                        value = value.get(
                            "id", value.get("ticket_type_id", value.get("name", ""))
                        )
                    # Add each item in a group to the list we still need to check.
                    if isinstance(value, (list, tuple, set)):
                        pending_types.extend(value)
                    elif value is not None:
                        # Split text containing several types, then save each one in lowercase.
                        for item in str(value).replace("/", ",").replace("|", ",").replace(";", ",").split(","):
                            if item.strip():
                                allowed_types.append(item.strip().lower())

                # Match the voucher using either the ticket ID or its name.
                ticket_values = {
                    str(current_ticket.get("id", "")).strip().lower(),
                    str(current_ticket.get("name", "")).strip().lower(),
                }
                voucher_applies = bool(
                    ticket_values.intersection(value.strip().lower() for value in allowed_types)
                )

            if voucher_applies:
                # Apply a percentage discount or subtract a fixed amount.
                discount = voucher["amount_discounted"]
                discounted_price = total_price
                if voucher.get("is_percentage", False):
                    discounted_price *= 1 - discount / 100
                else:
                    discounted_price = max(0, discounted_price - discount)
                total_price = discounted_price
            else:
                st.info("This voucher does not apply to the selected ticket type.")
    st.subheader(f"Order Summary: ${total_price:.2f}")
        
    '''
    Creates table, with three columns
    Column 1 & 2 is the size of 2 columns merged together
    Column 3 is size of 13 columns merged together
    '''
    t4col1, t4col2, t4col3 = st.columns([2, 2, 13])
    with t4col1:
        if st.button("Continue Purchase"):
            #Store current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load existing accounts
            users = load_accounts()

            # Find the current user
            for user in users:
                if user["email"] == st.session_state.current_account:

                    # Add the ticket order
                    user["tickets"].append({
                        "type": current_ticket["name"],
                        "date_of_visit": str(selected_date),
                        "time_of_order": current_time,
                        "adults": st.session_state.adults,
                        "children": st.session_state.children,
                        "voucher": voucher,
                        "total_price": total_price
                    })

                    break

            # Save updated accounts
            save_accounts(users)

            st.success("Order submitted successfully!")

            # Resets session states for adult and children to 0
            st.session_state.adults = 0
            st.session_state.children = 0
            st.switch_page(st.session_state.pages["home"])

    with t4col2:
        # Resets session states for adult and children to 0 if cancel order button is pressed
        if st.button("Cancel Order"):
            st.session_state.adults = 0
            st.session_state.children = 0
            st.switch_page(st.session_state.pages["home"])