import json
import streamlit as st
import math

st.title("INJECTIONS")

# -----------------------------
# Load data
# -----------------------------
with open("data.json", "r") as f:
    data = json.load(f)

injections = data["Name of injection"]

# -----------------------------
# Session state
# -----------------------------
if "injections_selected" not in st.session_state:
    st.session_state.injections_selected = []

# -----------------------------
# Layout config
# -----------------------------
ITEMS_PER_COLUMN = 10
num_cols = math.ceil(len(injections) / ITEMS_PER_COLUMN)
columns = st.columns(num_cols)

selected = []

# -----------------------------
# Render checkboxes
# -----------------------------
for idx, item in enumerate(injections):
    col_index = idx // ITEMS_PER_COLUMN
    with columns[col_index]:
        if st.checkbox(
            item,
            value=(item in st.session_state.injections_selected),
            key=f"injection_{item}"
        ):
            selected.append(item)

# -----------------------------
# Actions
# -----------------------------
def save_injections():
    st.session_state.injections_selected = selected
    st.success("Saved!")

def reset_injections():
    for item in injections:
        st.session_state[f"injection_{item}"] = False
    st.session_state.injections_selected = []
    st.rerun()

st.button("Save", on_click=save_injections)
st.button("Reset", on_click=reset_injections)
