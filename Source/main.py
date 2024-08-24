import os
import time
import numpy as np
from pathlib import Path
import streamlit as st
import pandas as pd

import visualize
import utilities


# List Path of Directories
path_root_data = os.path.join('..', 'Data')
path_uploaded = os.path.join(path_root_data, 'uploaded')
path_uploaded_txt = os.path.join(path_uploaded, 'txt')
path_uploaded_jpg = os.path.join(path_uploaded, 'jpg')
path_uploaded_wav = os.path.join(path_uploaded, 'wav')
path_uploaded_decoded = os.path.join(path_uploaded, 'decoded')
path_encoded_data = os.path.join(path_root_data, 'Encoded')
path_decoded_data = os.path.join(path_root_data, 'Decoded')
path_encoded_dna = os.path.join(path_root_data, 'Encoded', 'DNA')
path_decoded_dna = os.path.join(path_root_data, 'Decoded', 'DNA')
path_original_data = os.path.join(path_root_data, 'Original')
path_encoding_methods = os.path.join('Encodings')


def create_sidebar():  # noqa: E501
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
            * [DOI: 10.1126/science.1226355](https://www.science.org/doi/10.1126/science.1226355)

        * **Repetition Code** by Goldman et al.
            * [DOI: 10.1038/nature11875](https://www.nature.com/articles/nature11875)

        * **The 2D Code** by Grass et al.
            * [DOI: 10.1002/anie.201411378](https://doi.org/10.1002/anie.201411378)

        * **XOR-Based Code** by Bornholt et al.
            * [DOI: 10.1145/2872362.2872397](https://dl.acm.org/doi/pdf/10.1145/2872362.2872397)
        ''')

    return None


def upload_file(key_suffix):
    """This function is used for saving uploaded files

    Args:
        key_suffix (string): data type that was chosen by user

    Returns:
        save_path_os (str): full path of uploaded file
        uploaded_filename (str): name of uploaded file

    """
    dict_file_type_cache = {'txt': path_uploaded_txt, 'jpg': path_uploaded_jpg,
                            'wav': path_uploaded_wav}

    cache_folder_path = dict_file_type_cache[key_suffix]

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    imported_file = st.file_uploader(
        label='Upload your file', type=key_suffix, accept_multiple_files=False,
        key='Upload_file_' + key_suffix)

    uploaded_filename = ''
    save_path_os = ''

    if imported_file is not None:
        time_uploaded = str(time.time())
        uploaded_filename = os.path.splitext(imported_file.name)[0]
        filename = time_uploaded + '_' + imported_file.name
        save_path = Path(cache_folder_path, filename)
        save_path_os = os.path.join(cache_folder_path, filename)
        with open(save_path, mode='wb') as w:
            w.write(imported_file.getvalue())

        if save_path.exists():
            st.success('Your file is successfully uploaded!')
        # st.write(type(imported_file))
        file_details = {"filename": imported_file.name,
                        "filetype": imported_file.type}
        st.write(file_details)

    return save_path_os, uploaded_filename


def create_main_page():
    """This function is used to wrap all functionalities
    """

    st.header('File Upload')

    file_type = ['txt', 'jpg', 'wav']

    choose_file_type = st.selectbox(
        'Which type of file do you want to upload:', file_type)

    # Removing old uploaded data
    utilities.remove_cached_data()

    st.markdown('---')

    save_path = ''
    save_path, uploaded_filename = upload_file(key_suffix=choose_file_type)

    st.write('Your uploaded path data:\t', save_path)

    if save_path != '':
        encoded_binary_path = utilities.convert_text_data_to_binary(save_path)
        original_file_size = os.path.getsize(save_path)
    else:
        encoded_binary_path = ''
    st.write('Your encoded binary:\t', encoded_binary_path)

    st.markdown('---')

    st.header('DNA Encoding')
    existing_encoding = []
    for encoding_method in os.listdir(path_encoding_methods):
        existing_encoding.append(encoding_method)
    choose_dna_encoding = st.multiselect(
     'Select your prefered DNA Encoding Methods',
     existing_encoding)

    st.warning('The length of processing time depends on your chosen methods.')

    storage_length = st.text_input('Choose your length of storage (in hours)')

    df_report = pd.DataFrame(columns=['Filename', 'Method', 'Transformation',
                                      'Size', 'Cost', 'Time', 'Type'])
    df_summary = pd.DataFrame(columns=['Filename', 'Method', 'Size', 'Cost',
                                       'Time', 'Type', 'Similarity',
                                       'Encoding_Multipliers'])

    if (choose_dna_encoding != [] and encoded_binary_path != ''
            and storage_length != ''):
        binary = np.load(encoded_binary_path)
        file_basename = os.path.basename(encoded_binary_path)
        file_name = os.path.splitext(file_basename)[0]
        for encoding_method in choose_dna_encoding:
            try:
                output = utilities.pipeline(
                    encoding_method, binary, file_name, choose_file_type,
                    storage_length, save_path, uploaded_filename)
                list_encoded = output[0]
                list_decoded = output[1]
                list_summary = output[2]
                df_report.loc[len(df_report)] = list_encoded
                df_report.loc[len(df_report)] = list_decoded
                list_summary[7] = list_summary[7]/original_file_size
                df_summary.loc[len(df_summary)] = list_summary
            except Exception:
                continue
        st.write('Summary Report')
        st.dataframe(df_summary)

        with st.expander("Expand Detail"):
            st.write('Detail Table')
            st.dataframe(df_report)

        (chart_size, chart_time,
         chart_cost) = visualize.visualize_uploaded_plotly(df_report)

        st.plotly_chart(chart_size, use_container_width=True)
        st.plotly_chart(chart_time, use_container_width=True)
        st.plotly_chart(chart_cost, use_container_width=True)

    elif choose_dna_encoding != [] and encoded_binary_path == '':
        st.error('Choose your file and length of storage first!')
    else:
        pass

    st.write('---')
    st.header('Benchmark')
    df_summary_1 = df_summary
    df_summary_1 = df_summary_1.rename({
        'Size': 'Sum_Size', 'Time': 'Sum_Mean_Time', 'Cost': 'Sum_Cost'},
                                       axis=1)
    df_measure_sum = pd.read_pickle("data/pre_measure_stat_sum1.pkl")
    df_measure = pd.read_pickle("data/pre_measure1.pkl")
    df_report_1 = df_report
    if save_path != '':
        df_report_1['OriFile_Size'] = original_file_size
    df_concat = pd.concat([df_report_1, df_measure], ignore_index=True)
    df_measure_sum_concat = pd.concat(
        [df_summary_1, df_measure_sum], ignore_index=True)
    csv_sum = df_measure_sum_concat.to_csv().encode('utf-8')
    csv_detail = df_concat.to_csv().encode('utf-8')
    st.dataframe(df_measure_sum_concat)
    st.download_button(
        label="Download",
        data=csv_sum,
        file_name='summary_data.csv',
        mime='text/csv',
    )
    with st.expander("Expand Detail"):
        st.write('Detail Table')
        st.dataframe(df_concat)
        st.download_button(
            label="Download",
            data=csv_detail,
            file_name='detail_data.csv',
            mime='text/csv',
        )
    st.markdown("<h3 style='text-align: center;" +
                " color: black;'>File Size </h3>", unsafe_allow_html=True)

    chart = visualize.visualize_size_benchmark_plotly(df_measure_sum_concat)
    st.plotly_chart(chart, use_container_width=True)

    st.write('---')
    st.markdown("<h3 style='text-align: center; color: black;'>Cost </h3>",
                unsafe_allow_html=True)
    file_chosen = st.multiselect(
     'Select files that you want to review (This will affect Cost' +
     ' and Time Charts)', utilities.data_original)

    if file_chosen:
        chart = visualize.visualize_cost_benchmark_plotly(
            file_chosen, df_concat)
        st.plotly_chart(chart, use_container_width=True)

        st.write('---')
        st.markdown("<h3 style='text-align: center; color: black;'>Time</h3>",
                    unsafe_allow_html=True)

        chart = visualize.visualize_time_benchmark_plotly(
                file_chosen, df_concat)
        st.plotly_chart(chart, use_container_width=True)


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
    create_main_page()

    return None


if __name__ == '__main__':
    main()
