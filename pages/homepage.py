
import streamlit as st


def show_home():
    st.title("🎟️ TicketHub")
    st.subheader("Your next experience starts here!")

    st.write(
        "Discover events, explore experiences, and find your next favourite event."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Want to explore the park?")
        st.write("Go there now!")

    with col2:
         if st.button("Browse Tickets", use_container_width=True):
                st.session_state.current_page = "browse_tickets"
                st.rerun()



