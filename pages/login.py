import streamlit as st
from services.new_account_service import login_account
from services.validation_services import is_valid_email


def show_login():
    st.title("Log In")
    st.write("Welcome back to TicketHub!")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Log In")

        if submitted:
            valid_email, mssg_email = is_valid_email(email)
            if not email or not password:
                st.error("Please fill in all required fields.")
            elif not valid_email:
                st.error(mssg_email)
            else:
                success, message = login_account(email, password)
                if success:
                    st.session_state.current_account = email
                    st.session_state.current_page = "home"
                    st.rerun()
                else:
                    st.error(message)

    st.divider()

    if st.button("Don't have an account? Sign up"):
        st.session_state.current_page = "signup"
        st.rerun()
