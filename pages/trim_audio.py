import io
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from pydub import AudioSegment

from utils.formatter import fmt_time
from utils.history_manager import add_history
from components.waveform import waveform_editor

def page_trim():
    st.markdown(
        '<div class="page-title">✂️ Trim Audio</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Geser handle kuning kiri/kanan pada waveform '
        'untuk menentukan area trim.'
        '</div>',
        unsafe_allow_html=True
    )

    # UPLOAD
    st.markdown(
        '<div class="card-title">① Upload File Audio</div>',
        unsafe_allow_html=True
    )

    uploaded = st.file_uploader(
        "Upload Audio",
        type=[
            "mp3",
            "wav",
            "ogg",
            "flac",
            "m4a",
            "aac",
            "opus"
        ],
        label_visibility="collapsed",
    )

    if not uploaded:
        st.markdown(
            '<div class="upload-hint">'
            '🎵 Mendukung: MP3 · WAV · OGG · FLAC · '
            'M4A · AAC · OPUS'
            '</div>',
            unsafe_allow_html=True
        )
        return

    ext = Path(uploaded.name).suffix.lstrip(".").lower()

    # LOAD AUDIO
    with st.spinner("Memuat audio..."):

        try:
            audio_bytes = uploaded.read()

            audio = AudioSegment.from_file(
                io.BytesIO(audio_bytes),
                format=ext
            )

        except Exception as e:
            st.error(f"Gagal membaca file: {e}")
            return

    duration_sec = len(audio) / 1000
    size_kb = len(audio_bytes) / 1024

    # AUDIO INFO
    st.markdown("---")

    st.markdown(
        '<div class="card-title">② Info File</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
    <div class="stat-row">

        <div class="stat-box">
            <div class="stat-label">Durasi</div>
            <div class="stat-value">
                {fmt_time(duration_sec)}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Sample Rate</div>
            <div class="stat-value">
                {audio.frame_rate:,} Hz
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Channels</div>
            <div class="stat-value">
                {"Stereo" if audio.channels == 2 else "Mono"}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Bit Depth</div>
            <div class="stat-value">
                {audio.sample_width * 8}-bit
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Ukuran</div>
            <div class="stat-value">
                {size_kb:.1f} KB
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # WAVEFORM
    st.markdown("---")

    st.markdown(
        '<div class="card-title">③ Waveform Editor</div>',
        unsafe_allow_html=True
    )

    html_code = waveform_editor(
        audio_bytes,
        ext,
        duration_sec
    )

    components.html(
        html_code,
        height=280,
        scrolling=False
    )

    # TRIM SETTINGS
    st.markdown("---")

    st.markdown(
        '<div class="card-title">'
        '④ Format Output & Trim'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns([2, 2, 3])

    with col1:

        st.markdown("**⏮ Start**")

        start_sec = st.number_input(
            "start",
            min_value=0.0,
            max_value=duration_sec - 0.1,
            value=0.0,
            step=0.1,
            format="%.1f",
            label_visibility="collapsed",
        )

    with col2:

        st.markdown("**⏭ End**")

        end_sec = st.number_input(
            "end",
            min_value=0.1,
            max_value=duration_sec,
            value=duration_sec,
            step=0.1,
            format="%.1f",
            label_visibility="collapsed",
        )

    with col3:

        st.markdown("**Format Output**")

        out_fmt = st.radio(
            "fmt",
            options=["mp3", "wav", "ogg", "flac"],
            horizontal=True,
            label_visibility="collapsed"
        )

    # VALIDATION
    if start_sec >= end_sec:
        st.warning("⚠️ Start harus lebih kecil dari End.")
        return

    trimmed_dur = end_sec - start_sec

    st.markdown(f"""
    <div class="stat-row">

        <div class="stat-box">
            <div class="stat-label">Dari</div>
            <div class="stat-value">
                {fmt_time(start_sec)}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Sampai</div>
            <div class="stat-value">
                {fmt_time(end_sec)}
            </div>
        </div>

        <div class="stat-box">
            <div class="stat-label">Durasi Hasil</div>
            <div class="stat-value">
                {fmt_time(trimmed_dur)}
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    # PROCESS TRIM
    st.markdown("---")

    if st.button(
        "✂️ Trim Sekarang",
        use_container_width=True
    ):

        with st.spinner("Memproses trim..."):

            trimmed = audio[
                int(start_sec * 1000):
                int(end_sec * 1000)
            ]

            buf = io.BytesIO()

            trimmed.export(
                buf,
                format=out_fmt,
                **(
                    {"bitrate": "192k"}
                    if out_fmt == "mp3"
                    else {}
                )
            )

            buf.seek(0)

            result_bytes = buf.read()

        st.success(
            f"✅ Trim selesai! "
            f"Durasi: {fmt_time(trimmed_dur)}"
        )

        add_history(
            tool="Trim Audio",
            input_file=uploaded.name,
            output_file=out_name
        )

        st.audio(
            result_bytes,
            format=f"audio/{out_fmt}"
        )

        stem = Path(uploaded.name).stem

        out_name = (
            f"{stem}_trim.{out_fmt}"
        )

        st.download_button(
            label=f"⬇️ Download ({out_name})",
            data=result_bytes,
            file_name=out_name,
            mime=f"audio/{out_fmt}",
            use_container_width=True
        )