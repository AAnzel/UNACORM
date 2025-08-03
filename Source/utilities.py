import errno
import io
import multiprocessing
import os
import shutil
import sys
import time

import bitarray as ba

# Importing error simulation scripts
import mesa_call
import numpy as np
import simulate_errors
import streamlit as st

# Importing Encodings
import xor_code_python as encoding_xor
from Encodings.DNA_Aeon import unified as encoding_dnaaeon
from Encodings.RaptorCode import unified_dna_lt as encoding_lt
from Encodings.RaptorCode import unified_dna_online as encoding_online
from Encodings.RaptorCode import unified_dna_raptor as encoding_raptor
from Encodings.RepetitionCode.src import transform as encoding_repetition
from Encodings.SimpleCode.src import transform as encoding_simple
from Encodings.The2DCode import encoder as encoding_2d_tmp

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


# Defining paths for important files and directories
PATH_ROOT_DATA = os.path.join("..", "Data")
PATH_ORIGINAL_DATA = os.path.join(
    PATH_ROOT_DATA, "Original", "Test"
)  # TODO: Remove 'Test' # noqa
PATH_CACHE_DATA = os.path.join(PATH_ROOT_DATA, "cache_data")
PATH_EXISTING_DETAIL = os.path.join(PATH_CACHE_DATA, "pre_detail.pkl")
PATH_EXISTING_SUMMARY = os.path.join(PATH_CACHE_DATA, "pre_summary.pkl")
PATH_INTERMEDIARY_DETAIL = os.path.join(PATH_CACHE_DATA, "int_detail.pkl")
PATH_INTERMEDIARY_SUMMARY = os.path.join(PATH_CACHE_DATA, "int_summary.pkl")
_PATH_ORIGINAL_TRANSLATED = os.path.join(
    PATH_ROOT_DATA, "Translated_Binary"
)  # This is where we keep boolean
# representations of the original data
_PATH_ENCODED_DATA = os.path.join(PATH_ROOT_DATA, "Encoded")
_PATH_DECODED_DATA = os.path.join(PATH_ROOT_DATA, "Decoded")
_PATH_UPLOADED_DATA = os.path.join(PATH_ROOT_DATA, "Uploaded")
_PATH_ENCODING_METHODS = os.path.join("Encodings")


_FLOAT_ILLUMINA_COST_PER_BASE = 0.000015
_FLOAT_NANOPORE_COST_PER_BASE = 0.000025
_FLOAT_PACBIO_COST_PER_BASE = 0.000035
_INT_SEQUENCING_COVERAGE = 100
_FLOAT_SYNTHESIS_COST_PER_BASE = 0.1
LIST_FLOAT_ERROR_MULTIPLIERS = [0.0, 0.05, 0.1, 0.5, 1.0, 1.5, 2.0, 2.5]

_UPLOADED_SAVE_TIME = 3600  # 3600 seconds = 1h
encoding_2d = encoding_2d_tmp.api()  # Required because of the implementation

_LIST_PASS_METHODS = []
LIST_ENCODING_METHODS = []
for string_encoding_method in os.listdir(_PATH_ENCODING_METHODS):
    if string_encoding_method not in _LIST_PASS_METHODS and os.path.isdir(
        os.path.join(_PATH_ENCODING_METHODS, string_encoding_method)
    ):
        LIST_ENCODING_METHODS.append(string_encoding_method)


