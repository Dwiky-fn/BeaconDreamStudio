from pathlib import Path
import tempfile
import requests

import streamlit as st
from yt_dlp import YoutubeDL

from utils.history_manager import add_history


def get_spotify_metadata(url):

    endpoint = (
        "https://open.spotify.com/oembed"
    )

    response = requests.get(
        endpoint,
        params={"url": url}
    )

    if response.status_code != 200:

        raise Exception(
            "Gagal mengambil metadata Spotify."
        )

    data = response.json()

    return {
        "title": data.get("title"),
        "artist": data.get("author_name"),
        "thumbnail": data.get("thumbnail_url")
    }


def download_mp3(query, output_dir):

    ydl_opts = {

        # AUDIO FORMAT
        "format": "bestaudio/best",

        # OUTPUT
        "outtmpl": str(
            output_dir / "%(title)s.%(ext)s"
        ),

        # SEARCH
        "default_search": "ytsearch1",

        # BETTER CLOUD SUPPORT
        "quiet": True,
        "noplaylist": True,
        "geo_bypass": True,
        "nocheckcertificate": True,

        # YOUTUBE FIX
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },

        # MP3 CONVERT
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            query,
            download=True
        )

        if "entries" in info:

            video_info = info["entries"][0]

        else:

            video_info = info

        return {
            "title": video_info.get("title"),
            "duration": video_info.get("duration"),
            "uploader": video_info.get("uploader")
        }


def format_duration(seconds):

    if not seconds:
        return "Unknown"

    minutes = seconds // 60
    seconds = seconds % 60

    return f"{minutes}:{seconds:02d}"


def page_spotify_downloader():

    st.markdown(
        '<div class="page-title">'
        '🎵 Spotify Downloader'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Download lagu Spotify menjadi MP3.'
        '</div>',
        unsafe_allow_html=True
    )

    # URL INPUT
    st.markdown(
        '<div class="card-title">'
        '① Spotify URL'
        '</div>',
        unsafe_allow_html=True
    )

    url = st.text_input(
        "Spotify URL",
        placeholder=(
            "https://open.spotify.com/track/..."
        )
    )

    if not url:
        return

    st.markdown("---")

    # GET SPOTIFY METADATA
    try:

        metadata = get_spotify_metadata(url)

        title = metadata["title"]
        artist = metadata["artist"]
        thumbnail = metadata["thumbnail"]

        # COVER
        st.image(
            thumbnail,
            width=260
        )

        # SONG INFO
        st.markdown(
            f"### 🎵 {title}"
        )

        st.markdown(
            f"👤 {artist}"
        )

    except Exception as e:

        st.error(
            f"Gagal mengambil metadata: {e}"
        )

        return

    st.markdown("---")

    # DOWNLOAD BUTTON
    if st.button(
        "⬇️ Download MP3",
        use_container_width=True
    ):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            try:

                query = (
                    f"{title} {artist}"
                )

                with st.spinner(
                    "Mencari lagu di YouTube..."
                ):

                    yt_info = download_mp3(
                        query,
                        temp_dir
                    )

                # FIND MP3
                files = list(
                    temp_dir.glob("*.mp3")
                )

                if not files:

                    st.error(
                        "MP3 tidak ditemukan."
                    )

                    return

                file_path = files[0]

                # AUDIO INFO
                st.markdown("---")

                st.markdown(
                    '<div class="card-title">'
                    '② Informasi Lagu'
                    '</div>',
                    unsafe_allow_html=True
                )

                st.markdown(f"""
                <div class="stat-row">

                    <div class="stat-box">
                        <div class="stat-label">
                            Judul
                        </div>

                        <div class="stat-value">
                            {yt_info["title"]}
                        </div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-label">
                            Channel
                        </div>

                        <div class="stat-value">
                            {yt_info["uploader"]}
                        </div>
                    </div>

                    <div class="stat-box">
                        <div class="stat-label">
                            Durasi
                        </div>

                        <div class="stat-value">
                            {format_duration(
                                yt_info["duration"]
                            )}
                        </div>
                    </div>

                </div>
                """, unsafe_allow_html=True)

                # READ AUDIO
                with open(file_path, "rb") as f:

                    audio_bytes = f.read()

                st.success(
                    "✅ Lagu berhasil didownload!"
                )

                # HISTORY
                add_history(
                    tool="Spotify Downloader",
                    input_file=url,
                    output_file=file_path.name,
                    details=title
                )

                # AUDIO PLAYER
                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

                # DOWNLOAD BUTTON
                st.download_button(
                    label="⬇️ Download MP3",
                    data=audio_bytes,
                    file_name=file_path.name,
                    mime="audio/mp3",
                    use_container_width=True
                )

            except Exception as e:

                st.error(
                    f"Gagal download lagu: {e}"
                )