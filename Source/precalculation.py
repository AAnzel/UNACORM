import os
import pandas as pd
import numpy as np
import streamlit as st

from utilities import PATH_CACHE_DATA, PATH_ROOT_DATA
from utilities import np_data_to_binary_array, pipeline, df_generate_summary

_NUMBER_OF_EXPERIMENT_RUNS = 4
_LIST_PASS_METHODS = ['NOREC4DNA', 'DNA-Aeon']
_PATH_ORIGINAL_DATA = os.path.join(PATH_ROOT_DATA, 'Original', 'Test')  # TODO: Remove 'Test' # noqa
_PATH_EXISTING_DETAIL = os.path.join(PATH_CACHE_DATA, 'pre_detail.pkl')
_PATH_EXISTING_SUMMARY = os.path.join(PATH_CACHE_DATA, 'pre_summary.pkl')
_PATH_ENCODING_METHODS = os.path.join('Encodings')


def run_precalculation(int_num_of_iteration):
    """This function is used for running precalculation

    Args:
        num_of_iteration (int): number of iteration for each file
    """
    string_progress_text = ''
    st_progress_bar = st.progress(0, text=string_progress_text)

    bool_summary_exists = os.path.exists(_PATH_EXISTING_SUMMARY)
    bool_detail_exists = os.path.exists(_PATH_EXISTING_DETAIL)

    if bool_summary_exists:
        df_existing_summary = pd.read_pickle(_PATH_EXISTING_SUMMARY)
    else:
        df_existing_summary = pd.DataFrame(
            columns=['Filename', 'Method', 'Type', 'Sum_Mean_Time_s',
                     'Sum_Cost_$', 'Encoding_Multipliers', 'Similarity'])
    if bool_detail_exists:
        df_existing_detail = pd.read_pickle(_PATH_EXISTING_DETAIL)
    else:
        df_existing_detail = pd.DataFrame(
            columns=['Filename', 'Method', 'Transformation', 'Type', 'Size',
                     'Cost', 'Time', 'OriFile_Size', 'Similarity'])

    list_encoding_methods = []
    for string_encoding_method in os.listdir(_PATH_ENCODING_METHODS):
        if string_encoding_method not in _LIST_PASS_METHODS and os.path.isdir(
                os.path.join(_PATH_ENCODING_METHODS, string_encoding_method)):
            list_encoding_methods.append(string_encoding_method)

    list_results = []
    dict_same_files = {'Filename': [], 'Method': [], 'Similarity': []}
    list_original_files = os.listdir(_PATH_ORIGINAL_DATA)
    int_total_runs = len(list_original_files) * len(list_encoding_methods) *\
        int_num_of_iteration
    # We list original files
    int_counter = 1
    for string_file in list_original_files:
        path_one_file = os.path.join(_PATH_ORIGINAL_DATA, string_file)
        string_file_name = os.path.splitext(string_file)[0]

        if not os.path.isfile(path_one_file):
            continue

        for string_encoding_method in list_encoding_methods:
            # We check if we already processed the file with a specific
            # encoding method
            bool_file_is_processed = len(
                df_existing_summary[
                    (df_existing_summary["Filename"] == string_file_name) &
                    (df_existing_summary["Method"] == string_encoding_method)]
                ) != 0

            if not bool_file_is_processed:
                (np_binary_encoding,
                 int_file_size_bytes) = np_data_to_binary_array(
                    path_one_file, string_file_name)

                for int_i in range(int_num_of_iteration):
                    st_progress_bar.progress(
                        int_counter / int_total_runs,
                        text=(string_file + '_' + string_encoding_method +
                              '_' + str(int_i)))
                    int_counter += 1

                    (list_encoded_info, list_decoded_info,
                     np_decoded_array) = pipeline(
                        string_encoding_method, np_binary_encoding,
                        path_one_file, string_file, int_file_size_bytes, False,
                        0)

                    list_results.append(list_encoded_info)
                    list_results.append(list_decoded_info)

                    dict_same_files['Filename'].append(string_file_name)
                    dict_same_files['Method'].append(string_encoding_method)
                    dict_same_files['Similarity'].append(
                        np.array_equal(np_binary_encoding, np_decoded_array))

    df_new_detail = pd.DataFrame(
        list_results, columns=['Filename', 'Method', 'Transformation', 'Type',
                               'Size', 'Cost', 'Time', 'OriFile_Size'])
    df_new_detail = df_new_detail.merge(
        pd.DataFrame(dict_same_files), on=['Filename', 'Method'], how='inner')

    df_new_summary = df_generate_summary(df_new_detail, dict_same_files)

    st_progress_bar.empty()
    st.header('Recently calculated details')
    st.dataframe(df_new_detail)
    st.header('Existed precalculated details')
    st.dataframe(df_existing_detail)

    st.header('Recently calculated summary')
    st.dataframe(df_new_summary)
    st.header('Existed precalculated summary')
    st.dataframe(df_existing_summary)
    st.write('Do you want to merge new data into pickle file?')
    if st.button('Merge new data to pickel'):
        df_detail_concat = pd.concat(
            [df_new_detail, df_existing_detail], ignore_index=True)
        df_detail_concat.to_pickle(_PATH_EXISTING_DETAIL)
        df_summary_concat = pd.concat(
            [df_new_summary, df_existing_summary], ignore_index=True)
        df_summary_concat.to_pickle(_PATH_EXISTING_SUMMARY)

        if os.path.exists(_PATH_EXISTING_DETAIL) and os.path.exists(
                _PATH_EXISTING_SUMMARY):
            st.success('New data has been successfully merged')
            st.header('New Detail Data')
            st.dataframe(df_detail_concat)
            st.header('New Summary Data')
            st.dataframe(df_summary_concat)
        else:
            st.error('There was an error while uploading the pickle file')


def main():
    run_precalculation(_NUMBER_OF_EXPERIMENT_RUNS)


if __name__ == '__main__':
    main()
