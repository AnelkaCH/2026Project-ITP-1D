
import streamlit as st

# Importing the pages.
from pages.homepage import show_home
from pages.login import show_login
from pages.signup import show_signup
from pages.browse_tickets import show_browse_tickets
from pages.order_tickets import show_order_tickets

st.set_page_config(
    page_title="TicketHub",
    page_icon="🎟️",
    layout="wide"
)

# Initialize the current screen
if "current_page" not in st.session_state:
    st.session_state.current_page = "signup"

if "current_ticket_order" not in st.session_state:
    st.session_state.current_ticket_order = None

# Route to the selected screen
page = st.session_state.current_page

if page == "home":
    show_home()
elif page == "login":
    show_login()
elif page == "signup":
    show_signup()
elif page == "browse_tickets":
    show_browse_tickets()
elif page == "order_tickets":
    show_order_tickets()
else:
    st.session_state.current_page = "home"
    st.rerun()
