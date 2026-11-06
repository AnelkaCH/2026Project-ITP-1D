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
    
    
    # Keep the voucher input in a single column narrower than half the page.
    voucher_col, _ = st.columns([1, 2])
    with voucher_col:
        # Disable Enter-to-submit so the voucher is applied only by clicking the button.
        with st.form("voucher_form", enter_to_submit=False):
            voucher_input = st.text_input(
                "Voucher code",
                key=f"voucher_code_{current_ticket['id']}"
            )
            confirm_voucher = st.form_submit_button("Confirm Voucher")

        # Find and apply a matching voucher, if one was entered
        vouchers = load_valid_vouchers()
        if confirm_voucher:
            voucher = None
            for item in vouchers:
                if item["voucher_name"].strip().lower() == voucher_input.strip().lower():
                    voucher = item
                    break
            # if voucher is valid save it to memory
            if voucher is not None:
                st.session_state.applied_voucher = voucher
                st.session_state.applied_voucher_code = voucher_input.strip().lower()
            
            # if the voucher is invalid set the states back to none and dispaly invalid voucher
            else:
                st.session_state.pop("applied_voucher", None)
                st.session_state.pop("applied_voucher_code", None)
                st.write("Invalid voucher")

        # Change in the voucher code must be checked again
        if st.session_state.get("applied_voucher_code") != voucher_input.strip().lower():
            st.session_state.pop("applied_voucher", None)
            st.session_state.pop("applied_voucher_code", None)

        voucher = st.session_state.get("applied_voucher")
        if voucher is not None:
            total_price *= voucher["amount_discounted"]

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