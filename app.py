import streamlit as st
import pandas as pd

# Google Sheet published as CSV (publicly viewable)
csv_url = "https://docs.google.com/spreadsheets/d/1B_09WvM16z_jJ8HAZxu-v09AZCm5-5gmVmBjX4qznK8/export?format=csv"

# Load the CSV
@st.cache_data(ttl=60)  # Refresh every 60 seconds
def load_glossary():
    df = pd.read_csv(csv_url)
    df["Term"] = df["Term"].str.upper()
    return dict(zip(df["Term"], df["Definition"]))

glossary = load_glossary()

# UI
st.title("📘 Company Lingo Dictionary")
st.write("Type a term below to see its definition:")

term = st.text_input("Enter a term", "").strip().upper()

if term:
    definition = glossary.get(term)
    if definition:
        st.success(definition)
    else:
        st.error("Sorry, that term isn't in the glossary.")
