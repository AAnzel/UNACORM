import os
import pandas as pd
import time
import string
import numpy as np
import bitarray as ba
import streamlit as st
from pathlib import Path

# Importing Encodings
import xor_code_python as encoding_xor
from Encodings.The2DCode.encoder import api as api_encoding_2d
from Encodings.SimpleCode.src import transform as encoding_simple
from Encodings.RepetitionCode.src import transform as encoding_repetition
from Encodings.NOREC4DNA import unified_dna_lt as encoding_lt
from Encodings.NOREC4DNA import unified_dna_online as encoding_online # Include this one # noqa
from Encodings.NOREC4DNA import unified_dna_raptor as encoding_raptor # Include this one # noqa

encoding_2d = api_encoding_2d()  # We have to initialize the constructor


# Defining paths for important files and directories
path_root_data = os.path.join('..', 'Data')
path_original_data = os.path.join(path_root_data, 'Original', 'Test')  # after test, 'Test' at the end should be removed
path_original_decoded = os.path.join(path_root_data, 'Original', 'decoded')
path_encoded_data = os.path.join(path_root_data, 'Encoded_DNA')
path_decoded_data = os.path.join(path_root_data, 'Decoded_DNA')
path_encoded_dna = os.path.join(path_root_data, 'Encoded_DNA', 'DNA')
path_decoded_dna = os.path.join(path_root_data, 'Decoded_DNA', 'DNA')
path_existing_detail = os.path.join('data', 'pre_measure.pkl')
path_existing_summary = os.path.join('data', 'pre_measure_stat.pkl')
df_existing_detail = pd.read_pickle(path_existing_detail)
df_existing_summary = pd.read_pickle(path_existing_summary)
path_encoding_methods = os.path.join('Encodings')

existing_encoding = []
for encoding_method in os.listdir(path_encoding_methods):
    existing_encoding.append(encoding_method)

df_metrics = pd.read_csv(os.path.join(path_root_data, 'synthesis_cost.csv'))

# ============================================================================
# Function definitions start here
# ============================================================================


def cost_encoding(max_nt, oligos):
    """This function is used for calculating synthesizing cost

    Args:
        max_nt (int): max nucleutide from dna sequences
        oligos (int): number of oligos

    Returns:
        cost_total (number): synthesising cost
    """
    if max_nt <= 120:
        i = 0
    else:
        i = 1

    if oligos >= 2 and oligos <= 100:
        j = 1
    elif oligos >= 101 and oligos <= 500:
        j = 2
    elif oligos >= 501 and oligos <= 1000:
        j = 3
    else:
        j = 4

    cost = df_metrics.iloc[i, j]
    cost_total = cost * oligos

    return cost_total


def encoding(encoding_method, binary, file_basename, save_path):
    """This function is used for encoding the binary

    Args:
        encoding_method (str): chosen encoding method
        binary (array): binary sequence of uploaded file
        file_basename (str): name of file that contains timestamp
        save_path (str): path of original uploaded file

    Returns:
        generated_seq (list): encoded dna list
        numblocks (int): number of blocks from 2D Code that will be used for decoding
    """
    numblocks = 0
    if encoding_method == 'The2DCode':
        generated_seq = encoding_2d.encode('', binary)
    elif encoding_method == 'XORBasedCode':
        generated_seq = encoding_xor.encode('', binary)
    elif encoding_method == 'SimpleCode':
        generated_seq = encoding_simple.encode('', binary)
    elif encoding_method == 'RepetitionCode':
        generated_seq = encoding_repetition.encode('', binary)
    elif encoding_method == 'NOREC4DNA':
        generated_seq = encoding_lt.encode(save_path, binary)[0]
    else:
        pass
    return generated_seq, numblocks


def check_text_equal(path_original_file, path_decoded_file):
    """This function is used for checking if the original file is equal than generated decoded file

    Args:
        path_original_file (str): path of original uploaded file
        path_decoded_file (str): path of generated decoded file

    Returns:
        status (str): the result of comparison (Same or Different)
    """
    if os.path.isfile(path_original_file):
        with open(path_original_file, 'rb') as fd_original_file, \
                open(path_decoded_file, 'rb') as fd_decoded_file:
            binary_array_original = ba.bitarray()
            binary_array_decoded = ba.bitarray()

            binary_array_original.fromfile(fd_original_file)
            binary_array_decoded.fromfile(fd_decoded_file)

            binary_numpy_original = np.frombuffer(
                binary_array_original.unpack(), dtype=bool)
            binary_numpy_decoded = np.frombuffer(
                binary_array_decoded.unpack(), dtype=bool)

            status = ''
            if np.array_equal(binary_numpy_original, binary_numpy_decoded):
                status = 'Same'
            else:
                status = 'Different'

    return status


