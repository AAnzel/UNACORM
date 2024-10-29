import os
import errno
import shutil
import time
import numpy as np
import bitarray as ba
import streamlit as st

# Importing Encodings
import xor_code_python as encoding_xor
from Encodings.The2DCode import encoder as encoding_2d_tmp
from Encodings.SimpleCode.src import transform as encoding_simple
from Encodings.RepetitionCode.src import transform as encoding_repetition
from Encodings.RaptorCode import unified_dna_lt as encoding_lt
from Encodings.RaptorCode import unified_dna_online as encoding_online
from Encodings.RaptorCode import unified_dna_raptor as encoding_raptor
from Encodings.DNA_Aeon import unified as encoding_dnaaeon

# Importing MESA
import mesa_call


__author__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian']
__copyright__ = ''
__credits__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian', 'Chisom Ezekannagha']
__license__ = 'GNU General Public License v3.0'
__version__ = '1.0.0'
__maintainer__ = 'Aleksandar Anžel'
__email__ = 'AnzelA@rki.de'
__status__ = 'Stable'


# Defining paths for important files and directories
PATH_ROOT_DATA = os.path.join('..', 'Data')
PATH_ORIGINAL_DATA = os.path.join(PATH_ROOT_DATA, 'Original', 'Test')  # TODO: Remove 'Test' # noqa
PATH_CACHE_DATA = os.path.join(PATH_ROOT_DATA, 'cache_data')
PATH_EXISTING_DETAIL = os.path.join(PATH_CACHE_DATA, 'pre_detail.pkl')
PATH_EXISTING_SUMMARY = os.path.join(PATH_CACHE_DATA, 'pre_summary.pkl')
_PATH_ORIGINAL_TRANSLATED = os.path.join(
    PATH_ROOT_DATA, 'Translated_Binary')  # This is where we keep boolean
# representations of the original data
_PATH_ENCODED_DATA = os.path.join(PATH_ROOT_DATA, 'Encoded')
_PATH_DECODED_DATA = os.path.join(PATH_ROOT_DATA, 'Decoded')
_PATH_UPLOADED_DATA = os.path.join(PATH_ROOT_DATA, 'Uploaded')
_PATH_ENCODING_METHODS = os.path.join('Encodings')

_UPLOADED_SAVE_TIME = 3600  # 3600 seconds = 1h
_INT_SEQUENCING_COVERAGE = 100
encoding_2d = encoding_2d_tmp.api()

_LIST_PASS_METHODS = []
LIST_ENCODING_METHODS = []
for string_encoding_method in os.listdir(_PATH_ENCODING_METHODS):
    if string_encoding_method not in _LIST_PASS_METHODS and os.path.isdir(
            os.path.join(_PATH_ENCODING_METHODS, string_encoding_method)):
        LIST_ENCODING_METHODS.append(string_encoding_method)


def remove_cached_data():
    """
    remove_cached_data function removes all data that was previously created
    while running the dashboard

    Returns:
        None
    """

    time_limit = time.time() - _UPLOADED_SAVE_TIME
    list_directories_to_clean = [_PATH_UPLOADED_DATA, _PATH_ENCODED_DATA,
                                 _PATH_DECODED_DATA, _PATH_ORIGINAL_TRANSLATED]

    # Traversing directories and deleting everything from them
    for path_dir in list_directories_to_clean:
        for string_file in os.listdir(path_dir):
            path_file = os.path.join(path_dir, string_file)

            if 'gitkeep' in string_file or os.path.isdir(path_file):
                continue
            else:
                # Check if file is older than 1h, and if yes, delete it
                if os.stat(path_file).st_mtime < time_limit:
                    try:
                        if os.path.isfile(path_file) or\
                                os.path.islink(path_file):
                            os.unlink(path_file)
                        elif os.path.isdir(path_file):
                            shutil.rmtree(path_file)
                    except OSError as e:
                        print('Failed to delete ' + path_file + '. Reason: '
                              + str(e))
                    #  print('Successfully removed old data from uploaded' +
                    #        ' directory')
                else:
                    pass
    return None


@st.cache_data
def float_calculate_encoding_cost(list_dna_sequences):
    """
    float_calculate_encoding_cost function calculates synthesis cost

    The function takes a list of DNA sequences and calculates the cost of
    synthesis according to their structure and the Twist Bioscience's cost
    model.

    Args:
        list_dna_sequences (list): list of string DNA sequences

    Returns:
        float: calculated cost in US dollars
    """
    # Total Cost = (For Each Oligo) x (Length per Oligo) x (Cost per Base)
    # Cost per Base = $0.10 per base
    # Bulk Discount: 10% discount for orders exceeding 100,000 bases

    float_cost_per_base = 0.1
    int_total_base_pairs = sum([len(string_dna_sequence.strip())
                                for string_dna_sequence in
                                list_dna_sequences])
    float_cost_total = int_total_base_pairs * float_cost_per_base

    if int_total_base_pairs > 100000:
        float_cost_total *= 0.9

    return float_cost_total


