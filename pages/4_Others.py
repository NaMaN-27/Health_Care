import json
import streamlit as st
import math

from load_data import load_json_from_firebase

st.title("OTHER ITEMS")

# -----------------------------
# Load data
# -----------------------------
data = load_json_from_firebase()

items = data["Others"]

# -----------------------------
# Session state
# -----------------------------
if "others_selected" not in st.session_state:
    st.session_state.others_selected = []

# -----------------------------
# Layout config
# -----------------------------
ITEMS_PER_COLUMN = 10
num_cols = math.ceil(len(items) / ITEMS_PER_COLUMN)
columns = st.columns(num_cols)

selected = []

# -----------------------------
# Render checkboxes
# -----------------------------
for idx, item in enumerate(items):
    col_index = idx // ITEMS_PER_COLUMN
    with columns[col_index]:
        if st.checkbox(
            item,
            value=(item in st.session_state.others_selected),
            key=f"other_{item}"
        ):
            selected.append(item)

# -----------------------------
# Actions
# -----------------------------
def save_others():
    st.session_state.others_selected = selected
    st.success("Saved!")

def reset_others():
    for item in items:
        st.session_state[f"other_{item}"] = False
    st.session_state.others_selected = []
    st.rerun()

st.button("Save", on_click=save_others)
st.button("Reset", on_click=reset_others)
