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


def tuple_upload_file(string_key_suffix):
    """
    tuple_upload_file function uploads a file and caches it internally

    The function takes a string argument  necessary for creating seperate user
    sessions. It returns the path of the uploaded file and its name

    Args:
        string_key_suffix (string): key that seperates user sessions

    Returns:
        tuple: path of the uploaded file and its name are returned
    """

    st.header('Choose your ' + string_key_suffix + ' data')
    st.markdown('')

    imported_file = st.file_uploader(
        label='Upload your file', type=string_key_suffix,
        accept_multiple_files=False, key='Upload_file_' + string_key_suffix)

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
        # st.write(type(imported_file))
        file_details = {"filename": imported_file.name,
                        "filetype": imported_file.type}
        st.write(file_details)

    return path_input_file, string_file_name


def create_main_page():
    """
    create_main_page function creates the main dashboard page

    Returns:
        None
    """

    st.header('File Upload')

    list_file_type = ['txt', 'jpg', 'wav']

    string_chosen_file_type = st.selectbox(
        'Which type of file do you want to upload:', list_file_type)

    # Removing old uploaded data
    uti.remove_cached_data()

    st.markdown('---')

    path_input_file = ''
    path_input_file, string_input_file = tuple_upload_file(
        string_key_suffix=string_chosen_file_type)
    string_file_name = os.path.splitext(string_input_file)[0]

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
     'Select your prefered DNA Encoding Methods', uti.LIST_ENCODING_METHODS)

    st.warning('The length of processing time depends on your chosen methods.')

    string_chosen_storage_length = st.text_input(
        'Choose your length of storage (in hours)')

    df_new_detail = None
    df_new_summary = None

    list_results = []
    dict_same_files = {'Filename': [], 'Method': [], 'Similarity': []}
    if (list_chosen_dna_encoding != [] and np_binary_encoding is not None
            and string_chosen_storage_length != ''):
        for string_encoding_method in list_chosen_dna_encoding:
            try:
                (list_encoded_info, list_decoded_info,
                 np_decoded_array) = uti.tuple_pipeline(
                    string_encoding_method, np_binary_encoding,
                    path_input_file, string_input_file, original_file_size,
                    True, int(string_chosen_storage_length))

                list_results.append(list_encoded_info)
                list_results.append(list_decoded_info)
                print('ENCODED\n', list_encoded_info)
                print('DECODED\n', list_decoded_info)

                dict_same_files['Filename'].append(string_file_name)
                dict_same_files['Method'].append(string_encoding_method)
                dict_same_files['Similarity'].append(
                    np.array_equal(np_binary_encoding, np_decoded_array))
            except Exception:
                continue

        df_new_detail = pd.DataFrame(
            list_results,
            columns=['Filename', 'Method', 'Transformation', 'Type',
                     'Size', 'Cost', 'Time', 'OriFile_Size'])
        df_new_detail = df_new_detail.merge(
            pd.DataFrame(dict_same_files), on=['Filename', 'Method'],
            how='inner')

        df_new_summary = uti.df_generate_summary(df_new_detail)

        st.write('Summary Report')
        st.dataframe(df_new_summary)

        with st.expander("Expand Detail"):
            st.write('Detail Table')
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

    st.write('---')
    st.header('Benchmark')
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

    csv_detail = df_details_combined.to_csv().encode('utf-8')
    csv_sum = df_summary_combined.to_csv().encode('utf-8')

    st.dataframe(df_summary_combined)
    st.download_button(
        label="Download",
        data=csv_sum,
        file_name='summary_data.csv',
        mime='text/csv',
    )

    with st.expander("Expand Detail"):
        st.write('Detail Table')
        st.dataframe(df_details_combined)
        st.download_button(
            label="Download",
            data=csv_detail,
            file_name='detail_data.csv',
            mime='text/csv',
        )
    st.markdown("<h3 style='text-align: center;" +
                " color: black;'>File Size </h3>", unsafe_allow_html=True)

    chart = vis.visualize_size_benchmark_plotly(df_summary_combined)
    st.plotly_chart(chart, use_container_width=True)

    st.write('---')
    st.markdown("<h3 style='text-align: center; color: black;'>Cost </h3>",
                unsafe_allow_html=True)
    file_chosen = st.multiselect(
     'Select files that you want to review (This will affect Cost' +
     ' and Time Charts)', os.listdir(uti.PATH_ORIGINAL_DATA))

    if file_chosen:
        chart = vis.visualize_cost_benchmark_plotly(
            file_chosen, df_details_combined)
        st.plotly_chart(chart, use_container_width=True)

        st.write('---')
        st.markdown("<h3 style='text-align: center; color: black;'>Time</h3>",
                    unsafe_allow_html=True)

        chart = vis.visualize_time_benchmark_plotly(
                file_chosen, df_details_combined)
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
                    details {
                                display: None;
                            }
                    </style>

                ''', unsafe_allow_html=True)

    create_sidebar()
    create_main_page()

    return None


if __name__ == '__main__':
    main()
