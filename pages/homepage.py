from services.json_service import load_accounts

from pathlib import Path
import time

import streamlit as st

CAROUSEL_DIR = Path("static/images/carousel")
IMAGES = sorted(CAROUSEL_DIR.glob("*.jpg"))
SLIDE_SECONDS = 5  # how long each slide stays before auto-advancing


def change_slide(step):
    # Move forward (+1) or back (-1), wrapping around at either end
    st.session_state.carousel_index = (
        st.session_state.carousel_index + step
    ) % len(IMAGES)
    # Restart the timer so a manual click gets a full slide duration
    st.session_state.carousel_last_change = time.time()


# A fragment reruns on its own every SLIDE_SECONDS without reloading the rest of the page
@st.fragment(run_every=SLIDE_SECONDS)
def show_carousel():
    if not IMAGES:
        return

    if "carousel_index" not in st.session_state:
        st.session_state.carousel_index = 0
        st.session_state.carousel_last_change = time.time()

    # Auto-advance once enough time has passed since the last change
    # (0.5s of slack so the timer's tick isn't missed by a few milliseconds)
    if time.time() - st.session_state.carousel_last_change >= SLIDE_SECONDS - 0.5:
        change_slide(1)

    index = st.session_state.carousel_index

    # Every slide is always on the page, stacked on top of each other (see theme.py),
    # so all images are already loaded and nothing has to download mid-fade
    with st.container(key="carousel"):
        for i, image in enumerate(IMAGES):
            with st.container(key=f"slide_{i}"):
                st.image(str(image), width="stretch")

    # Make only the current slide visible; the CSS transition crossfades the change
    st.html(f"<style>.st-key-slide_{index} {{ opacity: 1; }}</style>")

    # Controls: previous button, position dots, next button
    with st.container(horizontal=True, horizontal_alignment="center", vertical_alignment="center"):
        st.button(":material/chevron_left:", key="carousel_prev", on_click=change_slide, args=(-1,))
        dots = " ".join("●" if i == index else "○" for i in range(len(IMAGES)))
        st.markdown(dots)
        st.button(":material/chevron_right:", key="carousel_next", on_click=change_slide, args=(1,))

def show_home():
    show_carousel()
    
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Want to explore the park?")
        st.write("Go there now!")

    with col2:
        if st.button("Browse Tickets", width="stretch"):
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



