import streamlit as st
import hashlib
import os

from services.new_account_service import register_account
from services.validation_service import (
    is_valid_email, 
    is_valid_password
)

def show_signup():
    st.title("Create an Account")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Sign Up")

    if submitted:
        valid_email = is_valid_email(email)
        valid_password, mssg_password = is_valid_password(password)

        if not email or not password or not confirm_password:
            st.error("Please fill in all required fields.")


        elif not valid_email:
            st.error("Invalid email format. Please enter a valid email address.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        elif not valid_password:
            st.error(mssg_password)

        else:
            salt = os.urandom(32)
            hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            success, message = register_account(email, hashed_password.hex(), salt.hex())

            if success:
                st.success(message)
            else:
                st.error(message)

    st.divider()
    
    if st.button("Already have an account? Log in"):
        st.switch_page(st.session_state.pages["login"])
