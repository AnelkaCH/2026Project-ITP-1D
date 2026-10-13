import json
import streamlit as st
from pathlib import Path


DATA_FILE = (
    Path(__file__).resolve().parent.parent/"data"/"account_info.json"
)

def load_accounts():
    print("Loading from:", DATA_FILE)

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

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

    st.subheader("Already bought tickets?")
    st.write("View your orders!")
    users=load_accounts()
    for user in users:
        if user["email"] == st.session_state.current_account:

            for i, ticket in enumerate(user["tickets"]):
                st.write(f"**{ticket['type']}**")
                st.write(f"Date: {ticket['date']}")

                if st.button("See More", key=f"see_more_{i}"):
                    st.session_state.selected_ticket = i
                    st.session_state.current_page = "display_orders"
                    st.rerun()

                st.divider()

            break
            
    if st.button("View Orders", use_container_width=True):
        st.session_state.current_page = "display_orders"
        st.rerun()