def remove_cached_data():
    """
    remove_cached_data function removes all data that was previously created
    while running the dashboard

    Returns:
        None
    """

    time_limit = time.time() - _UPLOADED_SAVE_TIME
    list_directories_to_clean = [
        _PATH_UPLOADED_DATA,
        _PATH_ENCODED_DATA,
        _PATH_DECODED_DATA,
        _PATH_ORIGINAL_TRANSLATED,
    ]

    # Traversing directories and deleting everything from them
    for path_dir in list_directories_to_clean:
        for string_file in os.listdir(path_dir):
            path_file = os.path.join(path_dir, string_file)

            if "gitkeep" in string_file or os.path.isdir(path_file):
                continue
            else:
                # Check if file is older than 1h, and if yes, delete it
                if os.stat(path_file).st_mtime < time_limit:
                    try:
                        if os.path.isfile(path_file) or os.path.islink(
                            path_file
                        ):
                            os.unlink(path_file)
                        elif os.path.isdir(path_file):
                            shutil.rmtree(path_file)
                    except OSError as e:
                        print(
                            "Failed to delete "
                            + path_file
                            + ". Reason: "
                            + str(e)
                        )
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
    # Twist Bioscience price model
    # Bulk Discount: 10% discount for orders exceeding 100,000 bases

    float_cost_per_base = _FLOAT_SYNTHESIS_COST_PER_BASE
    int_total_base_pairs = sum([
        len(string_dna_sequence.strip())
        for string_dna_sequence in list_dna_sequences
    ])
    float_cost_total = int_total_base_pairs * float_cost_per_base

    if int_total_base_pairs > 100000:
        float_cost_total *= 0.9

    return float_cost_total


@st.cache_data
def float_calculate_decoding_cost(
    list_dna_sequences,
    string_technology="PacBio",
    int_sequencing_coverage=_INT_SEQUENCING_COVERAGE,
):
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
    if string_technology == "Illumina":
        float_cost_per_base = _FLOAT_ILLUMINA_COST_PER_BASE
    elif string_technology == "Nanopore":
        float_cost_per_base = _FLOAT_NANOPORE_COST_PER_BASE
    elif string_technology == "PacBio":
        float_cost_per_base = _FLOAT_PACBIO_COST_PER_BASE
    else:
        raise RuntimeError("ERROR: Bad technology string for sequencing!")

    int_total_base_pairs = (
        sum([
            len(string_dna_sequence.strip())
            for string_dna_sequence in list_dna_sequences
        ])
        * int_sequencing_coverage
    )
    float_cost_total = int_total_base_pairs * float_cost_per_base

    return float_cost_total


def np_list_encode_decode(
    str_encoding_method, list_np_data, path_file, bool_encode
):
    """
    np_list_encode_decode function encodes or decodes the data using all
    encoding methods

    Args:
        str_encoding_method (str): chosen encoding method
        list_np_data (list or np.array): list of string DNA sequence if
        encoding or numpy array of binary data when decoding
        path_file (os.path): path of the original un-encoded file
        bool_encode (bool): if True, encoding is performed, if False then
        decoding

    Returns:
        np_list_generated_seq (list): list of encoded DNA sequences if
        encoding, or numpy boolean array if decoding
    """
    np_list_generated_seq = [] if bool_encode else np.array([])

    if bool_encode:
        if str_encoding_method == "The2DCode":
            np_list_generated_seq = encoding_2d.encode("", list_np_data)
        elif str_encoding_method == "XORBasedCode":
            np_list_generated_seq = encoding_xor.encode("", list_np_data)
        elif str_encoding_method == "SimpleCode":
            np_list_generated_seq = encoding_simple.encode("", list_np_data)
        elif str_encoding_method == "RepetitionCode":
            np_list_generated_seq = encoding_repetition.encode("", list_np_data)
        elif str_encoding_method == "OnlineCode":  # TODO: Tweak hyperparameter
            np_list_generated_seq = encoding_online.encode(
                path_file, list_np_data
            )[0]
        elif str_encoding_method == "LTCode":  # TODO: Tweak hyperparameters
            np_list_generated_seq = encoding_lt.encode(path_file, list_np_data)[
                0
            ]
        elif str_encoding_method == "RaptorCode":
            np_list_generated_seq = encoding_raptor.encode(
                path_file, list_np_data
            )[0]
        elif str_encoding_method == "DNA_Aeon":
            np_list_generated_seq = encoding_dnaaeon.encode(path_file, "")
        else:
            print(
                "Encoding method " + str_encoding_method + " is not implemented"
            )
            pass
    else:
        if str_encoding_method == "The2DCode":
            np_list_generated_seq = encoding_2d.decode("", list_np_data)
        elif str_encoding_method == "XORBasedCode":
            np_list_generated_seq = encoding_xor.decode("", list_np_data)
        elif str_encoding_method == "SimpleCode":
            np_list_generated_seq = encoding_simple.decode("", list_np_data)
        elif str_encoding_method == "RepetitionCode":
            np_list_generated_seq = encoding_repetition.decode("", list_np_data)
        elif str_encoding_method == "OnlineCode":  # TODO: Tweak hyperparameter
            np_list_generated_seq = encoding_online.decode(
                path_file, list_np_data
            )
        elif str_encoding_method == "LTCode":  # TODO: Tweak hyperparameters
            np_list_generated_seq = encoding_lt.decode(path_file, list_np_data)
        elif str_encoding_method == "RaptorCode":
            np_list_generated_seq = encoding_raptor.decode(
                path_file, list_np_data
            )
        elif str_encoding_method == "DNA_Aeon":
            np_list_generated_seq = encoding_dnaaeon.decode("", list_np_data)
        else:
            print(
                "Encoding method " + str_encoding_method + " is not implemented"
            )
            pass

    return np_list_generated_seq


