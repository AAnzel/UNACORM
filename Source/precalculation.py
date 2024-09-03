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
path_original_data = os.path.join(path_root_data, 'Original', 'Test')  # TODO: Remove 'Test' # noqa
path_original_decoded = os.path.join(path_root_data, 'Original', 'decoded')
path_encoded_data = os.path.join(path_root_data, 'Encoded_DNA')
path_decoded_data = os.path.join(path_root_data, 'Decoded_DNA')
path_encoded_dna = os.path.join(path_root_data, 'Encoded_DNA', 'DNA')
path_decoded_dna = os.path.join(path_root_data, 'Decoded_DNA', 'DNA')
path_existing_detail = os.path.join('data', 'pre_measure.pkl')
path_existing_summary = os.path.join('data', 'pre_measure_stat.pkl')
path_encoding_methods = os.path.join('Encodings')

list_encoding_methods = []
list_pass_methods = ['NOREC4DNA', 'DNA-Aeon']
for string_encoding_method in os.listdir(path_encoding_methods):
    if string_encoding_method not in list_pass_methods and os.path.isdir(
            os.path.join(path_encoding_methods, string_encoding_method)):
        list_encoding_methods.append(string_encoding_method)

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
    i = 0 if max_nt <= 120 else 1

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
        generated_seq (list): encoded dna list
    """
    if bool_encode:
        if str_encoding_method == 'The2DCode':
            generated_seq = encoding_2d.encode('', list_np_data)
        elif str_encoding_method == 'XORBasedCode':
            generated_seq = encoding_xor.encode('', list_np_data)
        elif str_encoding_method == 'SimpleCode':
            generated_seq = encoding_simple.encode('', list_np_data)
        elif str_encoding_method == 'RepetitionCode':
            generated_seq = encoding_repetition.encode('', list_np_data)
        elif str_encoding_method == 'NOREC4DNA':  # ! Fix
            generated_seq = encoding_lt.encode(path_file, list_np_data)[0]
        else:
            pass
    else:
        if str_encoding_method == 'The2DCode':
            generated_seq = encoding_2d.decode('', list_np_data)
        elif str_encoding_method == 'XORBasedCode':
            generated_seq = encoding_xor.decode('', list_np_data)
        elif str_encoding_method == 'SimpleCode':
            generated_seq = encoding_simple.decode('', list_np_data)
        elif str_encoding_method == 'RepetitionCode':
            generated_seq = encoding_repetition.decode('', list_np_data)
        elif str_encoding_method == 'NOREC4DNA':  # ! Fix
            generated_seq = encoding_lt.decode(path_file, list_np_data)[0]
        else:
            pass

    return generated_seq


def check_text_equal(path_original_file, path_decoded_file):
    """This function is used for checking if the original file is equal as
    the processed decoded file

    Args:
        path_original_file (str): path of original file
        path_decoded_file (str): path of processed decoded file

    Returns:
        status (str): the result of comparison (Same or Different)
    """

    if not os.path.exists(path_original_file):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_original_file)
    if not os.path.exists(path_decoded_file):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_decoded_file)

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

            if np.array_equal(binary_numpy_original, binary_numpy_decoded):
                status = 'Same'
            else:
                status = 'Different'

    return status


def compare2ori(save_path, decoded_path, encoding_method, binary, decoded_seq):
    """This function is used for specifying condition of comparison for
    different encoding method

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


def pipeline(encoding_method, binary, file_basename, string_file_extension,
             save_path, original_size):
    """This function is used for integrating the process for one file

    Args:
        encoding_method (str): chosen encoding method
        binary (array): numpy binary array of uploaded file
        file_basename (str): name of file
        string_file_extension (str): file extension
        save_path (str): path of uploaded data
        original_size (number): size of original file

    Returns:
        list_encoded [list]: list of result from encoding process including
        time, cost, and size
        list_decoded [list]: list of result from decoding process including
        time, cost, and size
    """
    int_start_time = time.time()
    generated_seq = list_encode_decode(encoding_method, binary, save_path,
                                       True)
    int_time_used = time.time() - int_start_time

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

    string_file_name = file_basename + '_' + encoding_method + '.txt'

    file_path = os.path.join(path_encoded_dna, string_file_name)
    with open(file_path, 'w') as f:
        f.writelines(generated_seq)

    encoded_size = os.path.getsize(file_path)
    list_encoded = [
        file_basename, encoding_method, 'Encoding',
        '.' + string_file_extension, encoded_size, cost, int_time_used,
        original_size]

    modified_sequence = []
    i = 0
    modified_sequence = generated_seq

    file_path = os.path.join(path_decoded_dna, string_file_name)
    with open(file_path, 'w') as f:
        for i in modified_sequence:
            f.write(i)

    size = os.path.getsize(file_path)

    start_time = time.time()
    decoded_seq = list_encode_decode(encoding_method, modified_sequence,
                                     save_path, False)
    time_used = time.time() - start_time

    cost = 0
    string_file_name = file_basename + '_' + encoding_method + '.npy'

    file_path = os.path.join(path_decoded_data, string_file_name)
    np.save(file_path, decoded_seq)
    list_decoded = [
        file_basename, encoding_method, 'Decoding',
        '.' + string_file_extension, size, cost, time_used, original_size]

    return list_encoded, list_decoded


