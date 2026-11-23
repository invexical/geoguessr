from __future__ import annotations

import base64
import json
from pathlib import Path

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

# Browser-side keys are visible to users. Restrict Google keys by HTTP referrer
# and API; protect Firebase writes with firestore.rules.
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

# game.html may live in static/ (current repo layout) or next to this file.
html_path = next(
    (p for p in (ROOT / "static" / "game.html", ROOT / "game.html") if p.is_file()),
    None,
)
if html_path is None:
    st.error("game.html was not found. Put it in the static/ folder (or beside geo_app.py).")
    st.stop()

html = html_path.read_text(encoding="utf-8")

# Inject the config as base64 so quotes, "</script>" or unicode in a secret can
# never break the page. This is the same inline approach that worked before; it
# does not depend on Streamlit static file serving or on any URL path.
placeholder = "__APP_CONFIG_B64__"
if placeholder not in html:
    st.error(
        f"{html_path.name} does not contain the {placeholder} placeholder. "
        "Make sure you uploaded the newest game.html."
    )
    st.stop()

config_b64 = base64.b64encode(json.dumps(config, ensure_ascii=False).encode("utf-8")).decode("ascii")
html = html.replace(placeholder, config_b64)

st.iframe(html, height=1080, width="stretch")
