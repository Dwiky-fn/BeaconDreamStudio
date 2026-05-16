import streamlit as st

from utils.history_manager import (
    load_history
)

def page_history():

    st.markdown(
        '<div class="page-title">'
        '🕘 History'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Riwayat aktivitas BeaconDream Studio.'
        '</div>',
        unsafe_allow_html=True
    )

    history = load_history()

    if not history:

        st.info(
            "Belum ada riwayat."
        )

        return

    for item in history:

        st.markdown(f"""
        <div class="stat-box"
            style="margin-bottom:12px">

            <div class="stat-label">
                {item["tool"]}
            </div>

            <div class="stat-value">
                {item["input"]}
            </div>

            <div style="
                color:#6b7280;
                margin-top:6px;
                font-size:.85rem;
            ">
                ➜ {item["output"]}
            </div>

            <div style="
                color:#6b7280;
                margin-top:8px;
                font-size:.75rem;
            ">
                {item["date"]}
            </div>

        </div>
        """, unsafe_allow_html=True)