@st.cache_data
def float_calculate_decoding_cost(
        list_dna_sequences, string_technology='PacBio',
        int_sequencing_coverage=_INT_SEQUENCING_COVERAGE):
    """
    float_calculate_decoding_cost function calculates sequencing cost

    The function takes a list of DNA sequences and calculates the cost of
    sequencing according to their structure, chosen sequencing technology,
    and the fixed set of costs saved in an external file.

    Args:
        list_dna_sequences (list): list of string DNA sequences
        string_technology (string): sequencing technology

    Returns:
        int: calculated cost in US dollars
    """
    # To calculate sequence cost per base pair:
    # Total Cost = Total Base Pairs x Cost per Base Pair (depending on
    # technology)
    # Where Total Base Pairs = For each oligo x
    #                          Length of each oligo (number of nucleotides) x
    #                          Coverage
    #
    # Illumina: 0.000015
    # Nanopore: 0.000025
    # PacBio:   0.000035

    float_cost_per_base = 0
    if string_technology == 'Illumina':
        float_cost_per_base = 0.000015
    elif string_technology == 'Nanopore':
        float_cost_per_base = 0.000025
    elif string_technology == 'PacBio':
        float_cost_per_base = 0.000035
    else:
        raise RuntimeError('ERROR: Bad technology string for sequencing!')

    int_total_base_pairs = sum([len(string_dna_sequence.strip())
                                for string_dna_sequence in
                                list_dna_sequences]) * int_sequencing_coverage
    float_cost_total = int_total_base_pairs * float_cost_per_base

    return float_cost_total


