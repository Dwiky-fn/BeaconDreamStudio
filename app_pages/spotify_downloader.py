from pathlib import Path
import tempfile

import streamlit as st
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL

from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = st.secrets[
    "SPOTIFY_CLIENT_ID"
]

SPOTIFY_CLIENT_SECRET = st.secrets[
    "SPOTIFY_CLIENT_SECRET"
]

SPOTIFY_CLIENT_ID = os.getenv(
    "SPOTIFY_CLIENT_ID"
)

SPOTIFY_CLIENT_SECRET = os.getenv(
    "SPOTIFY_CLIENT_SECRET"
)

def get_spotify_track(url):

    auth_manager = SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET
    )

    sp = spotipy.Spotify(
        auth_manager=auth_manager
    )

    track = sp.track(url)

    title = track["name"]

    artist = track["artists"][0]["name"]

    return f"{title} {artist}"


def download_mp3(query, output_dir):

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(
            output_dir / "%(title)s.%(ext)s"
        ),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "default_search": "ytsearch1"
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            query,
            download=True
        )

        title = info["entries"][0]["title"]

    return title


def page_spotify_downloader():

    st.markdown(
        '<div class="page-title">'
        '🎵 Spotify Downloader'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Download lagu Spotify sebagai MP3.'
        '</div>',
        unsafe_allow_html=True
    )

    url = st.text_input(
        "Spotify URL",
        placeholder="https://open.spotify.com/track/..."
    )

    if not url:
        return

    if st.button(
        "⬇️ Download MP3",
        use_container_width=True
    ):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            try:

                with st.spinner(
                    "Mengambil metadata Spotify..."
                ):

                    query = get_spotify_track(url)

                st.info(
                    f"🎵 Ditemukan: {query}"
                )

                with st.spinner(
                    "Mencari di YouTube..."
                ):

                    download_mp3(
                        query,
                        temp_dir
                    )

                files = list(
                    temp_dir.glob("*.mp3")
                )

                if not files:

                    st.error(
                        "MP3 tidak ditemukan."
                    )

                    return

                file_path = files[0]

                with open(file_path, "rb") as f:
                    audio_bytes = f.read()

                st.success(
                    "✅ Lagu berhasil didownload!"
                )

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

                st.download_button(
                    label="⬇️ Download MP3",
                    data=audio_bytes,
                    file_name=file_path.name,
                    mime="audio/mp3",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"Gagal download: {e}"
                )