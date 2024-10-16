import os
import time
import numpy as np
import streamlit as st
import pandas as pd

import visualize as vis
import utilities as uti


__author__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian']
__copyright__ = ''
__credits__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian', 'Chisom Ezekannagha']
__license__ = 'GNU General Public License v3.0'
__version__ = '1.0.0'
__maintainer__ = 'Aleksandar Anžel'
__email__ = 'AnzelA@rki.de'
__status__ = 'Stable'


_PATH_UPLOADED_DATA = os.path.join(uti.PATH_ROOT_DATA, 'Uploaded')


def display_processed_data(df_summary, df_detail, bool_expand_detail=False):
    string_key = 'new' if bool_expand_detail else 'old'

    st.header('Benchmark')
    st.dataframe(df_summary, use_container_width=True)
    st.download_button(
        label="Download Benchmark Data",
        data=df_summary.to_csv(index=False).encode('utf-8'),
        file_name='summary_data.csv',
        mime='text/csv',
        key='Download_Summary_' + string_key
    )

    with st.expander("Expand Detailed Information",
                     expanded=bool_expand_detail):
        st.markdown('Detail Table')
        st.dataframe(df_detail, use_container_width=True)
        st.download_button(
            label="Download Detailed Benchmark Data",
            data=df_detail.to_csv(index=False).encode('utf-8'),
            file_name='detail_data.csv',
            mime='text/csv',
            key='Download_Detail_' + string_key
        )

    return None


def create_contact_page():
    st_col_1, st_col_2, st_col_3 = st.columns([1, 2, 1])

    st_col_2.markdown(
        '''
        # Contact Us

        We appreciate your interest in our project! Here are the best ways to get in touch or contribute.

        ## Project Repository

        Our project is hosted on GitHub. You can find the main repository here:

        **GitHub Repository:** [github.com/YourUsername/YourProject](https://github.com/YourUsername/YourProject)

        ## Reporting Issues

        If you've encountered a bug or have a feature request, please open an issue on our GitHub repository:

        **Open an Issue:** [github.com/YourUsername/YourProject/issues/new](https://github.com/YourUsername/YourProject/issues/new)

        Before creating a new issue, please check if a similar one already exists.

        ## Contributing

        We welcome contributions! If you'd like to contribute to the project:

        1. Fork the repository
        2. Create a new branch for your feature or bug fix
        3. Make your changes
        4. Submit a pull request

        **Create a Pull Request:** [github.com/YourUsername/YourProject/compare](https://github.com/YourUsername/YourProject/compare)

        Please review our contribution guidelines before submitting a pull request.

        ## Discussions

        For general questions, ideas, or community discussions, please use our GitHub Discussions forum:

        **GitHub Discussions:** [github.com/YourUsername/YourProject/discussions](https://github.com/YourUsername/YourProject/discussions)

        ## Project Updates

        Stay updated with our latest releases and announcements:

        **Releases:** [github.com/YourUsername/YourProject/releases](https://github.com/YourUsername/YourProject/releases)

        ## Additional Contact Information

        For matters not suitable for GitHub, you can reach us at:

        **Email:** [info@yourproject.com](mailto:info@yourproject.com)

        ## Follow Us

        Stay connected with our project:

        - **GitHub:** [@YourUsername](https://github.com/YourUsername)
        - **Twitter:** [@YourProject](https://twitter.com/YourProject)

        ---

        Thank you for your interest in our project! We look forward to your contributions and feedback.
        '''
    )
    return None


def create_about_page():
    """
    create_about function creates the About page

    Returns:
        None
    """

    st_col_1, st_col_2, st_col_3 = st.columns([1, 2, 1])
    st_col_2.markdown('''
        ### DNA Encoding Methods:

        * **Simple Code** by Church _et al._
        [DOI: 10.1126/science.1226355](https://www.science.org/doi/10.1126/science.1226355)

        * **Repetition Code** by Goldman _et al._
        [DOI: 10.1038/nature11875](https://www.nature.com/articles/nature11875)

        * **The 2D Code** by Grass _et al._
        [DOI: 10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378)

        * **XOR-Based Code** by Bornholt _et al._
        [DOI: 10.1145/2872362.2872397](https://dl.acm.org/doi/pdf/10.1145/2872362.2872397)

        * **DNA-Aeon Code** by Welzel _et al._
        [DOI: 10.1038/s41467-023-36297-3](https://doi.org/10.1038/s41467-023-36297-3)

        * **Raptor Code** by Shokrollahi _et al._
        [DOI: 10.1109/TIT.2006.874390](https://doi.org/10.1109/TIT.2006.874390)

        * **LT Code** by Luby _et al._
        [DOI: 10.1109/SFCS.2002.1181950](https://doi.org/10.1109/SFCS.2002.1181950)

        * **Online Code** by Maymounkov _et al._
        [LINK: TR2002-833.pdf](https://cs.nyu.edu/media/publications/TR2002-833.pdf)
        ''')

    return None