@st.cache_data
def list_encode_decode(str_encoding_method, list_np_data, path_file,
                       bool_encode):
    """
    list_encode_decode function encodes or decodes the data using all encoding
    methods

    Args:
        str_encoding_method (str): chosen encoding method
        list_np_data (list or np.array): list of string DNA sequence if
        encoding or numpy array of binary data when decoding
        path_file (os.path): path of the original un-encoded file
        bool_encode (bool): if True, encoding is performed, if False then
        decoding

    Returns:
        list_generated_seq (list): encoded DNA list if encoding, or numpy
        boolean array if decoding
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
        elif str_encoding_method == 'OnlineCode':  # ! Fix
            list_generated_seq = encoding_online.encode(
                path_file, list_np_data)[0]
        elif str_encoding_method == 'LTCode':  # ! Fix
            list_generated_seq = encoding_lt.encode(
                 path_file, list_np_data)[0]
        elif str_encoding_method == 'RaptorCode':
            list_generated_seq = encoding_raptor.encode(
                path_file, list_np_data)[0]
        elif str_encoding_method == 'DNA_Aeon':
            list_generated_seq = encoding_dnaaeon.encode(
                path_file, '')
        else:
            print('Encoding method ' + str_encoding_method +
                  ' is not implemented')
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
        elif str_encoding_method == 'OnlineCode':  # ! Fix
            list_generated_seq = encoding_online.decode(
                path_file, list_np_data)
        elif str_encoding_method == 'LTCode':  # ! Fix
            list_generated_seq = encoding_lt.decode(
                 path_file, list_np_data)
        elif str_encoding_method == 'RaptorCode':
            list_generated_seq = encoding_raptor.decode(
                path_file, list_np_data)
        elif str_encoding_method == 'DNA_Aeon':
            list_generated_seq = encoding_dnaaeon.decode(
                '', list_np_data)
        else:
            print('Encoding method ' + str_encoding_method +
                  ' is not implemented')
            pass

    return list_generated_seq


@st.cache_data
def tuple_pipeline(string_encoding_method, np_bit_array, path_input_file,
                   string_file_name, int_original_size, bool_simulate_error,
                   int_storage_length):
    """
    tuple_pipeline function is used for integrating the encoding/decoding
    process for one file

    Args:
        string_encoding_method (str): chosen encoding method
        np_bit_array (array): numpy boolean array of uploaded file
        path_input_file (str): path of uploaded data
        string_file_name (str): the base name of the file with extension
        int_original_size (number): size of original file
        bool_simulate_error (bool): if True, MESA call is invoked and error
        simulation initiated. If False, DNA sequences are not modified
        int_storage_length (int): number of years for simulating DNA
        degradation. Used only if bool_simulate_error is True

    Returns:
        list_encoded (list): list of result from encoding process including
        time, cost, and size
        list_decoded (list): list of result from decoding process including
        time, cost, and size
        np_decoded_dna_sequences (np.array): numpy boolean array containing
        decoded sequences
    """
    string_input_file_basename = os.path.splitext(string_file_name)[0]
    string_file_extension = os.path.splitext(string_file_name)[1][1:]

    # We time the encoding process
    int_start_time = time.time()
    list_dna_sequences = list_encode_decode(
        string_encoding_method, np_bit_array, path_input_file, True)
    int_time_encoding = time.time() - int_start_time

    list_dna_sequences = [string_dna.upper()
                          for string_dna in list_dna_sequences]

    int_cost_encoding = float_calculate_encoding_cost(list_dna_sequences)

    string_encoded_file_name = string_input_file_basename + '_' + \
        string_encoding_method + '.txt'
    path_encoded_file = os.path.join(_PATH_ENCODED_DATA,
                                     string_encoded_file_name)
    with open(path_encoded_file, 'w') as f:
        f.writelines(string_dna + '\n' for string_dna in list_dna_sequences)

    int_encoded_file_size = os.path.getsize(path_encoded_file)

    list_encoded = [
        string_input_file_basename, string_encoding_method, 'Encoding',
        '.' + string_file_extension, int_encoded_file_size, int_cost_encoding,
        int_time_encoding, int_original_size]

    list_modified_sequences = []
    if not bool_simulate_error:
        list_modified_sequences = list_dna_sequences
    else:
        string_progress_text = ''
        st_progress_bar = st.progress(0, text=string_progress_text)
        int_num_of_sequences = len(list_dna_sequences)
        for int_i in range(int_num_of_sequences):
            st_progress_bar.progress(
                (int_i + 1) / int_num_of_sequences,
                text=('Sequence ' + str(int_i + 1) + ' of ' +
                      str(int_num_of_sequences)))
            list_modified_sequences.append(
                mesa_call.string_api_call([list_dna_sequences[int_i]],
                                          int_storage_length))
        st_progress_bar.empty()

    # We time the decoding process
    int_start_time = time.time()
    np_decoded_dna_sequences = list_encode_decode(
        string_encoding_method, list_modified_sequences, path_input_file,
        False)
    int_time_decoding = time.time() - int_start_time

    int_cost_decoding = float_calculate_decoding_cost(list_dna_sequences)
    string_decoded_file_name = string_input_file_basename + '_' + \
        string_encoding_method + '.npy'

    path_decoded_file = os.path.join(_PATH_DECODED_DATA,
                                     string_decoded_file_name)
    np.save(path_decoded_file, np_decoded_dna_sequences)
    int_decoded_file_size = os.path.getsize(path_decoded_file)

    list_decoded = [
        string_input_file_basename, string_encoding_method, 'Decoding',
        '.' + string_file_extension, int_decoded_file_size, int_cost_decoding,
        int_time_decoding, int_original_size]

    return list_encoded, list_decoded, np_decoded_dna_sequences


@st.cache_data
def df_generate_summary(df_report):
    """
    df_generate_summary function generates a summary report of multiple
    benchmark runs

    This function aggregates mulitple benchmarks of all encoding methods and
    all original files. The resulting file does not contain per run information
    but an aggregated information of all runs per encoding method and original
    file

    Args:
        df_report (pd.DataFrame): DataFrame containing the detailed benchmark
        information of multiple runs

    Returns:
        pd.DataFrame: DataFrame containing the summary information
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
        columns={'Time': 'Sum_Mean_Time_s', 'Cost': 'Sum_Cost_$'},
        inplace=True)
    df_summary = df_summary.merge(
        df_encoding_multipliers,
        on=['Filename', 'Method', 'Type'], how='inner')

    return df_summary


@st.cache_data
def np_data_to_binary_array(path_original_file, string_file_name):
    """
    np_data_to_binary_array function is used to convert the original file to
    its binary representation contained in a numpy array

    Args:
        path_original_file (os.path): path of the original file
        string_file_name (string): name of the file without extension

    Returns:
        binary_numpy_content (np.array): boolean array representing the
        original file
        int_translated_file_size (int): size of the resulting numpy array on
        the disk
    """
    np_binary_numpy_content = None
    int_translated_file_size = 0

    if os.path.isfile(path_original_file):
        with open(path_original_file, 'rb') as fd_file:
            np_binary_array_content = ba.bitarray()
            np_binary_array_content.fromfile(fd_file)
            np_binary_numpy_content = np.frombuffer(
                np_binary_array_content.unpack(), dtype=bool)

            path_translated_file = os.path.join(_PATH_ORIGINAL_TRANSLATED,
                                                string_file_name + '.npy')
            np.save(path_translated_file, np_binary_numpy_content)
            int_translated_file_size = os.path.getsize(path_translated_file)
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_original_file)

    return np_binary_numpy_content, int_translated_file_size
