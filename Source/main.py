import os

import streamlit as st
import utilities as uti

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


def main():
    """
    main function wraps all other functions and creates all tabs

    Returns:
        None
    """

    st.set_page_config(
        page_title="UNACORM",
        layout="wide",
        page_icon=os.path.join(uti.PATH_CACHE_DATA, "images", "Icon.png"),
        initial_sidebar_state="collapsed",
    )

    st.html("""
        <style>

        .stMainMenu {visibility:hidden;}
        .stAppDeployButton {visibility:hidden;}
        footer {visibility: hidden;}
        button[title="View fullscreen"]{
            visibility: hidden;}

        .stToolbarActions {
            max-width: 100px !important;  /* Restrict width */
            overflow: hidden;             /* Hide overflow */
            white-space: nowrap;          /* Prevent text wrapping */
            text-overflow: ellipsis;      /* Show ellipsis for overflow */
        }

        header.stAppHeader {
            background-color: #ffffff;
            min-height: 140px !important;           /* Increase header height */
            padding: 0px 0px !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1); /* Subtle shadow */
            position: relative !important;
            z-index: 1000 !important;              /* Keep above other content */
        }

        .rc-overflow {
            display: flex;
            justify-content: flex-end;
            margin-top: 65px;
            margin-bottom: 20px;
        }

        .rc-overflow-item {
                padding: 10px 5px;/* Larger clickable area */
            }

        .rc-overflow-item a, .rc-overflow-item span {
            font-size: 1.1em !important;
        }

        </style>
        """)

    # Removing old uploaded data
    uti.remove_cached_data()

    st.logo(
        os.path.join(uti.PATH_CACHE_DATA, "images", "Logo.png"),
        link="https://github.com/AAnzel/DNA_Encodings/",
    )

    st.html(
        '<style> img[data-testid="stHeaderLogo"] {height: 7rem; margin-left: 65px;}</style>'
    )

    st_home_page = st.Page(
        "1_home.py",
        title="Home",
        icon=":material/home:",
    )
    st_benchmark_page = st.Page(
        "2_benchmark.py",
        title="Benchmark",
        icon=":material/monitoring:",
    )
    st_upload_page = st.Page(
        "3_upload.py",
        title="Upload",
        icon=":material/upload_file:",
    )
    st_about_page = st.Page(
        "4_about.py",
        title="About",
        icon=":material/info:",
    )
    st_contact_page = st.Page(
        "5_contact.py",
        title="Contact",
        icon=":material/mail:",
    )

    st_pages = st.navigation(
        [
            st_home_page,
            st_benchmark_page,
            st_upload_page,
            st_about_page,
            st_contact_page,
        ],
        position="top",
    )
    st_pages.run()

    return None


if __name__ == "__main__":
    main()
