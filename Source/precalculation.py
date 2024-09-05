import os
import errno
import pandas as pd
import time
import string
import numpy as np
import bitarray as ba
import streamlit as st

# Importing Encodings
import xor_code_python as encoding_xor
from Encodings.The2DCode import encoder as encoding_2d
from Encodings.SimpleCode.src import transform as encoding_simple
from Encodings.RepetitionCode.src import transform as encoding_repetition
from Encodings.NOREC4DNA import unified_dna_lt as encoding_lt
from Encodings.NOREC4DNA import unified_dna_online as encoding_online # Include this one # noqa
from Encodings.NOREC4DNA import unified_dna_raptor as encoding_raptor # Include this one # noqa


# Defining paths for important files and directories
path_root_data = os.path.join('..', 'Data')
path_cache_data = os.path.join(path_root_data, 'cache_data')
path_original_data = os.path.join(path_root_data, 'Original', 'Test')  # TODO: Remove 'Test' # noqa
path_original_translated = os.path.join(
    path_root_data, 'Original_Translated')  # This is where we keep boolean
# representations of the original data
path_encoded_data = os.path.join(path_root_data, 'Encoded')
path_decoded_data = os.path.join(path_root_data, 'Decoded')
path_existing_detail = os.path.join(path_cache_data, 'pre_detail.pkl')
path_existing_summary = os.path.join(path_cache_data, 'pre_summary.pkl')
path_encoding_methods = os.path.join('Encodings')

_NUMBER_OF_EXPERIMENT_RUNS = 4
_LIST_PASS_METHODS = ['NOREC4DNA', 'DNA-Aeon']
_DF_METRICS = pd.read_csv(os.path.join(path_cache_data, 'synthesis_cost.csv'))

# ============================================================================
# Function definitions start here
# ============================================================================


def cost_encoding(list_dna_sequences):
    """This function is used for calculating synthesizing cost

    Args:
        list_dna_sequences (list): list of DNA sequences

    Returns:
        int_cost_total (int): synthesising cost
    """
    int_num_of_oligos = len(list_dna_sequences)
    int_max_nucleotides = 0
    for string_seq in list_dna_sequences:
        int_nucleotide_number = len(string_seq.translate(
            {ord(c): None for c in string.whitespace}))
        if int_nucleotide_number > int_max_nucleotides:
            int_max_nucleotides = int_nucleotide_number

    i = 0 if int_max_nucleotides <= 120 else 1

    if int_num_of_oligos >= 2 and int_num_of_oligos <= 100:
        j = 1
    elif int_num_of_oligos >= 101 and int_num_of_oligos <= 500:
        j = 2
    elif int_num_of_oligos >= 501 and int_num_of_oligos <= 1000:
        j = 3
    else:
        j = 4

    int_cost_total = _DF_METRICS.iloc[i, j] * int_num_of_oligos

    return int_cost_total


def list_encode_decode(str_encoding_method, list_np_data, path_file,
                       bool_encode):
    """This function is used for encoding the binary data into DNA sequences

    Args:
        encoding_method (str): chosen encoding method
        list_np_data (list or np.array): data to encode or decode
        path_file (os.path): path of the original un-encoded file
        bool_encode (bool): if true encoding is performed, if false then
        decoding

    Returns:
        list_generated_seq (list): encoded dna list
    """
    list_generated_seq = []

    if bool_encode:
        if str_encoding_method == 'The2DCode':
            list_generated_seq = encoding_2d.encode('', list_np_data)
        elif str_encoding_method == 'XORBasedCode':
            list_generated_seq = encoding_xor.encode('', list_np_data)
        elif str_encoding_method == 'SimpleCode':
            list_generated_seq = encoding_simple.encode('', list_np_data)
        elif str_encoding_method == 'RepetitionCode':
            list_generated_seq = encoding_repetition.encode('', list_np_data)
        elif str_encoding_method == 'NOREC4DNA':  # ! Fix
            list_generated_seq = encoding_lt.encode(path_file, list_np_data)[0]
        else:
            pass
    else:
        if str_encoding_method == 'The2DCode':
            list_generated_seq = encoding_2d.decode('', list_np_data)
        elif str_encoding_method == 'XORBasedCode':
            list_generated_seq = encoding_xor.decode('', list_np_data)
        elif str_encoding_method == 'SimpleCode':
            list_generated_seq = encoding_simple.decode('', list_np_data)
        elif str_encoding_method == 'RepetitionCode':
            list_generated_seq = encoding_repetition.decode('', list_np_data)
        elif str_encoding_method == 'NOREC4DNA':  # ! Fix
            list_generated_seq = encoding_lt.decode(path_file, list_np_data)[0]
        else:
            pass

    return list_generated_seq


