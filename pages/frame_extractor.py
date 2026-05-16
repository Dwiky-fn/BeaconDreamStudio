from pathlib import Path
import tempfile
import zipfile
import cv2

import streamlit as st

from utils.history_manager import add_history

def page_frame_extractor():

    st.markdown(
        '<div class="page-title">🎞️ Frame Extractor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Extract frame dari video berdasarkan FPS.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">① Upload Video</div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "Upload Video",
        type=["mp4", "mov", "avi", "mkv", "webm"],
        label_visibility="collapsed"
    )

    if not uploaded:
        st.info(
            "🎥 Format didukung: "
            "MP4 · MOV · AVI · MKV · WEBM"
        )
        return

    fps_target = st.slider(
        "FPS Output",
        min_value=1,
        max_value=60,
        value=25
    )

    if st.button(
        "🖼️ Extract Frames",
        use_container_width=True
    ):

        with tempfile.TemporaryDirectory() as temp_dir:

            temp_dir = Path(temp_dir)

            video_path = temp_dir / uploaded.name

            with open(video_path, "wb") as f:
                f.write(uploaded.read())

            output_folder = temp_dir / "frames"
            output_folder.mkdir(exist_ok=True)

            cap = cv2.VideoCapture(str(video_path))

            original_fps = cap.get(
                cv2.CAP_PROP_FPS
            )

            frame_interval = (
                original_fps / fps_target
            )

            frame_count = 0
            saved_count = 0

            progress = st.progress(0)

            total_frames = int(
                cap.get(cv2.CAP_PROP_FRAME_COUNT)
            )

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                if frame_count >= saved_count * frame_interval:

                    filename = (
                        output_folder /
                        f"frame_{saved_count:04d}.png"
                    )

                    cv2.imwrite(
                        str(filename),
                        frame
                    )

                    saved_count += 1

                frame_count += 1

                progress.progress(
                    min(
                        frame_count / total_frames,
                        1.0
                    )
                )

            cap.release()

            # ZIP RESULT
            zip_path = temp_dir / "frames.zip"

            with zipfile.ZipFile(
                zip_path,
                "w",
                zipfile.ZIP_DEFLATED
            ) as zipf:

                for file in output_folder.glob("*.png"):

                    zipf.write(
                        file,
                        arcname=file.name
                    )

            with open(zip_path, "rb") as f:
                zip_bytes = f.read()

            st.success(
                f"✅ {saved_count} frame berhasil diextract!"
            )

            add_history(
                tool="Frame Extractor",
                input_file=uploaded.name,
                output_file="frames.zip"
            )

            st.download_button(
                label="⬇️ Download ZIP",
                data=zip_bytes,
                file_name="frames.zip",
                mime="application/zip",
                use_container_width=True
            )