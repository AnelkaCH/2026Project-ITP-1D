import json
import streamlit as st
from pathlib import Path

DATA_FILE = (
    Path(__file__).resolve().parent.parent/"data"/"ticket_type.json"
)

def load_ticket_types():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def show_browse_tickets():
    st.title("Browse Tickets")
    st.write("Select from the available ticket types below:")
    
    ticket_types = load_ticket_types()
    for ticket in ticket_types:
        st.subheader(ticket["name"])
        st.write(ticket["description"])
        if st.button("Order Now", key=ticket["name"]):
            st.session_state.current_page = "order_tickets"
            st.session_state.current_ticket_order = ticket["id"]
            st.rerun()

    st.divider()
        
    if st.button("Exit to Home"):
        st.session_state.current_page = "home"
        st.rerun()