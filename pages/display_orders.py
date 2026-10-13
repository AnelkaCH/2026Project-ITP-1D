import streamlit as st
from services.json_service import load_accounts

def show_display_orders():
    users = load_accounts()
    current_user = None

    # Find the logged-in user
    for user in users:
        if user["email"] == st.session_state.current_account:
            current_user = user
            break

    # Get the selected ticket
    selected_ticket = st.session_state.selected_ticket
    tickets = current_user["tickets"]

    if selected_ticket < 0 or selected_ticket >= len(tickets):
        st.error("Ticket not found.")
        return

    ticket = tickets[selected_ticket]

    # Display ticket details
    st.subheader(ticket["type"])
    st.write("Date:", ticket["date"])

    st.divider()

    st.write("Adults:", ticket["adults"])
    st.write("Children:", ticket["children"])
    st.write("Total Price: $", ticket["total_price"])

    st.divider()

    if st.button("Back to home"):
        st.session_state.current_page = "home"
        st.rerun()

