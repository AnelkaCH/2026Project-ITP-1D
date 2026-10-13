import json
import streamlit as st
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent/"data"/"ticket_type.json"
)

def load_ticket_types():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

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

    st.divider()
        
    if st.button("Exit to Home"):
        st.session_state.current_page = "home"
        st.rerun()