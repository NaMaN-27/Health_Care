import streamlit as st
import datetime
import firebase_admin
from firebase_admin import credentials, storage
from load_data import load_json_from_firebase


# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(layout="centered")

# ---------------------------------------------------
# WHITE MULTISELECT + BUTTON STYLE
# ---------------------------------------------------
st.markdown("""
<style>

/* Multiselect box */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
    border: 1px solid #ccc !important;
    border-radius: 8px !important;
}

/* Text inside */
div[data-baseweb="select"] * {
    color: black !important;
}

/* Dropdown menu */
div[data-baseweb="popover"] {
    background-color: white !important;
    color: black !important;
}

/* Hover option */
li[role="option"]:hover {
    background-color: #f2f2f2 !important;
}

/* Button style */
div.stButton > button {
    background-color: white;
    color: black;
    border: 1px solid #ccc;
    border-radius: 6px;
    height: 38px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# FIREBASE INIT
# ---------------------------------------------------
if not firebase_admin._apps:
    firebase_creds = dict(st.secrets["firebase"])
    cred = credentials.Certificate(firebase_creds)
    firebase_admin.initialize_app(cred, {
        "storageBucket": "jeswaniclinic-de930.firebasestorage.app"
    })

data = load_json_from_firebase()

tablets = data["Names of tablets"]
injections = data["Name of injection"]
syrups = data["Name of Syrup"]
others = data["Others"]


# ---------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------
keys = [
    "tablets_selected", "injections_selected",
    "syrups_selected", "others_selected",
    "final_tablets", "final_injections",
    "final_syrups", "final_others"
]

for k in keys:
    if k not in st.session_state:
        st.session_state[k] = []


# ---------------------------------------------------
# CALLBACK FUNCTIONS
# ---------------------------------------------------
def add_items(selected_key, final_key):
    for item in st.session_state[selected_key]:
        if item not in st.session_state[final_key]:
            st.session_state[final_key].append(item)
    st.session_state[selected_key] = []


# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center;">
  <div>
    <span style="font-size:28px; font-weight:800;">Jeswani Clinic</span>
    <span style="font-size:18px; font-weight:600; margin-left:10px;">
      Hirala Chowk, Beed
    </span>
  </div>
  <div style="font-size:18px;">
    Mob No: 9890460700
  </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# PATIENT DETAILS
# ---------------------------------------------------
col0, col1, col2 = st.columns([1, 2.5, 1])

with col0:
    patient_id = st.text_input("", placeholder="Patient ID")

with col1:
    name = st.text_input("", placeholder="Patient Name")

with col2:
    date = st.date_input("", value=datetime.date.today())

address = st.text_input("", placeholder="Address")


# ---------------------------------------------------
# MEDICINE SECTION FUNCTION
# ---------------------------------------------------
def medicine_section(options, selected_key, final_key, button_key):

    col1, col2 = st.columns([4, 1])

    with col1:
        st.multiselect(
            "",
            options,
            key=selected_key,
            label_visibility="hidden",
            placeholder=""
        )

    with col2:
        st.write("")
        st.button(
            "A",
            key=button_key,
            on_click=add_items,
            args=(selected_key, final_key)
        )

    # Show final list
    for item in st.session_state[final_key]:
        st.write("•", item)


# ---------------------------------------------------
# TWO COLUMN LAYOUT
# ---------------------------------------------------
left, right = st.columns([1.2, 1])

with left:
    medicine_section(tablets, "tablets_selected", "final_tablets", "btn_tab")

with right:
    medicine_section(injections, "injections_selected", "final_injections", "btn_inj")
    st.markdown("<br>", unsafe_allow_html=True)
    medicine_section(syrups, "syrups_selected", "final_syrups", "btn_syr")
    st.markdown("<br>", unsafe_allow_html=True)
    medicine_section(others, "others_selected", "final_others", "btn_oth")