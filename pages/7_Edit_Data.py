import streamlit as st
import json
import uuid

from load_data import load, save_json_to_firebase

st.set_page_config(layout="centered")

DATA_FILE = "data.json"

# -----------------------------
# Helpers
# -----------------------------
def load_data():
    try:
        data =load()
    except Exception as e:
        st.error("Failed to load data.json from Firebase")
        st.exception(e)
        st.stop()
    return data

def save_data(data):
    save_json_to_firebase(data)

data = load_data()

CATEGORY_MAP = {
    "Tablets": "Names of tablets",
    "Injections": "Name of injection",
    "Syrups": "Name of Syrup",
    "Others": "Others"
}

# -----------------------------
# UI
# -----------------------------
st.title("✏️ Edit Medicine List")

category = st.selectbox("Select category", CATEGORY_MAP.keys())
json_key = CATEGORY_MAP[category]

# -----------------------------
# Init session state (per category)
# -----------------------------
if (
    "edit_items" not in st.session_state
    or st.session_state.get("active_category") != json_key
):
    st.session_state.edit_items = [
        {"id": str(uuid.uuid4()), "name": x}
        for x in data[json_key]
    ]
    st.session_state.active_category = json_key

items = st.session_state.edit_items

st.divider()

# -----------------------------
# Edit + reorder list
# -----------------------------
for idx, item in enumerate(items):
    col1, col2, col3, col4 = st.columns([6, 1, 1, 1])

    with col1:
        item["name"] = st.text_input(
            "",
            value=item["name"],
            key=item["id"]
        )

    with col2:
        if st.button("⬆️", key=f"up_{item['id']}") and idx > 0:
            items[idx - 1], items[idx] = items[idx], items[idx - 1]
            st.rerun()

    with col3:
        if st.button("⬇️", key=f"down_{item['id']}") and idx < len(items) - 1:
            items[idx + 1], items[idx] = items[idx], items[idx + 1]
            st.rerun()

    with col4:
        if st.button("❌", key=f"del_{item['id']}"):
            items.pop(idx)
            st.rerun()

# -----------------------------
# Save
# -----------------------------
st.divider()

if st.button("💾 Save Changes"):
    data[json_key] = [x["name"] for x in items]
    save_data(data)
    st.success("Saved successfully ✅")
