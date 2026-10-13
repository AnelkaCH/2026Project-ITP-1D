import streamlit as st
from services.json_service import load_ticket_types, load_accounts, save_accounts

def show_home():
    st.title("🎟️ TicketHub")
    st.subheader("Your next experience starts here!")

    st.write(
        "Discover events, explore experiences, and find your next favourite event."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Want to explore the park?")
        st.write("Go there now!")

    with col2:
        if st.button("Browse Tickets", use_container_width=True):
            st.session_state.current_page = "browse_tickets"
            st.rerun()

    st.subheader("Already bought tickets? View your orders!")
    
    users=load_accounts()
    for user in users:
        if user["email"] == st.session_state.current_account:
            if not user["tickets"]:
                st.write("You have no ticket orders yet.")
            for i, ticket in enumerate(user["tickets"]):
                st.write(f"**{ticket['type']}**")
                st.write(f"Time of Order: {ticket['time_of_order']}")
                st.write(f"Date of Planned Visit: {ticket['date_of_visit']}")

                if st.button("See More", key=f"see_more_{i}"):
                    st.session_state.selected_ticket = i
                    st.session_state.current_page = "display_orders"
                    st.rerun()

                st.divider()

            break



