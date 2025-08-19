import streamlit as st
import text_content as tc
import utilities as uti

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"

_, st_col_1, _ = st.columns([1, 9, 1])
st_col_1.header(":primary[︱]Contact Us")
st_col_1.markdown(tc.STRING_CONTACT_PAGE_0)
st.html("<br><br>")

_, st_col_1, st_col_2, st_col_3, _ = st.columns(
    [1, 3, 3, 3, 1], gap="large", vertical_alignment="top"
)
st_col_1.markdown(tc.STRING_CONTACT_PAGE_1)
st_col_2.markdown(tc.STRING_CONTACT_PAGE_2)
st_col_3.markdown(tc.STRING_CONTACT_PAGE_3)

_, st_col_1, st_col_2, st_col_3, _ = st.columns(
    [1, 3, 3, 3, 1], gap="large", vertical_alignment="top"
)

st_col_1.link_button(
    "GitHub Repository",
    url="https://github.com/AAnzel/DNA_Encodings/tree/master",
    icon=":material/home_storage:",
    use_container_width=True,
    type="primary",
)

st_col_2.link_button(
    "Open Issue",
    url="https://github.com/AAnzel/DNA_Encodings/issues/new",
    icon=":material/bug_report:",
    use_container_width=True,
    type="primary",
)

st_col_3.link_button(
    "Create a Pull Request",
    url="https://github.com/AAnzel/DNA_Encodings/compare",
    icon=":material/add:",
    use_container_width=True,
    type="primary",
)

st.html("<br><br>")

_, st_col_1, st_col_2, st_col_3, _ = st.columns(
    [1, 3, 3, 3, 1], gap="large", vertical_alignment="top"
)
st_col_1.markdown(tc.STRING_CONTACT_PAGE_4)
st_col_2.markdown(tc.STRING_CONTACT_PAGE_5)
st_col_3.markdown(tc.STRING_CONTACT_PAGE_6)

_, st_col_1, st_col_2, st_col_3, _ = st.columns(
    [1, 3, 3, 3, 1], gap="large", vertical_alignment="top"
)

st_col_1.link_button(
    "Discuss",
    url="https://github.com/AAnzel/DNA_Encodings/discussions/new/choose",
    icon=":material/comment:",
    use_container_width=True,
    type="primary",
)

st_col_2.link_button(
    "Releases",
    url="https://github.com/AAnzel/DNA_Encodings/releases",
    icon=":material/deployed_code:",
    use_container_width=True,
    type="primary",
)

st_col_3.link_button(
    "AnzelA@rki.de",
    url="mailto:AnzelA@rki.de",
    icon=":material/mail:",
    use_container_width=True,
    type="primary",
)

uti.display_footer()
