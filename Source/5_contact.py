import streamlit as st
import text_content as tc
import utilities as uti

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Anyabolu"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"

with st.container(horizontal_alignment="center"), st.container(width=1300):
    st.header(":primary[︱]Contact Us")
    st.markdown(tc.STRING_CONTACT_PAGE_0)
    st.space(size="small")

    with st.container(
        horizontal=True, horizontal_alignment="center", gap="large"
    ):
        with st.container(
            vertical_alignment="distribute", height=210, border=False
        ):
            st.markdown(tc.STRING_CONTACT_PAGE_1)
            st.link_button(
                "GitHub Repository",
                url="https://github.com/AAnzel/UNACORM/tree/master",
                icon=":material/home_storage:",
                width="stretch",
                type="primary",
            )
        with st.container(
            vertical_alignment="distribute", height=210, border=False
        ):
            st.markdown(tc.STRING_CONTACT_PAGE_2)
            st.link_button(
                "Open Issue",
                url="https://github.com/AAnzel/UNACORM/issues/new",
                icon=":material/bug_report:",
                width="stretch",
                type="primary",
            )

        with st.container(
            vertical_alignment="distribute", height=210, border=False
        ):
            st.markdown(tc.STRING_CONTACT_PAGE_3)
            st.link_button(
                "Create a Pull Request",
                url="https://github.com/AAnzel/UNACORM/compare",
                icon=":material/add:",
                width="stretch",
                type="primary",
            )

    st.space(size="large")

    with st.container(
        horizontal=True, horizontal_alignment="center", gap="large"
    ):
        with st.container(
            vertical_alignment="distribute", height=210, border=False
        ):
            st.markdown(tc.STRING_CONTACT_PAGE_4)
            st.link_button(
                "Discuss",
                url="https://github.com/AAnzel/UNACORM/discussions/new/choose",
                icon=":material/comment:",
                width="stretch",
                type="primary",
            )

        with st.container(
            vertical_alignment="distribute", height=210, border=False
        ):
            st.markdown(tc.STRING_CONTACT_PAGE_5)
            st.link_button(
                "Releases",
                url="https://github.com/AAnzel/UNACORM/releases",
                icon=":material/deployed_code:",
                width="stretch",
                type="primary",
            )

        with st.container(
            vertical_alignment="distribute", height=210, border=False
        ):
            st.markdown(tc.STRING_CONTACT_PAGE_6)
            st.link_button(
                "AnzelA@rki.de",
                url="mailto:AnzelA@rki.de",
                icon=":material/mail:",
                width="stretch",
                type="primary",
            )

    uti.display_footer()
