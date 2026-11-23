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

# ---------------------------------------------------------------------------
# Guard: /app/static/* only exists when static serving is switched on.
# If it is off, Streamlit answers that URL with its own app shell, so the
# iframe would load Streamlit inside itself and spin forever.
# ---------------------------------------------------------------------------
if not st.get_option("server.enableStaticServing"):
    st.error(
        "Static file serving is turned off, so the game page cannot be loaded.\n\n"
        "Create `.streamlit/config.toml` in your repository with:\n\n"
        "```toml\n[server]\nenableStaticServing = true\n```\n\n"
        "Then reboot the app (this setting is only read at server start)."
    )
    st.stop()

game_path = ROOT / "static" / "game.html"
if not game_path.is_file():
    st.error("static/game.html was not found. Keep the static folder beside this file.")
    st.stop()

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

config_json = json.dumps(config, ensure_ascii=False, separators=(",", ":"))
fragment = urlencode({"config": config_json})
iframe_url = f"/app/static/game.html#{fragment}"

# Keep this as a real same-origin document (not inline HTML / srcdoc) so Google's
# HTTP-referrer key restrictions see your streamlit.app URL.
# st.iframe has no `alt` argument; passing one raises a TypeError.
if hasattr(st, "iframe"):
    st.iframe(iframe_url, height=850, width="stretch")
else:  # older Streamlit releases
    import streamlit.components.v1 as components

    components.iframe(iframe_url, height=850)
