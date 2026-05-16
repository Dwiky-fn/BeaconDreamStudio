# pages/youtube_downloader.py

from pathlib import Path
import tempfile

import streamlit as st
from yt_dlp import YoutubeDL

from utils.history_manager import add_history

def download_video(url, mode, output_dir):

    if mode == "mp3":

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
        }

    else:

        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": str(
                output_dir / "%(title)s.%(ext)s"
            ),
        }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        title = info.get("title", "download")

    return title


def page_youtube_downloader():

    st.markdown(
        '<div class="page-title">'
        '📥 YouTube Downloader'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Download video atau audio dari YouTube.'
        '</div>',
        unsafe_allow_html=True
    )

    # URL INPUT
    st.markdown(
        '<div class="card-title">'
        '① URL YouTube'
        '</div>',
        unsafe_allow_html=True
    )

    url = st.text_input(
        "URL",
        placeholder="https://youtube.com/..."
    )

    # FORMAT
    mode = st.radio(
        "Format",
        options=["mp3", "mp4"],
        horizontal=True
    )

    if not url:
        return

    st.markdown("---")

    # DOWNLOAD BUTTON
    if st.button(
        f"⬇️ Download {mode.upper()}",
        use_container_width=True
    ):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            with st.spinner(
                "Mengunduh dari YouTube..."
            ):

                try:

                    title = download_video(
                        url,
                        mode,
                        temp_dir
                    )

                    # FIND FILE
                    files = list(
                        temp_dir.glob(f"*.{mode}")
                    )

                    if not files:
                        st.error(
                            "File gagal ditemukan."
                        )
                        return

                    file_path = files[0]

                    with open(file_path, "rb") as f:
                        file_bytes = f.read()

                    st.success(
                        "✅ Download selesai!"
                    )

                    add_history(
                        tool="YouTube Downloader",
                        input_file=url,
                        output_file=file_path.name
                    )

                    # PREVIEW
                    if mode == "mp3":

                        st.audio(
                            file_bytes,
                            format="audio/mp3"
                        )

                    else:

                        st.video(
                            file_bytes
                        )

                    # DOWNLOAD BUTTON
                    st.download_button(
                        label=f"⬇️ Download {mode.upper()}",
                        data=file_bytes,
                        file_name=file_path.name,
                        mime=(
                            "audio/mp3"
                            if mode == "mp3"
                            else "video/mp4"
                        ),
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"Gagal download: {e}"
                    )