import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# === Setup ===
SHEET_ID = "1B_09WvM16z_jJ8HAZxu-v09AZCm5-5gmVmBjX4qznK8"
CSV_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# === Load dictionary ===
dict_df = pd.read_csv(CSV_URL)

# === Streamlit UI ===
st.title("📘 ALC Dictionary")
query = st.text_input("Search for a term:")
if query:
    results = dict_df[dict_df['Term'].str.lower().str.contains(query.lower())]
    if not results.empty:
        for _, row in results.iterrows():
            st.write(f"**{row['Term']}**")
            st.write(f"{row['Definition']}")
    else:
        st.info("No matching term found.")

# === Submission form ===
st.markdown("---")
st.header("➕ Submit a New Term")

with st.form("submission_form"):
    name = st.text_input("Your Name")
    new_term = st.text_input("New Term")
    new_def = st.text_area("Definition")
    submitted = st.form_submit_button("Submit")
    if submitted and name and new_term and new_def:
        # Connect to Google Sheet
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("alc-dictionary-6d2b3856648e.json", scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key(SHEET_ID)
        ws = sheet.worksheet("Submissions")
        ws.append_row([name, new_term, new_def])
        st.success("✅ Submission received!")
