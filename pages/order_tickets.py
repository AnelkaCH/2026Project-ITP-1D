import streamlit as st
from datetime import date
from services.json_service import load_ticket_types, load_accounts, save_accounts

def show_order_tickets():
    st.title("Order Tickets")
    ticket_types = load_ticket_types()

    current_ticket = None

    for ticket in ticket_types:
        if ticket["id"] == st.session_state.current_ticket_order:
            current_ticket = ticket
            break

    if current_ticket is None:
        st.error("Ticket type not found.")
        return
    else:
        st.write("Currently ordering:", current_ticket["name"])
        st.write(current_ticket["description"])

    selected_date = st.date_input(
        "Select a date",
        value=date.today()
    )

    st.write("Selected date:", selected_date)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("-", key="minus"):
            if st.session_state.quantity_adult > 0:
                st.session_state.quantity_adult -= 1

    with col2:
        st.write(f"### {st.session_state.quantity_adult}")

    with col3:
        if st.button("+", key="plus"):
            st.session_state.quantity_adult += 1

    st.divider()

    col4, col5, col6 = st.columns([1, 2, 1])

    with col4:
        if st.button("-", key="minus_child"):
            if st.session_state.quantity_child > 0:
                st.session_state.quantity_child -= 1

    with col5:
        st.write(f"### {st.session_state.quantity_child}")

    with col6:
        if st.button("+", key="plus_child"):
            st.session_state.quantity_child += 1

    st.divider()

    if st.button("Purchase Order"):
        total_adult_price = st.session_state.quantity_adult * current_ticket["adult_price"]
        total_child_price = st.session_state.quantity_child * current_ticket["child_price"]

        total_price = total_adult_price + total_child_price

        # Load existing accounts
        users = load_accounts()

        # Find the current user
        for user in users:
            if user["email"] == st.session_state.current_account:

                # Add the ticket order
                user["tickets"].append({
                    "type": current_ticket["name"],
                    "date": str(selected_date),
                    "adults": st.session_state.quantity_adult,
                    "children": st.session_state.quantity_child,
                    "total_price": total_price
                })

                break

        # Save updated accounts
        save_accounts(users)

        st.success("Order submitted successfully!")

        st.session_state.quantity_adult = 0
        st.session_state.quantity_child = 0
        st.session_state.current_page = "home"
        st.rerun()

    if st.button("Cancel Order"):
        st.session_state.quantity_adult = 0
        st.session_state.quantity_child = 0
        st.session_state.current_page = "home"
        st.rerun()