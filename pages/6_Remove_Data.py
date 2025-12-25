import streamlit as st
import json
import os

DATA_FILE = "data.json"

st.set_page_config(page_title="Remove Data", layout="centered")
st.title("🗑 Remove Items")

# -----------------------------
# Load JSON
# -----------------------------
if not os.path.exists(DATA_FILE):
    st.error("data.json not found")
    st.stop()

with open(DATA_FILE, "r") as f:
    data = json.load(f)

# -----------------------------
# Category Mapping
# -----------------------------
CATEGORY_MAP = {
    "Tablet": "Names of tablets",
    "Injection": "Name of injection",
    "Syrup": "Name of Syrup",
    "Others": "Others"
}

# -----------------------------
# UI
# -----------------------------
category_ui = st.selectbox(
    "Select category",
    list(CATEGORY_MAP.keys())
)

json_key = CATEGORY_MAP[category_ui]
items = data.get(json_key, [])

if not items:
    st.info("No items found in this category")
    st.stop()

st.write("Select items to remove:")

selected_items = st.multiselect(
    "Items",
    options=items
)

# -----------------------------
# Remove Logic
# -----------------------------
if st.button("Remove Selected"):
    if not selected_items:
        st.warning("No items selected")
        st.stop()

    data[json_key] = [i for i in items if i not in selected_items]

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    st.success(f"✅ Removed {len(selected_items)} item(s)")
    st.rerun()
