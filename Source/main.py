import os
import streamlit as st
import page


def create_sidebar():
    """This function is used for creating sidebar description

    Returns:
        None
    """

    col_1, col_2 = st.sidebar.columns([3, 1])
    col_2.image(os.path.join('data', 'images', 'GitHub-Mark-120px-plus.png'),
                width=54)
    col_2.markdown('[GitHub](https://github.com/AAnzel/DNA_Encodings)')
    col_1.markdown('''
                      # UNACORM
                      The **U**nified D**NA** En**co**dings Platfo**rm**''')

    st.sidebar.markdown('''
        ---
        ### DNA Encoding Methods:

        * **Simple Code** by Church et al.
            * [DOI: 10.1126/science.1226355](https://www.science.org/doi/10.1126/science.1226355)  # noqa

        * **Repetition Code** by Goldman et al.
            * [DOI: 10.1038/nature11875](https://www.nature.com/articles/nature11875)  # noqa

        * **The 2D Code** by Grass et al.
            * [DOI: 10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378)  # noqa

        * **XOR-Based Code** by Bornholt et al.
            * [DOI: 10.1145/2872362.2872397](https://dl.acm.org/doi/pdf/10.1145/2872362.2872397)  # noqa
        ''')

    return None


def main():
    """This function is main function

    Returns:
        None
    """

    st.set_page_config(page_title='UNACORM', layout='wide',
                       initial_sidebar_state='expanded')

    st.markdown('''
                    <style>
                    #MainMenu {visibility: hidden;}
                    .stDeployButton {display:none;}
                    footer {visibility: hidden;}
                    details {
                                display: None;
                            }
                    </style>

                ''', unsafe_allow_html=True)

    create_sidebar()
    page.create_main_page()

    return None


if __name__ == '__main__':
    main()
