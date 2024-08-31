import os
import time
import string
import shutil
import importlib
import bitarray as ba
import pandas as pd
import numpy as np
import streamlit as st

import xor_code_python as xor
import Encodings.The2DCode as code_2d

import mesa_call

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

# List of name of files for showing charts in benchmarking
data_original = []
for file_name in os.listdir(path_original_data):
    path = os.path.join(path_original_data, file_name)
    if os.path.isfile(path):
        data_original.append(os.path.splitext(file_name)[0])


constructor_2d_code = code_2d.encoder.api()


def remove_cached_data():
    """This function is used for deleting old uploaded files by user that was
    uploaded older than 1 hour ago.
    """

    SAVE_TIME = 3600  # 3600 seconds = 1h
    time_limit = time.time() - SAVE_TIME
    # List of directories for uploaded file
    path_uploaded_list = [
        path_uploaded_txt, path_uploaded_jpg, path_uploaded_wav,
        path_encoded_data, path_decoded_data, path_encoded_dna,
        path_decoded_dna, path_uploaded_decoded]

    # Traversing directories for uploaded files and deleting everything from it
    for dir in path_uploaded_list:
        for file_name in os.listdir(dir):
            path = os.path.join(dir, file_name)
            if 'gitkeep' in file_name or os.path.isdir(path):
                continue
            else:
                file_path = os.path.join(dir, file_name)

                # Check if file is older than 1h, and if yes, delete it
                if os.stat(file_path).st_mtime < time_limit:
                    try:
                        if os.path.isfile(file_path) or\
                                os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except OSError as e:
                        print('Failed to delete ' + file_path + '. Reason: '
                              + e)

                    print('Successfully removed old data from uploaded' +
                          ' directory')
                else:
                    pass


@st.cache_data
def cost_encoding(max_nucleotide, oligos):
    """This function is used for calculating synthesizing cost

    Args:
        max_nucleotide (int): max nucleutide from dna sequences
        oligos (int): number of oligos

    Returns:
        cost_total (number): synthesising cost
    """
    # Based file for calculating synthesis cost
    df_metrics = pd.read_csv(
        os.path.join(path_root_data, 'synthesis_cost.csv'))

    if max_nucleotide <= 120:
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


@st.cache_data
def encoding(encoding_method, binary, file_basename, save_path):
    """This function is used for encoding the binary

    Args:
        encoding_method (str): chosen encoding method
        binary (array): binary sequence of uploaded file
        file_basename (str): name of file that contains timestamp
        save_path (str): path of original uploaded file

    Returns:
        generated_seq (list): encoded dna list
        numblocks (int): number of blocks from 2D Code that will be used for
        decoding
    """
    numblocks = 0
    if encoding_method == 'The2DCode':
        generated_seq = constructor_2d_code.encode('', binary)
    elif encoding_method == 'XORBasedCode':
        generated_seq = xor.encode('', binary)
    else:
        method = importlib.import_module(
            f'Encodings.{encoding_method}.src.transform')
        generated_seq = method.encode('', binary)

    return generated_seq, numblocks


