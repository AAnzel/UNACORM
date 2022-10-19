import os
import streamlit as st
import page


def create_sidebar_and_main():
    """_summary_

    Returns:
        _type_: _description_
    """
    tmp_col_1, tmp_col_2, tmp_col_3, tmp_col_4, tmp_col_5 = st.columns(5)
    tmp_col_3.title('UNACORM')
    st.markdown('---')

    st.sidebar.image(os.path.join('images', 'Uni Marburg Logo.png'),
                     use_column_width=True)

    st.sidebar.markdown('---')
    col_1, col_2 = st.sidebar.columns([3, 1])
    col_2.image(os.path.join('images', 'GitHub-Mark-120px-plus.png'), width=54)
    col_2.markdown('[GitHub](https://github.com/AAnzel/DNA_Encodings)')
    col_1.markdown('''
                      **UNACORM**

                      The **U**NIFIED D**NA** EN**CO**DINGS PLATFO**RM**''')

    st.sidebar.markdown('''
        ---
        **Description**\n
        DNA Encoding Methods:\n
        -Simple Code by Church et al.:\n
         DOI: 10.1126/science.1226355\n
        -Repetition Code by Goldman et al.:\n
         DOI: 10.1038/nature11875\n
        -The 2D Code by Grass et al.:\n
         DOI: 10.1002/anie.201411378\n
        -XOR-Based Code by Bornholt et al.:\n
         DOI: 10.1145/2872362.2872397\n
        ---
        ''')

    page.create_main_upload()

    return None


def main():

    st.set_page_config(page_title='UNACORM', layout='wide',
                       initial_sidebar_state='expanded')

    st.markdown('''
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    details {
                                display: None;
                            }
                    </style>

                ''', unsafe_allow_html=True)

    create_sidebar_and_main()

    return None


if __name__ == '__main__':
    main()
