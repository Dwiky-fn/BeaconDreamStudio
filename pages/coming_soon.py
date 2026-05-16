import streamlit as st

def page_coming_soon(icon, title):
    st.markdown(
        f'<div class="page-title">{icon} {title}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-sub">'
        'Fitur ini sedang dalam pengembangan.'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.info(
        "🚧 Coming Soon — "
        "Fitur ini akan segera tersedia."
    )