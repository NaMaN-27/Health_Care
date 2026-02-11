import streamlit as st
import json
import datetime
import firebase_admin
from firebase_admin import credentials,storage
from load_data import load_json_from_firebase


if not firebase_admin._apps:
    firebase_creds = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_creds)

    firebase_admin.initialize_app(cred, {
        "storageBucket": "jeswaniclinic-de930.firebasestorage.app"
    })



# Initialize expected session state keys if missing
for k in ("tablets_selected", "syrups_selected", "injections_selected", "others_selected"):
    if k not in st.session_state:
        st.session_state[k] = []

data = load_json_from_firebase()


tablets = data["Names of tablets"]

st.set_page_config(layout="centered")

# --------------------------------------
# HEADER — single line
# --------------------------------------
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
    <span style="font-size:28px; font-weight:800;">
      Jeswani Clinic
    </span>
    <span style="font-size:18px; font-weight:600;">
      Hirala Chowk, Beed
    </span>
  </div>

  <div style="font-size:18px; font-weight:400;">
    Mob No: 9890460700
  </div>

</div>
""", unsafe_allow_html=True)



# --------------------------------------
# ID + NAME + DATE
# --------------------------------------
col0, col1, col2 = st.columns([1, 2.5, 1])

with col0:
    patient_id = st.text_input("", placeholder="Patient ID")

with col1:
    name = st.text_input("", placeholder="Patient Name")

with col2:
    date = st.date_input("", value=datetime.date.today())

# --------------------------------------
# ADDRESS
# --------------------------------------
address = st.text_input("", placeholder="Address")

# --------------------------------------
# TWO COLUMNS FOR ITEMS (display only)
# --------------------------------------
left, right = st.columns([1.2, 1])

with left:
    selected_items = st.multiselect(
    "Select tablets:", 
    tablets, 
    max_selections=8,
    default=st.session_state.tablets_selected  # Keep previously selected items
    )
    st.session_state.tablets_selected  = selected_items
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)

    #if st.session_state.tablets_selected:
    #    for v in st.session_state.tablets_selected:
    #        st.write(f"• {v}")
    #else:
    #    st.write("No items selected.")

with right:
    if st.session_state.injections_selected:
        for v in st.session_state.injections_selected:
            st.write(f"• {v}")
    else:
        st.write("No items selected.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.session_state.others_selected:
        for v in st.session_state.others_selected:
            st.write(f"• {v}")
    else:
        st.write("No items selected.")

    st.markdown("<br><br>", unsafe_allow_html=True)

    if st.session_state.syrups_selected:
        for v in st.session_state.syrups_selected:
            st.write(f"• {v}")
    else:
        st.write("No items selected.")
