import json
import streamlit as st
import math

st.title("TABLETS")

# -----------------------------
# Load data
# -----------------------------
with open("data.json", "r") as f:
    data = json.load(f)

tablets = data["Names of tablets"]

# -----------------------------
# Session state
# -----------------------------
if "tablets_selected" not in st.session_state:
    st.session_state.tablets_selected = []

# -----------------------------
# Layout config
# -----------------------------
ITEMS_PER_COLUMN = 10
num_cols = math.ceil(len(tablets) / ITEMS_PER_COLUMN)
columns = st.columns(num_cols)

selected = []

# -----------------------------
# Render checkboxes
# -----------------------------
for idx, t in enumerate(tablets):
    col_index = idx // ITEMS_PER_COLUMN
    with columns[col_index]:
        if st.checkbox(
            t,
            value=(t in st.session_state.tablets_selected),
            key=f"tablet_{t}"
        ):
            selected.append(t)

# -----------------------------
# Actions
# -----------------------------
def save_tablets():
    st.session_state.tablets_selected = selected
    st.success("Saved!")

def reset_tablets():
    for t in tablets:
        st.session_state[f"tablet_{t}"] = False
    st.session_state.tablets_selected = []
    st.rerun()

st.button("Save", on_click=save_tablets)
st.button("Reset", on_click=reset_tablets)
