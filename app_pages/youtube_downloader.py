from pathlib import Path
import tempfile

import streamlit as st
from yt_dlp import YoutubeDL

from utils.history_manager import add_history


def format_duration(seconds):

    if not seconds:
        return "Unknown"

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return (
            f"{hours}:{minutes:02d}:{seconds:02d}"
        )

    return f"{minutes}:{seconds:02d}"


def get_video_info(url):

    ydl_opts = {
        "quiet": True,
        "noplaylist": True,

        # FIX YOUTUBE
        "extractor_args": {
            "youtube": {
                "player_client": ["web"]
            }
        }
    }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

    return {
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "thumbnail": info.get("thumbnail"),
        "upload_date": info.get("upload_date"),
        "filesize": info.get("filesize"),
        "description": info.get("description"),
        "like_count": info.get("like_count")
    }


def download_video(
    url,
    mode,
    output_dir
):

    common_opts = {

        "outtmpl": str(
            output_dir / "%(title)s.%(ext)s"
        ),

        "quiet": True,
        "noplaylist": True,

        # FIX YOUTUBE
        "extractor_args": {
            "youtube": {
                "player_client": ["web"]
            }
        },

        "geo_bypass": True,
        "nocheckcertificate": True,

        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False
    }

    if mode == "mp3":

        ydl_opts = {
            **common_opts,

            "format": (
                "bestaudio[ext=m4a]/"
                "bestaudio/best"
            ),

            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }

    else:

        ydl_opts = {
            **common_opts,

            "format": (
                "bestvideo[ext=mp4]+"
                "bestaudio[ext=m4a]/"
                "best"
            ),

            "merge_output_format": "mp4"
        }

    with YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=True
        )

        return info.get(
            "title",
            "download"
        )


def page_youtube_downloader():

    st.markdown(
        '<div class="page-title">'
        '📥 YouTube Downloader'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Download video atau audio '
        'dari YouTube.'
        '</div>',
        unsafe_allow_html=True
    )

    # URL
    st.markdown(
        '<div class="card-title">'
        '① URL YouTube'
        '</div>',
        unsafe_allow_html=True
    )

    url = st.text_input(
        "URL",
        placeholder=(
            "https://youtube.com/watch?v=..."
        )
    )

    if not url:
        return

    # GET INFO
    try:

        info = get_video_info(url)

        # THUMBNAIL
        if info["thumbnail"]:

            st.image(
                info["thumbnail"],
                use_container_width=True
            )

        st.markdown("---")

        # TITLE
        st.markdown(
            f"## 🎬 {info['title']}"
        )

        st.markdown(
            f"👤 {info['uploader']}"
        )

        # STATS
        st.markdown(f"""
        <div class="stat-row">

            <div class="stat-box">

                <div class="stat-label">
                    Durasi
                </div>

                <div class="stat-value">
                    {format_duration(
                        info["duration"]
                    )}
                </div>

            </div>

            <div class="stat-box">

                <div class="stat-label">
                    Views
                </div>

                <div class="stat-value">
                    {info["view_count"]:,}
                </div>

            </div>

            <div class="stat-box">

                <div class="stat-label">
                    Likes
                </div>

                <div class="stat-value">
                    {
                        info["like_count"]:, 
                        if info["like_count"]
                        else "Hidden"
                    }
                </div>

            </div>

        </div>
        """, unsafe_allow_html=True)

        # DESCRIPTION
        if info["description"]:

            with st.expander(
                "📝 Deskripsi"
            ):

                st.write(
                    info["description"][:3000]
                )

    except Exception as e:

        st.error(
            f"Gagal mengambil info video: {e}"
        )

        return

    st.markdown("---")

    # FORMAT
    st.markdown(
        '<div class="card-title">'
        '② Format Download'
        '</div>',
        unsafe_allow_html=True
    )

    mode = st.radio(
        "Format",
        options=["mp3", "mp4"],
        horizontal=True
    )

    st.markdown("---")

    # DOWNLOAD
    if st.button(
        f"⬇️ Download {mode.upper()}",
        use_container_width=True
    ):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            try:

                with st.spinner(
                    "Mengunduh dari YouTube..."
                ):

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
                        "File hasil download "
                        "tidak ditemukan."
                    )

                    return

                file_path = files[0]

                # READ FILE
                with open(file_path, "rb") as f:

                    file_bytes = f.read()

                st.success(
                    "✅ Download selesai!"
                )

                # HISTORY
                add_history(
                    tool="YouTube Downloader",
                    input_file=url,
                    output_file=file_path.name,
                    details=mode.upper()
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

                # FILE INFO
                file_size = (
                    len(file_bytes)
                    / 1024
                    / 1024
                )

                st.markdown(f"""
                <div class="stat-row">

                    <div class="stat-box">

                        <div class="stat-label">
                            Format
                        </div>

                        <div class="stat-value">
                            {mode.upper()}
                        </div>

                    </div>

                    <div class="stat-box">

                        <div class="stat-label">
                            Ukuran
                        </div>

                        <div class="stat-value">
                            {file_size:.2f} MB
                        </div>

                    </div>

                </div>
                """, unsafe_allow_html=True)

                # DOWNLOAD BUTTON
                st.download_button(
                    label=(
                        f"⬇️ Download "
                        f"{mode.upper()}"
                    ),
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