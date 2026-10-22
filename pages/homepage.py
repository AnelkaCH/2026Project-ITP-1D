import streamlit as st
from services.json_service import load_accounts

def show_home():
    st.markdown(
        """
        <div class="title">
            <div style="font-size: 3rem;">🏰</div>
            <h1>Welcome to Wunderbar</h1>
            <p>Your next adventure starts here!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Want to explore the park?")
        st.write("Go there now!")

    with col2:
        if st.button("Browse Tickets", use_container_width=True):
            st.switch_page(st.session_state.pages["browse_tickets"])

    st.subheader("Already bought tickets? View your orders!")
    
    users=load_accounts()
    for user in users:
        if user["email"] == st.session_state.current_account:
            
            if not user["tickets"]:
                st.write("You have no ticket orders yet.")

            for i, ticket in enumerate(user["tickets"]):
                st.write(f"**{ticket['type']}**")
                st.write(f"Time of Order: {ticket['time_of_order']}")
                st.write(f"Date of Planned Visit: {ticket['date_of_visit']}")

                if st.button("See More", key=f"see_more_{i}"):
                    st.session_state.selected_ticket = i
                    st.switch_page(st.session_state.pages["display_orders"])

                st.divider()

            break



