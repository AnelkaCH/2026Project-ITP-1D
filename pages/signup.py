import streamlit as st
from services.new_account_service import register_account


def show_signup():
    st.title("Create an Account")

    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input(
            "Password",
            type="password"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submitted = st.form_submit_button("Sign Up")

    if submitted:
        if not email.strip():
            st.error("Please fill in all required fields.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        elif not password:
            st.error("Password cannot be empty.")

        else:
            success, message = register_account(
                email.strip(),
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
