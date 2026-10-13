import streamlit as st
from services.new_account_service import register_account
from services.validation_services import is_valid_email, is_valid_password

def show_signup():
    st.title("Create an Account")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submitted = st.form_submit_button("Sign Up")

    if submitted:
        valid_email, mssg_email = is_valid_email(email)
        valid_password, mssg_password = is_valid_password(password)

        if not email or not password or not confirm_password:
            st.error("Please fill in all required fields.")


        elif not valid_email:
            st.error(mssg_email)

        elif password != confirm_password:
            st.error("Passwords do not match.")

        elif not valid_password:
            st.error(mssg_password)

        else:
            success, message = register_account(
                email,
                password
            )

            if success:
                st.success(message)
            else:
                st.error(message)

    st.divider()
    
    if st.button("Already have an account? Log in"):
        st.session_state.current_page = "login"
        st.rerun()
