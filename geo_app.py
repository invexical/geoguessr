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
    config_json = json.dumps(config, ensure_ascii=False).replace("</", r"<\/")
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

# Inject the configuration into the HTML.
html = html_path.read_text(encoding="utf-8")
html = html.replace("__APP_CONFIG__", config_json)

# Serve the game as an actual HTML file, not an iframe srcdoc.
static_dir = ROOT / "static"
static_dir.mkdir(parents=True, exist_ok=True)

served_html_path = static_dir / "crossroads_geo.html"
served_html_path.write_text(html, encoding="utf-8")

# Embed the actual URL of the HTML file.
st.iframe(
    "app/static/crossroads_geo.html",
    height=1080,
    width="stretch",
)
