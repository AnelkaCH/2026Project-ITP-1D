import streamlit as st

'''
Creates CSS styling
'Cinzel' is priorized as the primary font for headers
.title is the title class with following attributes
headers within style class gets different colour and margins 
'''

CSS = """
<style>
/* Load the Cinzel font from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&display=swap');

/* All headings use Cinzel (Georgia / serif as fallbacks) */
h1, h2, h3 {
    font-family: 'Cinzel', Georgia, serif;
}

/* Cream banner box used for the Browse Tickets page title */
.title {
    text-align: center;
    padding: 2.5rem 1.5rem;
    border-radius: 20px;
    background: #F7F1E3;
    border: 1px solid #E3D6B8;
    margin-bottom: 2rem;
}

/* Banner heading: dark green, no extra spacing */
.title h1 {
    margin: 0;
    color: #2F5D50;
}

/* Banner subtitle text under the heading */
.title p {
    margin: 0.5rem 0 0 0;
    color: #6B5A45;
    font-size: 1.05rem;
}

/* Main page area: cap the width and add space at the top */
.block-container {
    max-width: 1200px;
    padding-top: 3rem;
}

/* Images fill their column at a fixed height without being cropped */
.stImage img {
    width: 100%;
    height: 200px;
    object-fit: contain;
    border-radius: 10px;
}

/* Subheaders inside containers (e.g. ticket cards) are dark green */
[data-testid="stVerticalBlockBorderWrapper"] h3 {
    color: #2F5D50;
}

/* Buttons: dark green with white text and rounded corners */
.stButton button {
    background-color: #2F5D50;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s ease;
}

/* Buttons turn a lighter green on hover */
.stButton button:hover {
    background-color: #477C69;
    color: white;
}

/* Carousel: a one-cell grid, so every slide sits in the same spot, stacked */
.st-key-carousel {
    display: grid;
    grid-template-columns: minmax(0, 1fr);  /* one full-width column */
}

/* Put every slide in that single cell */
.st-key-carousel > * {
    grid-area: 1 / 1;
    width: 100%;
}

/* Slides are invisible by default; homepage.py sets opacity: 1 on the current one.
   The transition makes the old slide fade out while the new one fades in. */
[class*="st-key-slide_"] {
    opacity: 0;
    transition: opacity 0.8s ease-in-out;
}

/* Carousel images are taller than card images, with square corners */
.st-key-carousel .stImage img {
    height: 500px;
    background: #F7F1E3;
    border-radius: 0;
}

/* Phone-sized screens: less padding and smaller title / images */
@media (max-width: 640px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .title {
        padding: 2rem 1rem;
    }

    .title h1 {
        font-size: 1.7rem;
    }

    .stImage img {
        height: 180px;
    }

    .st-key-carousel .stImage img {
        height: 260px;
    }
}

</style>
"""

# Turns CSS into HTML
def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)