import os
import time
import numpy as np
import streamlit as st
import pandas as pd

import visualize as vis
import utilities as uti
import text_content as tc


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
    st.dataframe(df_summary, use_container_width=True)
    st.download_button(
        label="Download Benchmark Data",
        data=df_summary.to_csv(index=False).encode('utf-8'),
        file_name='summary_data.csv',
        mime='text/csv',
        icon=":material/download:",
        key='Download_Summary_' + string_key
    )

    with st.expander("Expand Detailed Information",
                     expanded=bool_expand_detail):
        st.markdown('### Detailed Benchmark Data',
                    help=tc.STRING_DETAILED_HELP)
        st.dataframe(df_detail, use_container_width=True)
        st.download_button(
            label="Download Detailed Benchmark Data",
            data=df_detail.to_csv(index=False).encode('utf-8'),
            file_name='detail_data.csv',
            mime='text/csv',
            icon=":material/download:",
            key='Download_Detail_' + string_key
        )

    return None


def create_contact_page():
    """
    create_contact_page function creates the Contact page

    Returns:
        None
    """
    st_col_1, st_col_2, st_col_3 = st.columns([1, 2, 1])
    st_col_2.header('Contact Us')
    st_col_2.markdown(tc.STRING_CONTACT_PAGE)

    return None


def create_about_page():
    """
    create_about function creates the About page

    Returns:
        None
    """
    st_col_1, st_col_2, st_col_3 = st.columns([1, 2, 1])
    st_col_2.header('About')
    st_col_2.markdown(tc.STRING_ABOUT_PAGE)

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
            st.success('The file is successfully uploaded')

    st.write('Uploaded path data:\t', path_input_file)

    if path_input_file != '':
        np_binary_encoding, original_file_size = uti.np_data_to_binary_array(
            path_input_file)
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
        value=None, min_value=1, step=1, disabled=True)

    float_error_multiplier = st.number_input(
        'Choose error multiplier value or leave it 0 to skip',
        value=0.0, min_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[0],
        max_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[-1], step=0.5,
        help=tc.STRING_MUTAGENESIS_HELP)
    with st.expander('What is error multiplier?'):
        st.info(tc.STRING_MUTAGENESIS_HELP)

    if (int_chosen_storage_length is None and float_error_multiplier == 0.0):
        bool_simulate_errors = False
    else:
        bool_simulate_errors = True

    df_new_detail = None
    df_new_summary = None

    list_results = []
    list_cannot_encode_decode = []
    if (list_chosen_dna_encoding != [] and np_binary_encoding is not None):
        for string_encoding_method in list_chosen_dna_encoding:
            # ! Runtime errors can occur if we simulate DNA degradation using
            # ! MESA. These errors occur with some DNA Encoding methods, such
            # ! as The2DCode that breaks if the error creates a homopolymer of
            # ! length 3. This is why we have to catch errors
            list_encoded_info = []

            (list_encoded_info, list_decoded_info,
                np_decoded_array, dict_error_results) = uti.tuple_pipeline(
                    string_encoding_method, np_binary_encoding,
                    path_input_file, string_input_file, original_file_size,
                    bool_simulate_errors,
                    False,  # TODO: Add logic for this
                    int_chosen_storage_length,
                    float_error_multiplier)

            # If error occured, we note it
            if len(np_decoded_array) == 0:
                list_cannot_encode_decode.append(string_encoding_method)

            bool_similar_files = np.array_equal(
                np_binary_encoding, np_decoded_array)
            list_results.append(
                list_encoded_info
                + [bool_similar_files,
                   float_error_multiplier,
                   dict_error_results['Number_of_substitutions'],
                   dict_error_results['Number_of_deletions'],
                   dict_error_results['Number_of_insertions'],
                   dict_error_results['Total_number_of_errors'],
                   dict_error_results['Base_error_ratio']])
            list_results.append(
                list_decoded_info
                + [bool_similar_files,
                   float_error_multiplier,
                   dict_error_results['Number_of_substitutions'],
                   dict_error_results['Number_of_deletions'],
                   dict_error_results['Number_of_insertions'],
                   dict_error_results['Total_number_of_errors'],
                   dict_error_results['Base_error_ratio']])

        if list_cannot_encode_decode:
            st.error('Cannot encode/decode using the following methods:\t' +
                     str(list_cannot_encode_decode))

        df_new_detail = pd.DataFrame(
            list_results,
            columns=pd.Series(
                ['Filename', 'Method', 'Transformation', 'Type', 'Size',
                 'Cost', 'Time', 'OriFile_Size', 'Similarity',
                 'Error_Multiplier', 'Number_of_substitutions',
                 'Number_of_deletions', 'Number_of_insertions',
                 'Total_number_of_errors', 'Base_error_ratio']))

        df_new_summary = uti.df_generate_summary(df_new_detail)

        if df_new_detail is not None and df_new_summary is not None:
            st.markdown('---')
            st.header('Benchmark')
            display_processed_data(df_new_summary, df_new_detail, True)

        (chart_size, chart_time,
         chart_cost) = vis.visualize_uploaded(df_new_detail)

        st.header('Information Density', help=tc.STRING_DENSITY_HELP)
        chart = vis.visualize_density_benchmark(df_new_summary)
        st.plotly_chart(chart, use_container_width=True)
        st.header('Size', help=tc.STRING_SIZE_HELP)
        st.plotly_chart(chart_size, use_container_width=True)
        st.header('Time', help=tc.STRING_TIME_HELP)
        st.plotly_chart(chart_time, use_container_width=True)
        st.header('Cost', help=tc.STRING_COST_HELP)
        st.plotly_chart(chart_cost, use_container_width=True)

    elif list_chosen_dna_encoding != [] and np_binary_encoding is not None:
        st.error('Choose a file and length of storage first.')  # TODO: Change
    else:
        pass

    return None