def create_upload_page():
    """
    create_upload_page function creates the Upload Page

    Returns:
        tuple: path of the uploaded file and its name are returned
    """

    st.header('File Upload')
    st.markdown('')
    list_file_type = ['txt', 'jpg', 'wav']

    imported_file = st.file_uploader(
        label='Upload a file', type=list_file_type,
        accept_multiple_files=False, key='Upload_file_')

    string_input_file = ''
    path_input_file = ''

    if imported_file is not None:
        float_time_uploaded = str(time.time()).replace('.', '_')
        string_input_file = imported_file.name
        string_new_name = float_time_uploaded + '_' + imported_file.name
        path_input_file = os.path.join(_PATH_UPLOADED_DATA, string_new_name)
        with open(path_input_file, mode='wb') as w:
            w.write(imported_file.getvalue())

        if os.path.exists(path_input_file):
            st.success('The file is successfully uploaded.')

    string_file_name, string_file_extension = os.path.splitext(
        string_input_file)

    st.write('Uploaded path data:\t', path_input_file)

    if path_input_file != '':
        np_binary_encoding, original_file_size = uti.np_data_to_binary_array(
            path_input_file, string_file_name)
    else:
        np_binary_encoding = None
        original_file_size = None

    st.markdown('---')

    st.header('DNA Encoding')
    list_chosen_dna_encoding = st.multiselect(
     'Select preferred DNA Encoding Methods', uti.LIST_ENCODING_METHODS,
     placeholder='Choose DNA encoding methods')

    st.warning('The length of processing time depends on chosen methods')

    int_chosen_storage_length = st.number_input(
        'Choose length of storage (in months) or leave it empty to skip',
        value=None, min_value=1, step=1)

    df_new_detail = None
    df_new_summary = None

    list_results = []
    list_cannot_encode_decode = []
    if (list_chosen_dna_encoding != [] and np_binary_encoding is not None):
        for string_encoding_method in list_chosen_dna_encoding:
            # Runtime errors can occur if we simulate DNA degradation using
            # MESA. These errors occur with some DNA Encoding methods, such as
            # The2DCode that breaks if the error creates a homopolymer of
            # length 3. This is why we have to catch errors
            list_encoded_info = []
            try:
                (list_encoded_info, list_decoded_info,
                    np_decoded_array) = uti.tuple_pipeline(
                    string_encoding_method, np_binary_encoding,
                    path_input_file, string_input_file, original_file_size,
                    True if int_chosen_storage_length is not None else False,
                    int_chosen_storage_length)
            except Exception as exc_e:
                print(exc_e)
                list_cannot_encode_decode.append(string_encoding_method)
                # If the runtime error happens we have to create dummy data
                list_encoded_info = [string_file_name, string_encoding_method,
                                     'Encoding', string_file_extension,
                                     None, None, None, None]
                list_decoded_info = list_encoded_info
                list_decoded_info[2] = 'Decoding'
                np_decoded_array = np.array([])

            bool_similar_files = np.array_equal(
                np_binary_encoding, np_decoded_array)
            list_results.append(list_encoded_info +
                                [bool_similar_files])
            list_results.append(list_decoded_info +
                                [bool_similar_files])

        if list_cannot_encode_decode:
            st.error('Cannot encode/decode using the following methods:\t' +
                     str(list_cannot_encode_decode))

        df_new_detail = pd.DataFrame(
            list_results,
            columns=pd.Series(['Filename', 'Method', 'Transformation', 'Type',
                               'Size', 'Cost', 'Time', 'OriFile_Size',
                               'Similarity']))

        df_new_summary = uti.df_generate_summary(df_new_detail)

        if df_new_detail is not None and df_new_summary is not None:
            st.markdown('---')
            display_processed_data(df_new_summary, df_new_detail, True)

        (chart_size, chart_time,
         chart_cost) = vis.visualize_uploaded(df_new_detail)

        st.plotly_chart(chart_size, use_container_width=True)
        st.plotly_chart(chart_time, use_container_width=True)
        st.plotly_chart(chart_cost, use_container_width=True)

    elif list_chosen_dna_encoding != [] and np_binary_encoding is not None:
        st.error('Choose a file and length of storage first.')
    else:
        pass

    return None


