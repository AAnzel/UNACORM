import base64
import os

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

with st.container(horizontal_alignment="center"), st.container(width=1300):
    st.header(":primary[︱]About")
    st.markdown("")
    st.markdown(tc.STRING_ABOUT_PAGE_0)

    with open(
        os.path.join(uti.PATH_CACHE_DATA, "images", "DNA_process.png"), "rb"
    ) as f:
        image_b64 = base64.b64encode(f.read()).decode()
        st.html(
            "<img style='max-width: 100%;max-height: 100%;' "
            + "src='data:image/png;base64, "
            + str(image_b64)
            + "'/>",
            width=1000,
        )
    st.markdown(
        ":small[:grey[Created in Biorender] "
        + "[https://www.biorender.com/](https://www.biorender.com/)]"
    )

    st.markdown(tc.STRING_ABOUT_PAGE_1)
    st.markdown(tc.STRING_ABOUT_PAGE_3)
    st.image(
        os.path.join(uti.PATH_CACHE_DATA, "images", "data_set_summary.svg"),
        width=1000,
    )

    st.markdown(tc.STRING_ABOUT_PAGE_4)
    st.image(
        os.path.join(uti.PATH_CACHE_DATA, "images", "data_set_histogram.svg"),
        width=1000,
    )

    st.markdown(tc.STRING_ABOUT_PAGE_5)
    st.markdown(tc.STRING_ABOUT_PAGE_6)

    uti.display_footer()
