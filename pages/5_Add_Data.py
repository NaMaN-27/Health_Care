import streamlit as st
import json
import os

DATA_FILE = "data.json"

st.set_page_config(page_title="Add Data", layout="centered")
st.title("➕ Add Multiple Items")

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

st.write("Enter **one item per line**")

items_text = st.text_area(
    "Items",
    height=180,
    placeholder="Example:\nCrocin\nDolo 650\nAzithro"
)

# -----------------------------
# Save Logic
# -----------------------------
if st.button("Save All"):
    json_key = CATEGORY_MAP[category_ui]

    # Split lines → clean → unique
    new_items = [
        line.strip()
        for line in items_text.split("\n")
        if line.strip()
    ]

    if not new_items:
        st.warning("No valid items entered")
        st.stop()

    existing = set(data[json_key])
    added = []
    skipped = []

    for item in new_items:
        if item in existing:
            skipped.append(item)
        else:
            data[json_key].append(item)
            added.append(item)

    # Save only if something changed
    if added:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)

        st.success(f"✅ Added {len(added)} item(s)")

    if skipped:
        st.info(f"⚠️ Skipped duplicates: {', '.join(skipped)}")

    if added:
        st.rerun()
