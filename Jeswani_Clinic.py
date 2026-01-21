import streamlit as st
import datetime
import math

# Assuming you're loading data from Firebase for tablets, syrups, etc.
from load_data import load_json_from_firebase

# Fetch data from Firebase (or any source you're using)
data = load_json_from_firebase()

# Example: Get tablets, syrups, injections (you can repeat this for other categories)
tablets = data.get("Names of tablets", [])
syrups = data.get("Names of syrups", [])
injections = data.get("Names of injections", [])

# Initialize session state for each category if not already initialized
if "selected_tablets" not in st.session_state:
    st.session_state.selected_tablets = []
if "selected_syrups" not in st.session_state:
    st.session_state.selected_syrups = []
if "selected_injections" not in st.session_state:
    st.session_state.selected_injections = []

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

    # Render tablets dropdowns
    if st.session_state.selected_tablets:
        for idx, item in enumerate(st.session_state.selected_tablets):
            col1, col2 = st.columns([3, 1])  # Two columns: one for dropdown, one for remove button
            
            with col1:
                # Render a dropdown for each selected tablet
                selected_item = st.selectbox(
                    "",
                    tablets,
                    index=tablets.index(item) if item else 0,  # Keep the previously selected item
                    key=f"tablet_dropdown_{idx}"
                )
                # Update the item if the user selects something different
                st.session_state.selected_tablets[idx] = selected_item

            with col2:
                # Render a small cross button to remove the tablet row
                if st.button("❌", key=f"tablet_remove_{idx}"):
                    st.session_state.selected_tablets.pop(idx)
                    break  # Exit loop to refresh the UI immediately
    else:
        pass  # No "No items selected" in left column
    
    # Button to add more tablets dropdowns
    if st.button("Add more tablets"):
        st.session_state.selected_tablets.append(None)  # Add placeholder for next tablet dropdown

    # Render syrups dropdowns (same logic as tablets)
    if st.session_state.selected_syrups:
        for idx, item in enumerate(st.session_state.selected_syrups):
            col1, col2 = st.columns([3, 1])  # Two columns: one for dropdown, one for remove button
            
            with col1:
                selected_item = st.selectbox(
                    "",
                    syrups,
                    index=syrups.index(item) if item else 0,
                    key=f"syrup_dropdown_{idx}"
                )
                st.session_state.selected_syrups[idx] = selected_item

            with col2:
                if st.button("❌", key=f"syrup_remove_{idx}"):
                    st.session_state.selected_syrups.pop(idx)
                    break

    # Button to add more syrups dropdowns
    if st.button("Add more syrups"):
        st.session_state.selected_syrups.append(None)

    # Render injections dropdowns (same logic as tablets)
    if st.session_state.selected_injections:
        for idx, item in enumerate(st.session_state.selected_injections):
            col1, col2 = st.columns([3, 1])  # Two columns: one for dropdown, one for remove button
            
            with col1:
                selected_item = st.selectbox(
                    "",
                    injections,
                    index=injections.index(item) if item else 0,
                    key=f"injection_dropdown_{idx}"
                )
                st.session_state.selected_injections[idx] = selected_item

            with col2:
                if st.button("❌", key=f"injection_remove_{idx}"):
                    st.session_state.selected_injections.pop(idx)
                    break

    # Button to add more injections dropdowns
    if st.button("Add more injections"):
        st.session_state.selected_injections.append(None)

# -----------------------------
# RIGHT COLUMN - Display Items
# -----------------------------
with right:
    # Display tablets selected
    if st.session_state.selected_tablets:
        for v in st.session_state.selected_tablets:
            st.write(f"• {v}")
    else:
        st.write("No tablets selected.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Display syrups selected
    if st.session_state.selected_syrups:
        for v in st.session_state.selected_syrups:
            st.write(f"• {v}")
    else:
        st.write("No syrups selected.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Display injections selected
    if st.session_state.selected_injections:
        for v in st.session_state.selected_injections:
            st.write(f"• {v}")
    else:
        st.write("No injections selected.")
