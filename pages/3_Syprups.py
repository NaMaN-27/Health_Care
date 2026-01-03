import json
import streamlit as st
import math

from load_data import load_json_from_firebase

st.title("SYRUPS")

# -----------------------------
# Load data
# -----------------------------
data = load_json_from_firebase()
syrups = data["Name of Syrup"]

# -----------------------------
# Session state
# -----------------------------
if "syrups_selected" not in st.session_state:
    st.session_state.syrups_selected = []

# -----------------------------
# Layout config
# -----------------------------
ITEMS_PER_COLUMN = 10
num_cols = math.ceil(len(syrups) / ITEMS_PER_COLUMN)
columns = st.columns(num_cols)

selected = []

# -----------------------------
# Render checkboxes
# -----------------------------
for idx, item in enumerate(syrups):
    col_index = idx // ITEMS_PER_COLUMN
    with columns[col_index]:
        if st.checkbox(
            item,
            value=(item in st.session_state.syrups_selected),
            key=f"syrup_{item}"
        ):
            selected.append(item)

# -----------------------------
# Actions
# -----------------------------
def save_syrups():
    st.session_state.syrups_selected = selected
    st.success("Saved!")

def reset_syrups():
    for item in syrups:
        st.session_state[f"syrup_{item}"] = False
    st.session_state.syrups_selected = []
    st.rerun()

st.button("Save", on_click=save_syrups)
st.button("Reset", on_click=reset_syrups)
