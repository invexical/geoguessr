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

# Browser-side keys are visible to users. Restrict Google keys by HTTP referrer
# and API; protect Firebase writes with firestore.rules.
mapillary_token = str(st.secrets.get("MAPILLARY_ACCESS_TOKEN", "")).strip()
google_maps_api_key = str(st.secrets.get("GOOGLE_MAPS_API_KEY", "")).strip()
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
    "googleMapsApiKey": google_maps_api_key,
    "firebase": firebase_config,
}

html_path = ROOT / "game.html"
if not html_path.exists():
    st.error("game.html was not found. Keep geo_app.py and game.html in the same folder.")
    st.stop()

html = html_path.read_text(encoding="utf-8")
config_json = json.dumps(config, ensure_ascii=False).replace("</", r"<\/")
html = html.replace("__APP_CONFIG__", config_json)

st.iframe(html, height=1080, width="stretch")
