import streamlit as st
import text_content as tc

_, st_col_2, _ = st.columns([1, 9, 1])
st_col_2.header("Contact Us")
st_col_2.markdown(tc.STRING_CONTACT_PAGE)
