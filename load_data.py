import json
import streamlit as st
from firebase_admin import storage

@st.cache_data(show_spinner=False)
def load_json_from_firebase():
    bucket = storage.bucket()
    blob = bucket.blob("data.json")
    return json.loads(blob.download_as_text())


def save_json_to_firebase(data: dict):
    bucket = storage.bucket()
    blob = bucket.blob("data.json")
    blob.upload_from_string(
        json.dumps(data, indent=2),
        content_type="application/json"
    )
    # IMPORTANT: clear cache so all pages reload fresh data
    st.cache_data.clear()


def load():
    bucket = storage.bucket()
    blob = bucket.blob("data.json")
    return json.loads(blob.download_as_text())