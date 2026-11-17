
import streamlit as st
from services.json_service import load_ticket_types

def show_browse_tickets():

    # Exit button
    if st.button("← Exit to Home"):
        st.switch_page(st.session_state.pages["home"])

    # Page title
    st.markdown(
        """
        <div class="title">
            <h1>Embark on your journey today!</h1>
            <p>Discover the perfect pass for your next adventure.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Load ticket types
    ticket_types = load_ticket_types()

    # Display tickets in rows of two
    for i in range(0, len(ticket_types), 2):

        cols = st.columns(2, gap="medium")

        for j, col in enumerate(cols):

            index = i + j

            if index >= len(ticket_types):
                break

            ticket = ticket_types[index]

            with col:
                # height="stretch" makes every card in the row match the tallest one
                with st.container(border=True, height="stretch"):

                    st.image(
                        f"static/images/{ticket['image']}",
                        width="stretch"
                    )

                    st.subheader(ticket["name"])

                    st.write(ticket["description"])

                    # Fill leftover space so the buttons line up at the bottom
                    st.space("stretch")

                    if st.button(
                        "Order Now",
                        key=f"order_{ticket['id']}",
                        width="stretch"
                    ):
                        st.session_state.current_ticket_order = ticket["id"]
                        st.switch_page(
                            st.session_state.pages["order_tickets"]
                        )

