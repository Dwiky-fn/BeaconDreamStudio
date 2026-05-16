from pathlib import Path

import streamlit as st
from moviepy import VideoFileClip
from utils.history_manager import add_history

def page_video_to_mp3():
    st.markdown(
        '<div class="page-title">'
        '🎬 Convert Video to MP3'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Convert video menjadi file MP3.'
        '</div>',
        unsafe_allow_html=True
    )

    # UPLOAD VIDEO
    st.markdown(
        '<div class="card-title">'
        '① Upload Video'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "Upload Video",
        type=[
            "mp4",
            "mov",
            "avi",
            "mkv",
            "webm"
        ],
        label_visibility="collapsed"
    )

    if not uploaded:
        st.info(
            "🎥 Format yang didukung: "
            "MP4 · MOV · AVI · MKV · WEBM"
        )
        return

    # SAVE TEMP VIDEO
    temp_video = Path(
        f"temp_{uploaded.name}"
    )

    with open(temp_video, "wb") as f:
        f.write(uploaded.read())

    # VIDEO PREVIEW
    st.video(str(temp_video))

    st.markdown("---")

    # CONVERT BUTTON
    if st.button(
        "🎵 Convert to MP3",
        use_container_width=True
    ):

        with st.spinner(
            "Mengconvert video ke MP3..."
        ):

            try:
                video = VideoFileClip(
                    str(temp_video)
                )

                output_path = Path(
                    f"{temp_video.stem}.mp3"
                )

                # CONVERT TO MP3
                video.audio.write_audiofile(
                    str(output_path),
                    codec="mp3"
                )

                # READ RESULT
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()

                st.success(
                    "✅ Video berhasil diconvert!"
                )

                add_history(
                    tool="Video to MP3",
                    input_file=uploaded.name,
                    output_file=f"{stem}.mp3"
                )

                # AUDIO PLAYER
                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

                # DOWNLOAD BUTTON
                stem = Path(uploaded.name).stem

                st.download_button(
                    label="⬇️ Download MP3",
                    data=audio_bytes,
                    file_name=f"{stem}.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )

            except Exception as e:
                st.error(
                    f"Gagal convert video: {e}"
                )