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


def create_sidebar():
    """
    create_sidebar function creates the dashboard sidebar

    Returns:
        None
    """

    col_1, col_2 = st.sidebar.columns([3, 1])
    col_2.image(
        os.path.join(uti.PATH_CACHE_DATA, 'images',
                     'GitHub-Mark-120px-plus.png'),
        width=54)
    col_2.markdown('[GitHub](https://github.com/AAnzel/DNA_Encodings)')
    col_1.markdown('''
                      # UNACORM
                      The **U**nified D**NA** En**co**dings Platfo**rm**''')

    st.sidebar.markdown('''
        ---
        ### DNA Encoding Methods:

        * **Simple Code** by Church et al.
            * [DOI: 10.1126/science.1226355](https://www.science.org/doi/10.1126/science.1226355)

        * **Repetition Code** by Goldman et al.
            * [DOI: 10.1038/nature11875](https://www.nature.com/articles/nature11875)

        * **The 2D Code** by Grass et al.
            * [DOI: 10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378)

        * **XOR-Based Code** by Bornholt et al.
            * [DOI: 10.1145/2872362.2872397](https://dl.acm.org/doi/pdf/10.1145/2872362.2872397)
        ''')

    return None


def tuple_upload_file():
    """
    tuple_upload_file function uploads a file and caches it internally

    The function takes a string argument  necessary for creating seperate user
    sessions. It returns the path of the uploaded file and its name

    Returns:
        tuple: path of the uploaded file and its name are returned
    """

    st.header('File Upload')
    st.markdown('')
    list_file_type = ['txt', 'jpg', 'wav']

    imported_file = st.file_uploader(
        label='Upload your file', type=list_file_type,
        accept_multiple_files=False, key='Upload_file_')

    string_file_name = ''
    path_input_file = ''

    if imported_file is not None:
        float_time_uploaded = str(time.time()).replace('.', '_')
        string_file_name = imported_file.name
        string_new_name = float_time_uploaded + '_' + imported_file.name
        path_input_file = os.path.join(_PATH_UPLOADED_DATA, string_new_name)
        with open(path_input_file, mode='wb') as w:
            w.write(imported_file.getvalue())

        if os.path.exists(path_input_file):
            st.success('Your file is successfully uploaded!')

    return path_input_file, string_file_name


def create_main_page():
    """
    create_main_page function creates the main dashboard page

    Returns:
        None
    """

    # Removing old uploaded data
    uti.remove_cached_data()

    st.markdown('---')

    path_input_file = ''
    path_input_file, string_input_file = tuple_upload_file()
    string_file_name, string_file_extension = os.path.splitext(
        string_input_file)

    st.write('Your uploaded path data:\t', path_input_file)

    if path_input_file != '':
        np_binary_encoding, original_file_size = uti.np_data_to_binary_array(
            path_input_file, string_file_name)
    else:
        np_binary_encoding = None
        original_file_size = None

    st.markdown('---')

    st.header('DNA Encoding')
    list_chosen_dna_encoding = st.multiselect(
     'Select your preferred DNA Encoding Methods', uti.LIST_ENCODING_METHODS)

    st.warning('The length of processing time depends on your chosen methods')

    int_chosen_storage_length = st.number_input(
        'Choose your length of storage (in hours) or leave it empty to skip',
        value=None, min_value=1, step=1)

    df_new_detail = None
    df_new_summary = None

    list_results = []
    list_cannot_encode_decode = []
    dict_same_files = {'Filename': [], 'Method': [], 'Similarity': []}
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
            except Exception:
                list_cannot_encode_decode.append(string_encoding_method)
                # If the runtime error happens we have to create dummy data
                list_encoded_info = [string_file_name, string_encoding_method,
                                     'Encoding', string_file_extension,
                                     None, None, None, None]
                list_decoded_info = list_encoded_info
                list_decoded_info[2] = 'Decoding'
                np_decoded_array = np.array([])

            list_results.append(list_encoded_info)
            list_results.append(list_decoded_info)

            dict_same_files['Filename'].append(string_file_name)
            dict_same_files['Method'].append(string_encoding_method)
            dict_same_files['Similarity'].append(
                np.array_equal(np_binary_encoding, np_decoded_array))

        if list_cannot_encode_decode:
            st.error('Cannot encode/decode using the following methods:\t' +
                     str(list_cannot_encode_decode))

        df_new_detail = pd.DataFrame(
            list_results,
            columns=pd.Series(['Filename', 'Method', 'Transformation', 'Type',
                               'Size', 'Cost', 'Time', 'OriFile_Size']))
        df_new_detail = df_new_detail.merge(
            pd.DataFrame(dict_same_files), on=['Filename', 'Method'],
            how='inner')

        df_new_summary = uti.df_generate_summary(df_new_detail)

        st.markdown('Summary Report')
        st.dataframe(df_new_summary)

        with st.expander("Expand Detailed Information"):
            st.markdown('Detail Table')
            st.dataframe(df_new_detail)

        (chart_size, chart_time,
         chart_cost) = vis.visualize_uploaded_plotly(df_new_detail)

        st.plotly_chart(chart_size, use_container_width=True)
        st.plotly_chart(chart_time, use_container_width=True)
        st.plotly_chart(chart_cost, use_container_width=True)

    elif list_chosen_dna_encoding != [] and np_binary_encoding is not None:
        st.error('Choose your file and length of storage first!')
    else:
        pass

    df_existing_summary = pd.read_pickle(uti.PATH_EXISTING_SUMMARY)
    df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)

    # If we calculated something new
    if df_new_detail is not None and df_new_summary is not None:
        df_details_combined = pd.concat(
            [df_new_detail, df_existing_detail], ignore_index=True)
        df_summary_combined = pd.concat(
            [df_new_summary, df_existing_summary], ignore_index=True)
    else:
        df_details_combined = df_existing_detail
        df_summary_combined = df_existing_summary

    st.markdown('---')
    st.header('Benchmark')
    st.dataframe(df_summary_combined)
    st.download_button(
        label="Download",
        data=df_summary_combined.to_csv(index=False).encode('utf-8'),
        file_name='summary_data.csv',
        mime='text/csv',
    )

    with st.expander("Expand Detailed Information", expanded=False):
        st.markdown('Detail Table')
        st.dataframe(df_details_combined)
        st.download_button(
            label="Download",
            data=df_details_combined.to_csv(index=False).encode('utf-8'),
            file_name='detail_data.csv',
            mime='text/csv',
        )

    chart = vis.visualize_size_benchmark_plotly(df_summary_combined)
    st.plotly_chart(chart, use_container_width=True)

    list_files_to_visualize = list(
        pd.unique(df_summary_combined['Filename'])) + os.listdir(
            uti.PATH_ORIGINAL_DATA)
    list_files_chosen = st.multiselect(
     'Select files that you want to review (This will affect Cost' +
     ' and Time Charts)', default=list_files_to_visualize,
     options=list_files_to_visualize)

    st.markdown('---')
    chart = vis.visualize_cost_benchmark_plotly(
        list_files_chosen, df_details_combined)
    st.plotly_chart(chart, use_container_width=True)

    st.markdown('---')
    chart = vis.visualize_time_benchmark_plotly(
            list_files_chosen, df_details_combined)
    st.plotly_chart(chart, use_container_width=True)

    return None


def main():
    """
    main function wraps all other functions and creates the main page and the
    sidebar

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
                    </style>
                ''', unsafe_allow_html=True)

    create_sidebar()
    create_main_page()

    return None


if __name__ == '__main__':
    main()