def create_benchmark_page():
    """
    create_main_page function creates the main dashboard page containing the
    benchamark information

    Returns:
        None
    """
    df_existing_summary = pd.read_pickle(uti.PATH_EXISTING_SUMMARY)
    df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)

    st.header('Benchmark', help=tc.STRING_MAIN_BENCHMARK_HELP)
    display_processed_data(df_existing_summary, df_existing_detail)
    st.markdown('---')

    st.header('Information Density', help=tc.STRING_DENSITY_HELP)
    chart_density = vis.visualize_density_benchmark(df_existing_summary)
    st.plotly_chart(chart_density, use_container_width=True)

    st.header('Failure Rate', help=None)  # TODO: Add new help
    chart_failure_rate = vis.visualize_failure_rate_general(
        df_existing_summary)
    st.plotly_chart(chart_failure_rate, use_container_width=True)

    st.header('Base Error', help=None)  # TODO: Add new help
    chart_base_error = vis.visualize_base_error_general(df_existing_summary)
    st.plotly_chart(chart_base_error, use_container_width=True)

    float_error_multiplier = st.slider(  # TODO: Continue from here! :)
        'Choose error multiplier value or leave it 0 to skip',
        value=0.0, min_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[0],
        max_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[-1], step=0.5, format='%1f',
        help=tc.STRING_MUTAGENESIS_HELP)
    with st.expander('What is error multiplier?'):
        st.info(tc.STRING_MUTAGENESIS_HELP)

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
        bool_whisker_chart = True
    else:
        bool_whisker_chart = False

    chart_cost_all = vis.visualize_cost_benchmark(
        list_files_chosen, df_existing_detail, float_error_multiplier,
        bool_whisker_chart)
    chart_time_all = vis.visualize_time_benchmark(
        list_files_chosen, df_existing_detail, float_error_multiplier,
        bool_whisker_chart)

    st.header('Cost', help=tc.STRING_COST_HELP)
    st.plotly_chart(chart_cost_all, use_container_width=True)
    st.header('Time', help=tc.STRING_TIME_HELP)
    st.plotly_chart(chart_time_all, use_container_width=True)

    return None


def main():
    """
    main function wraps all other functions and creates all tabs

    Returns:
        None
    """

    st.set_page_config(page_title='UNACORM', layout='wide',
                       initial_sidebar_state='collapsed')

    st.html('''
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
                ''')

    # Removing old uploaded data
    uti.remove_cached_data()

    st.image(os.path.join(uti.PATH_CACHE_DATA, 'images', 'Logo.png'))

    st_tab_benchmark, st_tab_upload, st_tab_about, st_tab_contact = st.tabs(
        [':material/Monitoring: BENCHMARK',
         ':material/Upload_File: FILE UPLOAD', ':material/Info: ABOUT',
         ':material/Mail: CONTACT'])

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
