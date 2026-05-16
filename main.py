import streamlit as st
from pathlib import Path
from pages.history import page_history

# import pages
from pages.trim_audio import page_trim
from pages.coming_soon import page_coming_soon
from pages.video_to_mp3 import page_video_to_mp3
from pages.audio_converter import page_audio_converter
from pages.frame_extractor import page_frame_extractor
from pages.youtube_downloader import page_youtube_downloader

# PAGE CONFIG
st.set_page_config(
    page_title="BeaconDream Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# GLOBAL CSS
def load_css():
    css_path = Path("assets/style.css")

    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )

load_css()

# MENU
MENUS = [
    "Trim Audio",
    "Video to MP3",
    "Audio Converter",
    "Frame Extractor",
    "YouTube Downloader",
    # "History",
]

ICONS = {
    "Trim Audio": "✂️",
    "Video to MP3": "🎬",
    "Audio Converter": "🔄",
    "Frame Extractor": "🎞️",
    "YouTube Downloader": "📥",
    "History": "🕘",
}

# SIDEBAR
with st.sidebar:
    st.markdown(
        '<div class="brand">BeaconDream<span>Studio</span></div>',
        unsafe_allow_html=True
    )

    selected = st.radio(
        "Menu",
        options=MENUS,
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        '<div style="font-size:.75rem;color:#6b7280">'
        'v1.0.0 — BeaconDream Studio'
        '</div>',
        unsafe_allow_html=True
    )

# ROUTER
if selected == "Trim Audio":
    page_trim()

elif selected == "Video to MP3":
    page_video_to_mp3()

elif selected == "Audio Converter":
    page_audio_converter()

elif selected == "Frame Extractor":
    page_frame_extractor()

elif selected == "YouTube Downloader":
    page_youtube_downloader()

elif selected == "History":
    page_history()

else:
    page_coming_soon(
        ICONS[selected],
        selected
    )