def generate_summary(df_report, encoding_method, binary, file_basename,
                     string_file_extension, save_path, path):
    """This function is used for generating summary dataframe from detail
    dataframe (from 10 times running pipeline)

    Args:
        df_report (DataFrame): detailed df containing previous runs of one
        encoding method
        encoding_method (str): chosen encoding method
        binary (array): numpy binary array of uploaded file
        file_basename (str): name of file
        string_file_extension (str): file extension
        storage_length (int): chosen length of storage in hour
        save_path (str): path of uploaded data
        path (str): path of evaluated file

    Returns:
        _type_: _description_
    """
    df = df_report[
        (df_report['Filename'] == file_basename) &
        (df_report['Method'] == encoding_method) &
        (df_report['Type'] == '.' + string_file_extension)]
    original_size = os.path.getsize(path)
    encoded_string_file_name = file_basename + '_' + encoding_method + '.txt'
    encoded_path = os.path.join(path_encoded_dna, encoded_string_file_name)
    encoded_size = os.path.getsize(encoded_path)
    decoded_string_file_name = file_basename + '_' + encoding_method + '.npy'
    decoded_binary_path = os.path.join(path_decoded_data,
                                       decoded_string_file_name)
    decoded_seq = np.load(decoded_binary_path)
    decoded_path = os.path.join(
        path_original_decoded,
        file_basename + '_' + encoding_method + '.' + string_file_extension)
    status = compare2ori(save_path, decoded_path, encoding_method, binary,
                         decoded_seq)
    df_agg = df.groupby(
        ['Filename', 'Method', 'Transformation', 'Type']).agg(
            {'Time': 'mean', 'Size': 'mean', 'Cost': 'mean'}).reset_index()
    df_agg_sum = df_agg.groupby(
        ['Filename', 'Method', 'Type']).agg(
            {'Time': 'sum', 'Size': 'sum', 'Cost': 'sum'}).reset_index()
    df_agg_sum.rename(
        columns={'Time': 'Sum_Mean_Time', 'Size': 'Sum_Size',
                 'Cost': 'Sum_Cost'}, inplace=True)
    df_agg_sum['Encoding_Multipliers'] = encoded_size / original_size
    df_agg_sum['Similarity'] = status
    print(df_agg_sum)
    return df_agg_sum


def np_data_to_bitarray(path_original_file):
    """This function is used to convert data to binary

    Args:
        path_original_file (os.path): path of the original file

    Returns:
        binary_numpy_content (np.array): bit array representing the original
        file
    """
    if os.path.isfile(path_original_file):
        with open(path_original_file, 'rb') as fd_file:
            binary_array_content = ba.bitarray()
            binary_array_content.fromfile(fd_file)
            binary_numpy_content = np.frombuffer(
                binary_array_content.unpack(), dtype=bool)

    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_original_file)

    return binary_numpy_content


def run_precalculation(int_num_of_iteration):
    """This function is used for running precalculation

    Args:
        num_of_iteration (int): number of iteration for each file
    """
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

    df_summary = pd.DataFrame(
        columns=['Filename', 'Method', 'Type', 'Sum_Mean_Time', 'Sum_Size',
                 'Sum_Cost', 'Encoding_Multipliers', 'Similarity'])
    df_report = pd.DataFrame(
        columns=['Filename', 'Method', 'Transformation', 'Type', 'Size',
                 'Cost', 'Time', 'OriFile_Size'])

    # We list original files
    for string_file in os.listdir(path_original_data):
        path_one_file = os.path.join(path_original_data, string_file)

        if not os.path.isfile(path_one_file):
            continue

        string_file_name = os.path.splitext(string_file)[0]
        string_file_extension = os.path.splitext(string_file)[1][1:]

        for string_encoding_method in list_encoding_methods:
            # We check if we already processed the file with a specific
            # encoding method
            bool_file_is_processed = len(
                df_existing_summary[
                    (df_existing_summary["Filename"] == string_file_name) &
                    (df_existing_summary["Method"] == string_encoding_method)]
                ) != 0

            if not bool_file_is_processed:
                print(string_file_name, string_file_extension,
                      string_encoding_method)

                OriFileSize = os.path.getsize(path_one_file)
                np_binary_encoding = np_data_to_bitarray(path_one_file)

                for int_i in range(int_num_of_iteration):
                    output = pipeline(
                        string_encoding_method, np_binary_encoding,
                        string_file_name, string_file_extension, path_one_file,
                        OriFileSize)
                    list_encoded = output[0]
                    list_decoded = output[1]
                    # list_summary = output[2]
                    df_report.loc[len(df_report)] = list_decoded
                    df_report.loc[len(df_report)] = list_encoded

                df_one_encoding_method_summary = generate_summary(
                    df_report, string_encoding_method, np_binary_encoding,
                    string_file_name, string_file_extension, path_one_file,
                    path_one_file)
                df_summary = pd.concat(
                    [df_summary, df_one_encoding_method_summary],
                    ignore_index=True)

    st.header('Recently calculated details')
    st.dataframe(df_report)
    st.header('Existed precalculated details')
    st.dataframe(df_existing_detail)

    st.header('Recently calculated summary')
    st.dataframe(df_summary)
    st.header('Existed precalculated summary')
    st.dataframe(df_existing_summary)
    st.write('Do you want to merge both new data into pickle file?')
    if st.button('Merge new data to pickel'):
        detail_concat = pd.concat([df_report, df_existing_detail],
                                  ignore_index=True)
        detail_concat.to_pickle(path_existing_detail)
        summary_concat = pd.concat([df_summary, df_existing_summary],
                                   ignore_index=True)
        summary_concat.to_pickle(path_existing_summary)
        if os.path.exists(path_existing_detail) and os.path.exists(
                path_existing_summary):
            st.success('New data has been successfully merged')
            st.header('New Summary Data')
            st.dataframe(pd.read_pickle(path_existing_summary))
            st.header('New Detail Data')
            st.dataframe(pd.read_pickle(path_existing_detail))
        else:
            st.error('There was an error while uploading the pickle file')


def main():
    run_precalculation(1)  # 2 times iteration


if __name__ == '__main__':
    main()