def pipeline(string_encoding_method, np_bit_array, string_file_name,
             int_original_size):
    """This function is used for integrating the process for one file

    Args:
        string_encoding_method (str): chosen encoding method
        np_bit_array (array): numpy np_bit_array array of uploaded file
        path_input_file (str): path of uploaded data
        int_original_size (number): size of original file

    Returns:
        list_encoded [list]: list of result from encoding process including
        time, cost, and size
        list_decoded [list]: list of result from decoding process including
        time, cost, and size
    """
    path_input_file = os.path.join(path_original_data, string_file_name)
    string_input_file_basename = os.path.splitext(string_file_name)[0]
    string_file_extension = os.path.splitext(string_file_name)[1][1:]

    # We time the encoding process
    int_start_time = time.time()
    list_dna_sequences = list_encode_decode(
        string_encoding_method, np_bit_array, path_input_file, True)
    int_time_encoding = time.time() - int_start_time

    int_cost_encoding = cost_encoding(list_dna_sequences)

    string_encoded_file_name = string_input_file_basename + '_' + \
        string_encoding_method + '.txt'
    path_encoded_file = os.path.join(path_encoded_data,
                                     string_encoded_file_name)
    with open(path_encoded_file, 'w') as f:
        f.writelines(list_dna_sequences)

    int_encoded_file_size = os.path.getsize(path_encoded_file)

    list_encoded = [
        string_input_file_basename, string_encoding_method, 'Encoding',
        '.' + string_file_extension, int_encoded_file_size, int_cost_encoding,
        int_time_encoding, int_original_size]

    # TODO ===================================================================
    list_modified_sequence = []  # TODO: Add a flag to call MESA and generalize
    list_modified_sequence = list_dna_sequences
    # TODO ===================================================================

    # We time the decoding process
    int_start_time = time.time()
    np_decoded_dna_sequences = list_encode_decode(
        string_encoding_method, list_modified_sequence, path_input_file, False)
    int_time_decoding = time.time() - int_start_time

    int_cost_decoding = 0
    string_decoded_file_name = string_input_file_basename + '_' + \
        string_encoding_method + '.npy'

    path_decoded_file = os.path.join(path_decoded_data,
                                     string_decoded_file_name)
    np.save(path_decoded_file, np_decoded_dna_sequences)
    int_decoded_file_size = os.path.getsize(path_decoded_file)

    list_decoded = [
        string_input_file_basename, string_encoding_method, 'Decoding',
        '.' + string_file_extension, int_decoded_file_size, int_cost_decoding,
        int_time_decoding, int_original_size]

    return list_encoded, list_decoded, np_decoded_dna_sequences


