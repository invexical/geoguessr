from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


ROOT = Path(__file__).parent

st.set_page_config(
    page_title="Crossroads Geo",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Streamlit secrets are injected into the HTML app. Firebase's web config and a
# Mapillary client token are browser-visible credentials; secure the Firebase
# database with the Firestore rules in firestore.rules and restrict tokens in
# their provider dashboards where possible.
mapillary_token = str(st.secrets.get("MAPILLARY_ACCESS_TOKEN", ""))
try:
    firebase_secrets = dict(st.secrets.get("firebase", {}))
except Exception:
    firebase_secrets = {}

firebase_config = {
    "apiKey": str(firebase_secrets.get("apiKey", "")),
    "authDomain": str(firebase_secrets.get("authDomain", "")),
    "projectId": str(firebase_secrets.get("projectId", "")),
    "appId": str(firebase_secrets.get("appId", "")),
    "messagingSenderId": str(firebase_secrets.get("messagingSenderId", "")),
}

config = {
    "mapillaryToken": mapillary_token,
    "firebase": firebase_config,
}

html_path = ROOT / "game.html"
if not html_path.exists():
    st.error("game.html was not found. Keep app.py and game.html in the same folder.")
    st.stop()

html = html_path.read_text(encoding="utf-8")
# Prevent a config value from accidentally terminating the script element.
config_json = json.dumps(config, ensure_ascii=False).replace("</", "<\\/")
html = html.replace("__APP_CONFIG__", config_json)

st.iframe(html, height=980, width="stretch")