def tuple_pipeline(
    string_encoding_method,
    np_bit_array,
    path_input_file,
    string_file_name,
    int_original_size,
    bool_simulate_error,
    bool_use_mesa,
    int_storage_length,
    float_error_multiplier,
):
    """
    tuple_pipeline function is used for integrating the encoding/decoding
    process for one file

    Args:
        string_encoding_method (str): chosen encoding method
        np_bit_array (array): numpy boolean array of uploaded file
        path_input_file (str): path of uploaded data
        string_file_name (str): the base name of the file with extension
        int_original_size (int): size of original file
        bool_simulate_error (bool): if True, MESA call is invoked and error
        simulation initiated. If False, DNA sequences are not modified
        bool_use_mesa (bool): if True and bool_simulate_error is True, MESA
        call is invoked, else error simulation is conducted using
        simulate_errrors.py script
        int_storage_length (int): number of years for simulating DNA
        degradation. Used only if bool_simulate_error and bool_use_mesa are
        True
        float_error_multiplier (float): number that increases or decreases the
        probability of errors. Used only if bool_simulate_error is True and
        bool_use_mesa is False

    Returns:
        list_encoded (list): list of result from encoding process including
        time, cost, and size
        list_decoded (list): list of result from decoding process including
        time, cost, and size
        np_decoded_dna_sequences (np.array): numpy boolean array containing
        decoded sequences
        dict_error_results (dict): dictionary containing error information
        if bool_simulate_error is True, else it is empty
    """
    string_input_file_basename = os.path.splitext(string_file_name)[0]
    string_file_extension = os.path.splitext(string_file_name)[1][1:]

    # If the runtime error happens (encoding method fails) we have to create
    # dummy data and initialize everything
    list_dna_sequences = []
    list_modified_sequences = []
    list_encoded = [
        string_input_file_basename,
        string_encoding_method,
        "Encoding",
        string_file_extension,
        None,
        None,
        None,
        None,
    ]
    list_decoded = list_encoded
    list_decoded[2] = "Decoding"
    np_decoded_dna_sequences = np.array([])
    dict_error_results = {
        "Number_of_substitutions": 0,
        "Number_of_deletions": 0,
        "Number_of_insertions": 0,
        "Total_number_of_errors": 0,
        "Base_error_ratio": 0,
    }

    # We time the encoding process
    int_start_time = time.time()

    mp_queue = multiprocessing.Queue()

    mp_encoding_process = multiprocessing.Process(
        target=run_capturing_process,
        args=(
            mp_queue,
            np_list_encode_decode,
            (string_encoding_method, np_bit_array, path_input_file, True),
        ),
        name="Encoding_" + string_encoding_method,
    )

    mp_encoding_process.start()
    list_dna_sequences = print_output(mp_queue)
    mp_encoding_process.join()  # Wait for the process to finish

    if mp_encoding_process.exitcode != 0 or list_dna_sequences in [None, []]:
        print(
            "Subprocess encoding failed with exit code: ",
            mp_encoding_process.exitcode,
        )
        return (
            list_encoded,
            list_decoded,
            list_dna_sequences,
            dict_error_results,
        )

    int_time_encoding = time.time() - int_start_time

    list_dna_sequences = [
        string_dna.upper() for string_dna in list_dna_sequences
    ]

    int_cost_encoding = float_calculate_encoding_cost(list_dna_sequences)
    int_encoded_size = sum(
        len(string_dna_sequence) for string_dna_sequence in list_dna_sequences
    )

    list_encoded = [
        string_input_file_basename,
        string_encoding_method,
        "Encoding",
        "." + string_file_extension,
        int_encoded_size,
        int_cost_encoding,
        int_time_encoding,
        int_original_size,
    ]

    if not bool_simulate_error:
        list_modified_sequences = list_dna_sequences
    else:
        if bool_use_mesa:
            string_progress_text = ""
            st_progress_bar = st.progress(0, text=string_progress_text)
            int_num_of_sequences = len(list_dna_sequences)
            for int_i in range(int_num_of_sequences):
                st_progress_bar.progress(
                    (int_i + 1) / int_num_of_sequences,
                    text=(
                        "Sequence "
                        + str(int_i + 1)
                        + " of "
                        + str(int_num_of_sequences)
                    ),
                )

                list_modified_sequences.append(
                    mesa_call.string_api_call(
                        [list_dna_sequences[int_i]], int_storage_length
                    )
                )
            st_progress_bar.empty()

        else:
            (list_modified_sequences, dict_error_results) = (
                simulate_errors.tuple_simulate_errors(
                    list_dna_sequences, float_error_multiplier
                )
            )

    # We time the decoding process
    int_start_time = time.time()

    mp_queue = multiprocessing.Queue()

    mp_decoding_process = multiprocessing.Process(
        target=run_capturing_process,
        args=(
            mp_queue,
            np_list_encode_decode,
            (
                string_encoding_method,
                list_modified_sequences,
                path_input_file,
                False,
            ),
        ),
        name="Decoding_" + string_encoding_method,
    )

    mp_decoding_process.start()
    np_decoded_dna_sequences = print_output(mp_queue)
    mp_decoding_process.join()  # Wait for the process to finish

    if (
        mp_decoding_process.exitcode != 0
        or np_decoded_dna_sequences is None
        or len(np_decoded_dna_sequences) == 0
    ):
        print(
            "Subprocess decoding failed with exit code: ",
            mp_decoding_process.exitcode,
        )
        return (
            list_encoded,
            list_decoded,
            np_decoded_dna_sequences,
            dict_error_results,
        )

    int_time_decoding = time.time() - int_start_time

    int_cost_decoding = float_calculate_decoding_cost(list_dna_sequences)
    int_decoded_size = len(np_decoded_dna_sequences)

    list_decoded = [
        string_input_file_basename,
        string_encoding_method,
        "Decoding",
        "." + string_file_extension,
        int_decoded_size,
        int_cost_decoding,
        int_time_decoding,
        int_original_size,
    ]

    return (
        list_encoded,
        list_decoded,
        np_decoded_dna_sequences,
        dict_error_results,
    )


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
    df_information_densities = df_report[
        ["Filename", "Method", "Transformation", "Type", "Size", "OriFile_Size"]
    ].copy(deep=True)
    df_information_densities["Information_Density"] = (
        df_information_densities["OriFile_Size"]
        / df_information_densities["Size"]
    )
    df_information_densities = df_information_densities.loc[
        df_summary["Transformation"] == "Encoding"
    ]
    df_information_densities.drop(
        ["Transformation", "Size", "OriFile_Size"], axis=1, inplace=True
    )
    df_information_densities = (
        df_information_densities.groupby(["Filename", "Method", "Type"])
        .agg({"Information_Density": "first"})
        .reset_index()
    )

    df_summary.drop(["Size", "OriFile_Size"], axis=1, inplace=True)

    df_summary = (
        df_summary.groupby([
            "Filename",
            "Method",
            "Transformation",
            "Type",
            "Similarity",
            "Error_Multiplier",
        ])
        .agg({
            "Time": "mean",
            "Cost": "mean",
            "Number_of_substitutions": "first",
            "Number_of_deletions": "first",
            "Number_of_insertions": "first",
            "Total_number_of_errors": "first",
            "Base_error_ratio": "first",
        })
        .reset_index()
    )
    df_summary = (
        df_summary.groupby([
            "Filename",
            "Method",
            "Type",
            "Similarity",
            "Error_Multiplier",
        ])
        .agg({
            "Time": "sum",
            "Cost": "sum",
            "Number_of_substitutions": "first",
            "Number_of_deletions": "first",
            "Number_of_insertions": "first",
            "Total_number_of_errors": "first",
            "Base_error_ratio": "first",
        })
        .reset_index()
    )
    df_summary.rename(
        columns={
            "Time": "Sum_Mean_Time_s",
            "Cost": "Sum_Cost_$",
            "Number_of_substitutions": "Mean_Num_of_Subs",
            "Number_of_deletions": "Mean_Num_of_Dels",
            "Number_of_insertions": "Mean_Num_of_Ins",
            "Total_number_of_errors": "Mean_Num_of_Errors",
            "Base_error_ratio": "Mean_Base_Error_Ratio",
        },
        inplace=True,
    )

    df_summary = df_summary.merge(
        df_information_densities, on=["Filename", "Method", "Type"], how="inner"
    )

    return df_summary


