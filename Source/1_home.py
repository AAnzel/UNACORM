import streamlit as st
import text_content as tc

_, st_col_2, _ = st.columns([1, 9, 1])
with st_col_2:
    st.info(tc.STRING_INTRODUCTION)