def create_benchmark_page():
    """
    create_main_page function creates the main dashboard page

    Returns:
        None
    """
    df_existing_summary = pd.read_pickle(uti.PATH_EXISTING_SUMMARY)
    df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)

    display_processed_data(df_existing_summary, df_existing_detail)

    chart = vis.visualize_size_benchmark(df_existing_summary)
    st.plotly_chart(chart, use_container_width=True)

    list_files_to_visualize = list(
        pd.unique(df_existing_summary['Filename']))

    list_files_chosen = st.multiselect(
     'Select the files to review (This will affect Cost' +
     ' and Time Charts)', default=list_files_to_visualize,
     options=list_files_to_visualize, placeholder='Choose files')

    string_selected_visualization = st.radio(
        'Visualize using', ['Whisker Chart', 'Bar Chart'], horizontal=True)

    st.markdown('---')
    if string_selected_visualization == 'Whisker Chart':
        chart_cost_all = vis.visualize_cost_benchmark_whisker(
            list_files_chosen, df_existing_detail)
        chart_time_all = vis.visualize_time_benchmark_whisker(
            list_files_chosen, df_existing_detail)
    else:
        chart_cost_all = vis.visualize_cost_benchmark_bar(
            list_files_chosen, df_existing_detail)
        chart_time_all = vis.visualize_time_benchmark_bar(
            list_files_chosen, df_existing_detail)

    st.plotly_chart(chart_cost_all, use_container_width=True)
    st.markdown('---')
    st.plotly_chart(chart_time_all, use_container_width=True)

    return None


def main():
    """
    main function wraps all other functions and creates the main page and the
    sidebar

    Returns:
        None
    """

    st.set_page_config(page_title='UNACORM', layout='wide',
                       initial_sidebar_state='collapsed')

    st.markdown('''
                    <style>

                        #MainMenu {visibility: hidden;}
                        .stDeployButton {display:none;}
                        footer {visibility: hidden;}

                        .block-container {
                            padding-top: 1.8rem;
                        }

                        button[title="View fullscreen"]{
                            visibility: hidden;}

                        .stTabs [data-baseweb="tab-list"] {
                            gap: 80px;
                            display: flex;
                            justify-content: flex-end;
                            width: 100%;
                        }

                        .stTabs [data-baseweb="tab-list"]
                            button [data-testid="stMarkdownContainer"] p {
                                font-size: 1.2rem;
                                font-weight: bold;
                            }
                        .stTabs [data-baseweb="tab"] {
                            height: 50px;
                            white-space: pre-wrap;
                            border-radius: 4px 4px 0px 0px;
                            gap: 1px;
                            padding-top: 5px;
                            padding-bottom: 10px;
                        }

                    </style>
                ''', unsafe_allow_html=True)

    # Removing old uploaded data
    uti.remove_cached_data()

    st_col_1, st_col_2, _ = st.columns([1, 1, 1])
    st_col_1.title('UNACORM')
    st_col_1.markdown('The **U**nified D**NA** En**co**dings Platfo**rm**')
    st_col_2.markdown('')
    st_col_2.markdown('')
    st_col_2.image(
        os.path.join(uti.PATH_CACHE_DATA, 'images', 'github-mark-white.png'),
        width=60)
    st.markdown('')
    st.markdown('')
    st.markdown('')

    st_tab_benchmark, st_tab_upload, st_tab_about, st_tab_contact = st.tabs(
        ['📊 BENCHMARK', '📂 FILE UPLOAD', 'ℹ️ ABOUT', '✉️ CONTACT'])

    with st_tab_benchmark:
        create_benchmark_page()
    with st_tab_upload:
        create_upload_page()
    with st_tab_about:
        create_about_page()
    with st_tab_contact:
        create_contact_page()

    return None


if __name__ == '__main__':
    main()
