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

    # Get the selected ticket (may be missing if the page was opened directly)
    selected_ticket = st.session_state.get("selected_ticket")
    tickets = current_user.get("tickets", []) if current_user else []

    if selected_ticket is None or not (0 <= selected_ticket < len(tickets)):
        st.info("No order selected. Choose an order from the home page.")
        if st.button("Back to home"):
            st.switch_page(st.session_state.pages["home"])
        return

    ticket = tickets[selected_ticket]

    # Display ticket details
    st.subheader(ticket["type"])
    st.write("Date of Visit:", ticket["date_of_visit"])
    st.write("Time of Order:", ticket["time_of_order"])

    st.divider()

    # Display the amount of tickets and total price
    st.write("Adults:", ticket["adults"])
    st.write("Children:", ticket["children"])
    st.write("Total Price: $", ticket["total_price"])

    st.divider()

    # if user presses back to home button goes back top home
    if st.button("Back to home"):
        st.switch_page(st.session_state.pages["home"])

