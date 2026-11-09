import streamlit as st

from services.json_service import load_ticket_types

def show_browse_tickets():
    # Creates button to switch to home
    if st.button("Exit to Home"):
            st.switch_page(st.session_state.pages["home"])
    
    # After login, produces landing page with title
    st.markdown(
        """
        <div class="title">
            <h1>Embark on your journey today!</h1>
            <p>Browse our available ticket types below.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # loads different ticket types
    ticket_types = load_ticket_types()
    
    # loops each different ticket type's name and lists it down on the page
    for ticket in ticket_types:
        st.subheader(ticket["name"])
        st.write(ticket["description"])
        # Button has a key to indicate uniqueness in the case of duplicate buttons of same name
        if st.button("Order Now", key=ticket["name"]):
            # Creates some space in memory to save ticket selection of the user and goes back to the order ticket page
            st.session_state.current_ticket_order = ticket["id"]
            st.switch_page(st.session_state.pages["order_tickets"])

    st.divider()