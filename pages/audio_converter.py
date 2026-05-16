from pathlib import Path
import tempfile
import subprocess

import streamlit as st

from utils.history_manager import add_history

SUPPORTED_EXTENSIONS = [
    "m4a",
    "wav",
    "aac",
    "flac",
    "ogg"
]

def convert_audio(input_path, output_path):
    command = [
        "ffmpeg",
        "-i", str(input_path),

        "-vn",

        "-ar", "44100",
        "-ac", "2",
        "-b:a", "128k",

        str(output_path)
    ]

    subprocess.run(
        command,
        check=True
    )


def page_audio_converter():
    st.markdown(
        '<div class="page-title">'
        '🔄 Audio Converter'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Convert audio menjadi MP3.'
        '</div>',
        unsafe_allow_html=True
    )

    # =========================
    # UPLOAD FILES
    # =========================
    st.markdown(
        '<div class="card-title">'
        '① Upload Audio'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload Audio",
        type=SUPPORTED_EXTENSIONS,
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    if not uploaded_files:
        st.info(
            "🎵 Format didukung: "
            "M4A · WAV · AAC · FLAC · OGG"
        )

        return

    st.markdown("---")

    st.markdown(
        f"📁 Total file: "
        f"**{len(uploaded_files)}**"
    )

    # =========================
    # FILE LIST
    # =========================
    for file in uploaded_files:
        st.markdown(
            f"• {file.name}"
        )

    st.markdown("---")

    # =========================
    # CONVERT BUTTON
    # =========================
    if st.button(
        "🔄 Convert to MP3",
        use_container_width=True
    ):

        progress = st.progress(0)
        converted_files = []
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir = Path(temp_dir)
                total = len(uploaded_files)
                for i, file in enumerate(uploaded_files):
                    input_path = (
                        temp_dir / file.name
                    )

                    # SAVE INPUT
                    with open(input_path, "wb") as f:
                        f.write(file.read())

                    # OUTPUT
                    output_name = (
                        input_path.stem + ".mp3"
                    )

                    output_path = (
                        temp_dir / output_name
                    )

                    # CONVERT
                    convert_audio(
                        input_path,
                        output_path
                    )

                    # READ RESULT
                    with open(output_path, "rb") as f:
                        audio_bytes = f.read()

                    converted_files.append({
                        "name": output_name,
                        "bytes": audio_bytes
                    })

                    add_history(
                        tool="Audio Converter",
                        input_file=file.name,
                        output_file=output_name
                    )

                    progress.progress(
                        (i + 1) / total
                    )

            st.success(
                "✅ Semua file berhasil diconvert!"
            )

            

            st.markdown("---")

            # =========================
            # DOWNLOADS
            # =========================
            for file in converted_files:
                st.download_button(
                    label=f"⬇️ {file['name']}",
                    data=file["bytes"],
                    file_name=file["name"],
                    mime="audio/mp3",
                    use_container_width=True
                )
        except Exception as e:
            st.error(
                f"Gagal convert audio: {e}"
            )