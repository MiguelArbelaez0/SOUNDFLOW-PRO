"""Shared SoundFlow visual styles."""

import streamlit as st


def apply_styles():
    st.markdown(
        """<style>
        .stApp { background-color: #0f1117; }
        .block-container { max-width: 1350px; padding-top: 2rem; padding-bottom: 4rem; }
        .stButton > button { border-radius: 10px; font-weight: 600; }
        </style>""",
        unsafe_allow_html=True,
    )
