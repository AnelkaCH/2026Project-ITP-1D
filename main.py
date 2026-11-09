import streamlit as st

# Importing the pages.
from pages.homepage import show_home
from pages.login import show_login
from pages.signup import show_signup
from pages.browse_tickets import show_browse_tickets
from pages.order_tickets import show_order_tickets
from pages.display_orders import show_display_orders

from ui.theme import apply_theme

st.set_page_config(
    page_title="Wunderbar - Ticket Hub",
    page_icon="🎟️",
    layout="wide"
)

home = st.Page(show_home, title="Home", icon=":material/home:", url_path="home")
login = st.Page(show_login, title="Login", icon=":material/login:", url_path="login")
signup = st.Page(show_signup, title="Sign up", icon=":material/person_add:", url_path="signup")
browse_tickets = st.Page(show_browse_tickets, title="Browse tickets", icon=":material/search:", url_path="browse")
order_tickets = st.Page(show_order_tickets, title="Order tickets", icon=":material/shopping_cart:", url_path="order")
display_orders = st.Page(show_display_orders, title="My orders", icon=":material/receipt_long:", url_path="orders")

# Initialize session state
if "current_account" not in st.session_state:
    st.session_state.current_account = None

if "current_ticket_order" not in st.session_state:
    st.session_state.current_ticket_order = None

# Keep the page objects so other files can switch pages
st.session_state.pages = {
    "signup": signup,
    "login": login,
    "home": home,
    "browse_tickets": browse_tickets,
    "order_tickets": order_tickets,
    "display_orders": display_orders,
}

# Only show pages that make sense for the user's login state
if st.session_state.current_account is None:
    pg = st.navigation([login, signup], position="hidden")
else:
    pg = st.navigation([home, browse_tickets, order_tickets, display_orders], position="hidden")
    with st.sidebar:
        if st.button("Log out"):
            st.session_state.clear()
            st.rerun()

apply_theme()
pg.run()