def compare2ori(save_path, decoded_path, encoding_method, binary, decoded_seq):
    """This function is used for specifying condition of comparison for different encoding method

    Args:
        save_path (string): path of uploaded file
        decoded_path (strung): path of generated decoded file
        encoding_method (str): chosen encoding method
        binary (array): binary array of uploaded file
        decoded_seq (array): binary array of generated decoded file

    Returns:
        status (str): result of comparison (Same or Different)
    """
    if encoding_method == 'The2DCode':
        status = check_text_equal(save_path, decoded_path)
    else:
        if len(binary) == len(decoded_seq):
            i = 0
            status = 'Same'
            while i < len(binary) and status == 'Same':
                if binary[i] == decoded_seq[i]:
                    status = 'Same'
                else:
                    status = 'Different'
                i += 1
        else:
            status = 'Different'

    return status


def pipeline(encoding_method, binary, file_basename, file_type, save_path, original_size):
    """This function is used for integrating the process for uploaded file

    Args:
        encoding_method (str): chosen encoding method
        binary (array): numpy binary array of uploaded file
        file_basename (str): name of file
        file_type (str): file extension
        save_path (str): path of uploaded data
        original_size (number): size of original file

    Returns:
        list_encoded [list]: list of result from encoding process including time, cost, and size
        list_decoded [list]: list of result from decoding process including time, cost, and size
    """
    start_time = time.time()
    enc_output = encoding(encoding_method, binary, file_basename, save_path)
    time_used = time.time() - start_time
    generated_seq = enc_output[0]
    len_oligos = len(generated_seq)
    max_nt = 0
    generated_seq_upper = []
    for seq in generated_seq:
        nt = len(seq.translate({ord(c): None for c in string.whitespace}))
        generated_seq_upper.append(seq.upper())
        if nt > max_nt:
            max_nt = nt
    print('len_oligos = ' + str(len_oligos) + ' max_nt = ' + str(max_nt))
    cost = cost_encoding(max_nt, len_oligos)

    file_name = file_basename + '_' + encoding_method + '.txt'

    file_path = os.path.join(path_encoded_dna, file_name)
    with open(file_path, 'w') as f:
        f.writelines(generated_seq)

    encoded_size = os.path.getsize(file_path)
    list_encoded = [file_basename, encoding_method, 'Encoding', '.'+file_type, encoded_size, cost, time_used,
                    original_size]

    modified_sequence = []
    i = 0
    modified_sequence = generated_seq

    file_path = os.path.join(path_decoded_dna, file_name)
    with open(file_path, 'w') as f:
        for i in modified_sequence:
            f.write(i)

    size = os.path.getsize(file_path)

    start_time = time.time()
    if encoding_method == 'The2DCode':
        decoded_seq = encoding_2d.decode('', modified_sequence)
    elif encoding_method == 'XORBasedCode':
        decoded_seq = encoding_xor.decode('', modified_sequence)
    elif encoding_method == 'SimpleCode':
        decoded_seq = encoding_simple.decode('', modified_sequence)
    elif encoding_method == 'RepetitionCode':
        decoded_seq = encoding_repetition.decode('', modified_sequence)
    elif encoding_method == 'NOREC4DNA':
        decoded_seq = encoding_lt.decode(save_path, modified_sequence)[0]
    else:
        pass

    time_used = time.time() - start_time
    cost = 0

    print(encoding_method)

    file_name = file_basename + '_' + encoding_method + '.npy'

    file_path = os.path.join(path_decoded_data, file_name)
    np.save(file_path, decoded_seq)
    list_decoded = [file_basename, encoding_method, 'Decoding', '.'+file_type, size, cost, time_used, original_size]
    return list_encoded, list_decoded


def generate_summary(encoding_method, binary, file_basename, file_type, save_path, path):
    """This function is used for generating summary dataframe from detail dataframe (from 10 times running pipeline)

    Args:
        encoding_method (str): chosen encoding method
        binary (array): numpy binary array of uploaded file
        file_basename (str): name of file
        file_type (str): file extension
        storage_length (int): chosen length of storage in hour
        save_path (str): path of uploaded data
        path (str): path of evaluated file

    Returns:
        _type_: _description_
    """
    df = df_report[(df_report['Filename'] == file_basename) & (df_report['Method'] == encoding_method) &
                   (df_report['Type'] == '.'+file_type)]
    original_size = os.path.getsize(path)
    encoded_file_name = file_basename + '_' + encoding_method + '.txt'
    encoded_path = os.path.join(path_encoded_dna, encoded_file_name)
    encoded_size = os.path.getsize(encoded_path)
    decoded_file_name = file_basename + '_' + encoding_method + '.npy'
    decoded_binary_path = os.path.join(path_decoded_data, decoded_file_name)
    decoded_seq = np.load(decoded_binary_path)
    decoded_path = os.path.join(path_original_decoded, file_basename + '_' + encoding_method + '.' + file_type)
    status = compare2ori(save_path, decoded_path, encoding_method, binary, decoded_seq)
    df_agg = df.groupby(['Filename', 'Method', 'Transformation', 'Type']).agg({'Time': 'mean', 'Size': 'mean', 'Cost':
                                                                               'mean'}).reset_index()
    df_agg_sum = df_agg.groupby(['Filename', 'Method', 'Type']).agg({'Time': 'sum', 'Size': 'sum', 'Cost': 'sum'})\
        .reset_index()
    df_agg_sum.rename(columns={'Time': 'Sum_Mean_Time', 'Size': 'Sum_Size', 'Cost': 'Sum_Cost'}, inplace=True)
    df_agg_sum['Encoding_Multipliers'] = encoded_size/original_size
    df_agg_sum['Similarity'] = status
    print(df_agg_sum)
    return df_agg_sum


