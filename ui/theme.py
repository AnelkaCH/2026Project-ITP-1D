import streamlit as st

'''
Creates CSS styling
'Cinzel' is priorized as the primary font for headers
.title is the title class with following attributes
headers within style class gets different colour and margins 
'''

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&display=swap');

h1, h2, h3 {
    font-family: 'Cinzel', Georgia, serif;
}

.title {
    text-align: center;
    padding: 2.5rem 1.5rem;
    border-radius: 20px;
    background: #F7F1E3;
    border: 1px solid #E3D6B8;
    margin-bottom: 2rem;
}
.title h1 { margin: 0; color: #2F5D50; }
.title p { margin: 0.5rem 0 0 0; color: #6B5A45; }
</style>
"""

# Turns CSS into HTML
def apply_theme():
    st.markdown(CSS, unsafe_allow_html=True)