def df_generate_summary(df_report, dict_same_files):
    """This function is used for generating summary dataframe from detail
    dataframe (from 10 times running pipeline)

    Args:
        df_report (DataFrame): detailed df containing previous runs of one
        encoding method
        dict_same_files (dict): A dict containing if encoding/decoding process
        produced the same or different files for one encoding method

    Returns:
        _type_: _description_
    """
    df_summary = df_report.copy(deep=True)
    df_encoding_multipliers = df_report[[
        'Filename', 'Method', 'Transformation', 'Type', 'Size',
        'OriFile_Size']].copy(deep=True)
    df_encoding_multipliers['Encoding_Multipliers'] = df_encoding_multipliers[
        'Size'] / df_encoding_multipliers['OriFile_Size']
    df_encoding_multipliers = df_encoding_multipliers.loc[
        df_summary['Transformation'] == 'Encoding']
    df_encoding_multipliers.drop(
        ['Transformation', 'Size', 'OriFile_Size'], axis=1, inplace=True)
    df_encoding_multipliers = df_encoding_multipliers.groupby(
        ['Filename', 'Method', 'Type']).agg(
            {'Encoding_Multipliers': 'first'}).reset_index()

    df_summary.drop(['Size', 'OriFile_Size'], axis=1, inplace=True)

    df_summary = df_summary.groupby(
        ['Filename', 'Method', 'Transformation', 'Type', 'Similarity']).agg(
            {'Time': 'mean', 'Cost': 'mean'}).reset_index()
    df_summary = df_summary.groupby(
        ['Filename', 'Method', 'Type', 'Similarity']).agg(
            {'Time': 'sum', 'Cost': 'sum'}).reset_index()
    df_summary.rename(
        columns={'Time': 'Sum_Mean_Time', 'Cost': 'Sum_Cost'}, inplace=True)
    df_summary = df_summary.merge(
        df_encoding_multipliers,
        on=['Filename', 'Method', 'Type'], how='inner')

    return df_summary


def np_data_to_binary_array(path_original_file, string_file_name):
    """This function is used to convert data to binary

    Args:
        path_original_file (os.path): path of the original file
        string_file_name (string): name of the file without extension

    Returns:
        binary_numpy_content (np.array): bit array representing the original
        file
    """
    np_binary_numpy_content = None
    int_translated_file_size = 0

    if os.path.isfile(path_original_file):
        with open(path_original_file, 'rb') as fd_file:
            np_binary_array_content = ba.bitarray()
            np_binary_array_content.fromfile(fd_file)
            np_binary_numpy_content = np.frombuffer(
                np_binary_array_content.unpack(), dtype=bool)

            path_translated_file = os.path.join(path_original_translated,
                                                string_file_name + '.npy')
            np.save(path_translated_file, np_binary_numpy_content)
            int_translated_file_size = os.path.getsize(path_translated_file)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_original_file)

    return np_binary_numpy_content, int_translated_file_size


def run_precalculation(int_num_of_iteration):
    """This function is used for running precalculation

    Args:
        num_of_iteration (int): number of iteration for each file
    """
    string_progress_text = ''
    st_progress_bar = st.progress(0, text=string_progress_text)

    bool_summary_exists = os.path.exists(path_existing_summary)
    bool_detail_exists = os.path.exists(path_existing_detail)

    if bool_summary_exists:
        df_existing_summary = pd.read_pickle(path_existing_summary)
    else:
        df_existing_summary = pd.DataFrame(
            columns=['Filename', 'Method', 'Type', 'Sum_Mean_Time', 'Sum_Size',
                     'Sum_Cost', 'Encoding_Multipliers', 'Similarity'])
    if bool_detail_exists:
        df_existing_detail = pd.read_pickle(path_existing_detail)
    else:
        df_existing_detail = pd.DataFrame(
            columns=['Filename', 'Method', 'Transformation', 'Type', 'Size',
                     'Cost', 'Time', 'OriFile_Size'])

    list_encoding_methods = []
    for string_encoding_method in os.listdir(path_encoding_methods):
        if string_encoding_method not in _LIST_PASS_METHODS and os.path.isdir(
                os.path.join(path_encoding_methods, string_encoding_method)):
            list_encoding_methods.append(string_encoding_method)

    list_results = []
    dict_same_files = {'Filename': [], 'Method': [], 'Similarity': []}
    list_original_files = os.listdir(path_original_data)
    int_total_runs = len(list_original_files) * len(list_encoding_methods) *\
        int_num_of_iteration
    # We list original files
    int_counter = 1
    for string_file in list_original_files:
        path_one_file = os.path.join(path_original_data, string_file)
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
                        string_file, int_file_size_bytes)

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
        df_detail_concat.to_pickle(path_existing_detail)
        df_summary_concat = pd.concat(
            [df_new_summary, df_existing_summary], ignore_index=True)
        df_summary_concat.to_pickle(path_existing_summary)

        if os.path.exists(path_existing_detail) and os.path.exists(
                path_existing_summary):
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
