import streamlit as st
import random

st.title("Streamlit Test App")
st.write("Your app is working!")

name = st.text_input("Enter your name")

if st.button("Say Hello"):
    st.success(f"Hello, {name}!")

number = st.slider("Choose a number", 1, 100, 50)
st.write(f"You selected {number}")

if st.button("Generate Random Number"):
    st.write(f"Random number: {random.randint(1, 100)}")