def check_text_equal(path_original_file, path_decoded_file):
    """This function is used for checking if the original file is equal than
    generated decoded file

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


@st.cache_data
def pipeline(encoding_method, binary, file_basename, file_type, storage_length,
             save_path, uploaded_filename):
    """This function is used for integrating the process for uploaded file

    Args:
        encoding_method (str): chosen encoding method
        binary (array): numpy binary array of uploaded file
        file_basename (str): name of file that contains timestamp
        file_type (str): file extension
        storage_length (int): chosen length of storage in hour
        save_path (str): path of uploaded data
        uploaded_filename (str): uploaded file name without timestamp and
        extension

    Returns:
        list_encoded [list]: list of result from encoding process including
        time, cost, and size
        list_decoded [list]: list of result from decoding process including
        time, cost, and size
        list_summary [list]: list of summary from encoding and decoding process
    """
    start_time = time.time()
    enc_output = encoding(encoding_method, binary, file_basename, save_path)
    time_used = time.time() - start_time  # getting length of encoding process
    generated_seq = enc_output[0]
    # numblocks = enc_output[1]
    len_oligos = len(generated_seq)
    max_nucleotide = 0
    generated_seq_upper = []
    # getting maximum nucleotide
    for seq in generated_seq:
        # nucleotide is nt
        nt = len(seq.translate({ord(c): None for c in string.whitespace}))
        generated_seq_upper.append(seq.upper())
        if nt > max_nucleotide:
            max_nucleotide = nt
    print('len_oligos = ' + str(len_oligos) + ' max_nucleotide = ' +
          str(max_nucleotide))
    cost = cost_encoding(max_nucleotide, len_oligos)

    file_name = file_basename + '_' + encoding_method + '.txt'
    file_path = os.path.join(path_encoded_dna, file_name)

    with open(file_path, 'w') as f:
        f.writelines(generated_seq_upper)

    encoded_size = os.path.getsize(file_path)
    list_encoded = [uploaded_filename, encoding_method, 'Encoding',
                    encoded_size, cost, time_used, '.' + file_type]

    modified_sequence = []
    i = 0
    while i < len(generated_seq_upper):
        seq = [str(generated_seq_upper[i])]
        result = mesa_call.api_call(seq, storage_length)
        modified_sequence.append(result)
        i += 1

    file_path = os.path.join(path_decoded_dna, file_name)
    with open(file_path, 'w') as f:
        for i in modified_sequence:
            f.write(i)

    size = os.path.getsize(file_path)

    decoded_path = ''
    start_time = time.time()
    if encoding_method == 'The2DCode':
        decoded_seq = constructor_2d_code.decode('', modified_sequence)
    elif encoding_method == 'XORBasedCode':
        decoded_seq = xor.decode('', modified_sequence)
    elif encoding_method == 'SimpleCode':
        method = importlib.import_module(
            f'Encodings.{encoding_method}.src.transform')
        decoded_seq = method.decode('', modified_sequence)
    else:
        pass

    time_used = time.time() - start_time
    cost = 0

    file_name = file_basename + '_' + encoding_method + '.npy'

    file_path = os.path.join(path_decoded_data, file_name)
    np.save(file_path, decoded_seq)
    list_decoded = [uploaded_filename, encoding_method, 'Decoding', size,
                    cost, time_used, '.' + file_type]

    status = compare2ori(save_path, decoded_path, encoding_method, binary,
                         decoded_seq)
    sum_size = list_encoded[3] + list_decoded[3]
    sum_cost = list_encoded[4] + list_decoded[4]
    sum_time_used = list_encoded[5] + list_decoded[5]
    # summary list
    list_summary = [uploaded_filename, encoding_method, sum_size, sum_cost,
                    sum_time_used, '.'+file_type, status, encoded_size]
    if uploaded_filename not in data_original:
        data_original.append(uploaded_filename)
    return list_encoded, list_decoded, list_summary


def convert_text_data_to_binary(path_original_data):
    """This function is used to convert data to binary

    Args:
        path_original_data (str): path of original uploaded file

    Returns:
        bit_encoded_file (str): path of generated binary from uploaded file
    """
    # If we have a file, we convert it into numpy byte file (.npy)
    file_basename = os.path.basename(path_original_data)
    string_file_no_extension = os.path.splitext(file_basename)[0]
    encoded_filename = string_file_no_extension + ".npy"
    if os.path.isfile(path_original_data):
        with open(path_original_data, 'rb') as fd_file:
            binary_array_content = ba.bitarray()
            binary_array_content.fromfile(fd_file)
            binary_numpy_content = np.frombuffer(
                binary_array_content.unpack(), dtype=bool)

            np.save(os.path.join(path_encoded_data, string_file_no_extension),
                    binary_numpy_content, allow_pickle=False)

    bit_encoded_file = os.path.join(path_encoded_data, encoded_filename)

    return bit_encoded_file