def convert_text_data_to_binary(path_original_data):
    """This function is used to convert data to binary

    Args:
        path_original_data (str): path of original uploaded file

    Returns:
        bit_encoded_file (str): path of generated binary from uploaded file
    """
    file_basename = os.path.basename(path_original_data)
    string_file_no_extension = os.path.splitext(file_basename)[0]
    encoded_filename = string_file_no_extension + ".npy"
    if os.path.isfile(path_original_data):
        with open(path_original_data, 'rb') as fd_file:
            binary_array_content = ba.bitarray()
            binary_array_content.fromfile(fd_file)
            binary_numpy_content = np.frombuffer(
                binary_array_content.unpack(), dtype=bool)

            np.save(os.path.join(path_encoded_data, string_file_no_extension), binary_numpy_content, allow_pickle=False)

    bit_encoded_file = os.path.join(path_encoded_data, encoded_filename)

    return bit_encoded_file


df_report = pd.DataFrame(columns=['Filename', 'Method', 'Transformation', 'Type', 'Size', 'Cost', 'Time',
                                  'OriFile_Size'])


def run_precalculation(num_of_iteration):
    """This function is used for running precalculation

    Args:
        num_of_iteration (int): number of iteration for each file
    """
    df_summary = pd.DataFrame(columns=['Filename', 'Method', 'Type', 'Sum_Mean_Time', 'Sum_Size', 'Sum_Cost',
                                       'Encoding_Multipliers', 'Similarity'])
    for list_file in os.listdir(path_original_data):
        path = os.path.join(path_original_data, list_file)
        if os.path.isfile(path):
            file_name = os.path.splitext(list_file)[0]
            file_ext = os.path.splitext(list_file)[1]
            file_type = file_ext[1:len(file_ext)]
            for encoding_method in existing_encoding:
                if len(df_existing_summary[(df_existing_summary["Filename"] == file_name) &
                                       (df_existing_summary["Method"] == encoding_method)]) == 0:
                    print(file_name, file_type, encoding_method)
                    path_original = os.path.join(path_original_data, list_file)
                    OriFileSize = os.path.getsize(path_original)
                    encoded_binary_path = convert_text_data_to_binary(path_original)
                    binary = np.load(encoded_binary_path)
                    i = 0
                    try:
                        while i < num_of_iteration:
                            output = pipeline(encoding_method, binary, file_name, file_type, path_original,
                                              OriFileSize)
                            list_encoded = output[0]
                            list_decoded = output[1]
                            # list_summary = output[2]
                            df_report.loc[len(df_report)] = list_decoded
                            df_report.loc[len(df_report)] = list_encoded
                            i += 1
                    except Exception as e:
                        print(e)
                        continue
                    df_summary_generated = generate_summary(encoding_method, binary, file_name, file_type,
                                                            path_original, path)
                    df_summary = pd.concat([df_summary, df_summary_generated], ignore_index=True)

    st.header('Recently calculated details')
    st.dataframe(df_report)
    st.header('Existed precalculated details')
    st.dataframe(df_existing_detail)

    st.header('Recently calculated summary')
    st.dataframe(df_summary)
    st.header('Existed precalculated summary')
    st.dataframe(df_existing_summary)
    st.write('Do you want to merge both new data into pickel file?')
    if st.button('Merge new data to pickel'):
        detail_concat = pd.concat([df_report, df_existing_detail], ignore_index=True)
        save_file_detail = Path('data/detail_updated.pkl')
        detail_concat.to_pickle(save_file_detail)  # path should be changed to 'data/pre_measure1.pkl'
        summary_concat = pd.concat([df_summary, df_existing_summary], ignore_index=True)
        save_file_summary = Path('data/summary_updated.pkl')  # should be changed to 'data/pre_measure_stat_sum1.pkl'
        summary_concat.to_pickle(save_file_summary)
        if save_file_detail.exists() and save_file_summary.exists():
            st.success('New data has been successfully merged')
            st.header('New Detail Data')
            new_summary = pd.read_pickle(save_file_summary)
            st.dataframe(new_summary)
            st.header('New Summary Data')
            new_summary = pd.read_pickle(save_file_summary)
            st.dataframe(new_summary)
        else:
            st.error('There was an error while uploading the pickel file')


run_precalculation(1)  # 2 times iteration