@st.cache_data
def np_data_to_binary_array(path_original_file):
    """
    np_data_to_binary_array function is used to convert the original file to
    its binary representation contained in a numpy array

    Args:
        path_original_file (os.path): path of the original file

    Returns:
        binary_numpy_content (np.array): boolean array representing the
        original file
        int_translated_file_size (int): length of the resulting numpy array
        (number of bits)
    """
    np_binary_numpy_content = None
    int_translated_file_size = 0

    if os.path.isfile(path_original_file):
        with open(path_original_file, "rb") as fd_file:
            np_binary_array_content = ba.bitarray()
            np_binary_array_content.fromfile(fd_file)
            np_binary_numpy_content = np.frombuffer(
                np_binary_array_content.unpack(), dtype=bool
            )

            int_translated_file_size = np_binary_numpy_content.shape[0]
    else:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), path_original_file
        )

    return np_binary_numpy_content, int_translated_file_size


def run_capturing_process(mp_queue, function_target, tuple_args):
    """
    run_capturing_process is a wrapper functions that runs the
    np_list_encode_decode (given here as function_target argument) in new
    process

    Args:
        mp_queue (multiprocessing.Queue()): multiprocessing queue holding
        function_target stdout, stderr, and return value
        function_target (function): passed function that is run in a new
        process. It is always np_list_encode_decode
        tuple_args (tuple): tuple of arguments passed to the function_target as
        input
    """
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    # Redirect stdout and stderr to capture output
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

    try:
        # Call the encode/decode function and capture its return value
        np_list_generated_seq = function_target(*tuple_args)

        # Capture output and error messages
        output = sys.stdout.getvalue()
        error_output = sys.stderr.getvalue()

        # Send captured stdout and stderr to the queue
        if output:
            mp_queue.put(("stdout", output))
        if error_output:
            mp_queue.put(("stderr", error_output))

        # Send the result (which can be any Python object) to the queue
        mp_queue.put(("result", np_list_generated_seq))  # Send result back

    except Exception as e:
        print(f"Error during processing: {e}", file=sys.stderr)
    finally:
        # Signal completion with a sentinel value
        mp_queue.put(("done", None))  # Send a done signal to indicate finish
        sys.stdout = original_stdout
        sys.stderr = original_stderr


def print_output(mp_queue):
    """
    print_output function prints stderr and stdout of a function that is
    running in a new process. It also returns the function return values

    Args:
        mp_queue (multiprocessing.Queue()): multiprocessing queue holding
        function_target stdout, stderr, and return value

    Returns:
        list or np.array: returns a list of np.array, as defined in
        np_list_encode_decode function
    """
    while True:
        try:
            recv_type, recv_value = mp_queue.get()
            if recv_type == "stdout":
                print(recv_value, end="")
            elif recv_type == "stderr":
                print(recv_value, end="", file=sys.stderr)
            elif recv_type == "result":
                return recv_value  # Return the result for further use
            elif recv_type == "done":
                break  # Exit loop when done signal is received
        except EOFError:
            break
