import streamlit as st
import datetime
import math

# Assuming you're loading data from Firebase for tablets, syrups, etc.
from load_data import load_json_from_firebase

# Fetch data from Firebase (or any source you're using)
data = load_json_from_firebase()

# Example: Get tablets list (you can repeat this for syrups, injections, etc.)
tablets = data.get("Names of tablets", [])

# Initialize session state for items if not already initialized
if "selected_items" not in st.session_state:
    st.session_state.selected_items = []

# Layout configuration
st.set_page_config(layout="centered")

# -----------------------------
# HEADER — single line
# -----------------------------
st.markdown("""
<style>
@page {
  size: A5;
  margin: 10mm;
}
@media print {
  section.main > div {
    width: 148mm !important;
  }
}
</style>

<div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
  <div style="display:flex; align-items:baseline; gap:10px;">
    <span style="font-size:28px; font-weight:800;">Jeswani Clinic</span>
    <span style="font-size:18px; font-weight:600;">Hirala Chowk, Beed</span>
  </div>
  <div style="font-size:18px; font-weight:400;">Mob No: 9890460700</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# ID + NAME + DATE
# -----------------------------
col0, col1, col2 = st.columns([1, 2.5, 1])

with col0:
    patient_id = st.text_input("", placeholder="Patient ID")

with col1:
    name = st.text_input("", placeholder="Patient Name")

with col2:
    date = st.date_input("", value=datetime.date.today())

# -----------------------------
# Address
# -----------------------------
address = st.text_input("", placeholder="Address")

# -----------------------------
# LEFT COLUMN - Dropdown and Plus Button
# -----------------------------
left, right = st.columns([1.2, 1])

with left:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    # Initialize or load selected items
    if "selected_items" not in st.session_state:
        st.session_state.selected_items = []

    # Show the current selected items
    if st.session_state.selected_items:
        st.write("Currently selected items:")
        for idx, item in enumerate(st.session_state.selected_items):
            # Create a dropdown for each item
            selected_item = st.selectbox(
                f"Select item {idx + 1}", tablets, key=f"dropdown_{idx}"
            )
            
            # If the item is selected, update the session state
            if selected_item and selected_item != item:
                st.session_state.selected_items[idx] = selected_item

            # Create a cross (remove) button next to each dropdown
            if st.button(f"❌", key=f"remove_{idx}"):
                st.session_state.selected_items.pop(idx)
                st.experimental_rerun()  # Rerun to update the UI without the removed item

    else:
        st.write("No items selected.")

    # Button to add more dropdowns
    if st.button("Add more"):
        st.session_state.selected_items.append(None)  # Add placeholder for next dropdown

# -----------------------------
# RIGHT COLUMN - Display Items
# -----------------------------
with right:
    # Display tablets selected
    if st.session_state.tablets_selected:
        for v in st.session_state.tablets_selected:
            st.write(f"• {v}")
    else:
        st.write("No items selected.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Display injections selected
    if st.session_state.injections_selected:
        for v in st.session_state.injections_selected:
            st.write(f"• {v}")
    else:
        st.write("No items selected.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Display others selected
    if st.session_state.others_selected:
        for v in st.session_state.others_selected:
            st.write(f"• {v}")
    else:
        st.write("No items selected.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Display syrups selected
    if st.session_state.syrups_selected:
        for v in st.session_state.syrups_selected:
            st.write(f"• {v}")
    else:
        st.write("No items selected.")
