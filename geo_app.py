from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st

ROOT = Path(__file__).parent

st.set_page_config(
    page_title="Crossroads Geo",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# These values are used by the browser game. Browser-side Maps and Mapillary
# tokens are visible to visitors, so restrict them in their provider dashboards.
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

# IMPORTANT: Do not pass HTML text to st.iframe(). Streamlit embeds HTML text
# using srcdoc, which gives the frame an `about:srcdoc` URL. Google Maps HTTP
# referrer restrictions cannot reliably authorize that opaque URL. Instead,
# serve the trusted game file from Streamlit's HTTPS static-file endpoint.
game_path = ROOT / "static" / "game.html"
if not game_path.is_file():
    st.error(
        "static/game.html was not found. Keep the static folder beside geo_app.py "
        "and enable static serving in .streamlit/config.toml."
    )
    st.stop()

config_json = json.dumps(config, ensure_ascii=False, separators=(",", ":"))
# Put configuration in the URL fragment, not the HTTP query string. The
# fragment is read by the browser but is not sent to Streamlit's static server.
fragment = urlencode({"config": config_json})
iframe_url = f"/app/static/game.html#{fragment}"

st.iframe(
    iframe_url,
    height=1080,
    width="stretch",
    alt="Crossroads Geo interactive geography game",
)
