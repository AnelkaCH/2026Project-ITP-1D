import streamlit as st
from services.json_service import load_ticket_types

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