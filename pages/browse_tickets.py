import streamlit as st
from services.json_service import load_ticket_types

def show_browse_tickets():
    if st.button("Exit to Home"):
            st.switch_page(st.session_state.pages["home"])
    
    st.markdown(
        """
        <div class="title">
            <h1>Embark on your journey today!</h1>
            <p>Browse our available ticket types below.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    ticket_types = load_ticket_types()
    for ticket in ticket_types:
        st.subheader(ticket["name"])
        st.write(ticket["description"])
        if st.button("Order Now", key=ticket["name"]):
            st.session_state.current_ticket_order = ticket["id"]
            st.switch_page(st.session_state.pages["order_tickets"])

    st.divider()