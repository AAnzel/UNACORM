import streamlit as st
import text_content as tc

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"

_, st_col_2, _ = st.columns([1, 9, 1])
st_col_2.header(":primary[︱]About")
st_col_2.markdown(tc.STRING_ABOUT_PAGE)
