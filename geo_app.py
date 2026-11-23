from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlencode

import streamlit as st

ROOT = Path(__file__).parent

st.set_page_config(
    page_title="World Guesser",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Give the embedded game the full Streamlit viewport.
st.markdown(
    """
    <style>
      [data-testid="stHeader"], [data-testid="stToolbar"], footer {visibility:hidden;height:0;}
      [data-testid="stAppViewContainer"] > .main {padding-top:0!important;}
      .block-container {max-width:100%!important;padding:0!important;margin:0!important;}
      iframe {display:block;width:100%!important;height:100vh!important;min-height:560px;border:0;}
      [data-testid="stElementContainer"]:has(iframe) {margin:0!important;padding:0!important;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Browser-side provider keys are visible to visitors. Restrict the Google key
# by HTTP referrer and API in Google Cloud; Firebase writes are protected by rules.
mapillary_token = str(st.secrets.get("MAPILLARY_ACCESS_TOKEN", "")).strip()
google_maps_api_key = str(st.secrets.get("GOOGLE_MAPS_API_KEY", "")).strip()
try:
    firebase_secrets = dict(st.secrets.get("firebase", {}))
except Exception:
    firebase_secrets = {}

config = {
    "mapillaryToken": mapillary_token,
    "googleMapsApiKey": google_maps_api_key,
    "firebase": {
        "apiKey": str(firebase_secrets.get("apiKey", "")),
        "authDomain": str(firebase_secrets.get("authDomain", "")),
        "projectId": str(firebase_secrets.get("projectId", "")),
        "appId": str(firebase_secrets.get("appId", "")),
        "messagingSenderId": str(firebase_secrets.get("messagingSenderId", "")),
    },
}

# Keep this as a real static HTTPS document. Do NOT inline the HTML in st.iframe:
# that creates an about:srcdoc document, which breaks Google HTTP-referrer restrictions.
game_path = ROOT / "game.html"
if not game_path.is_file():
    st.error("game.html was not found. Keep the static folder beside this file.")
    st.stop()

config_json = json.dumps(config, ensure_ascii=False, separators=(",", ":"))
fragment = urlencode({"config": config_json})
iframe_url = f"/app/static/game.html#{fragment}"

st.iframe(
    iframe_url,
    height=850,
    width="stretch",
    alt="World Guesser interactive geography game",
)
