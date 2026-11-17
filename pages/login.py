import streamlit as st

from services.new_account_service import login_account
from services.validation_service import is_valid_email

def show_login(): #Defining function for login page
    st.title("Log In")
    st.write("Welcome back to TicketHub!")

    with st.form("login_form"): #Taking input from the user
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Log In")

        if submitted: #Checking if the email structure is valid 
            valid_email = is_valid_email(email)
            if not email or not password:
                st.error("Please fill in all required fields.")
            elif not valid_email:
                st.error("Please enter a valid email address.")
            else:
                success, message = login_account(email, password)
                if success:
                    st.session_state.current_account = email
                    st.switch_page(st.session_state.pages["home"])
                else:
                    st.error(message)

    st.divider()

    if st.button("Don't have an account? Sign up"):
        st.switch_page(st.session_state.pages["signup"])
