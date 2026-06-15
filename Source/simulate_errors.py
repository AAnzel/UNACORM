import random
from copy import deepcopy

import numpy as np

__author__ = ["Aleksandar Anžel"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Marius Welzel", "Chisom Anyabolu"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


_FLOAT_DEFAULT_SUBSTITUTION_RATE = 0.0238
_FLOAT_DEFAULT_DELETION_RATE = 0.0082
_FLOAT_DEFAULT_INSERTION_RATE = 0.0039


def dict_initialize_probabilities(float_multiplier):
    """
    dict_initialize_probabilities initializes the probabilities of deletions,
    substitutions, and insertions according to the provided multiplier.

    Args:
        float_multiplier (float): Multiplier increases or decreases
        probability of each error happening by its value. If it is higher than
        1 then it increases the chances of errors happening. If it is less than
        1 but greater than 0, then it decreases the error probabilites. If it
        is 0, then no errors are simulated.

    Returns:
        dict: A dictionary containig the probability of each error happening.
    """
    dict_error_probabilities = None
    (float_substitution_rate, float_deletion_rate, float_insertion_rate) = (
        float_multiplier
        * np.array([
            _FLOAT_DEFAULT_SUBSTITUTION_RATE,
            _FLOAT_DEFAULT_DELETION_RATE,
            _FLOAT_DEFAULT_INSERTION_RATE,
        ])
    )

    dict_error_probabilities = {
        "Substitutions": float_substitution_rate,
        "Deletions": float_deletion_rate,
        "Insertions": float_insertion_rate,
    }

    return dict_error_probabilities


def string_simulate_substitution(
    string_original, list_positions, string_base=None
):
    """
    string_simulate_substitution introduces substitutions in the parsed DNA
    sequences on the parsed positions.

    Args:
        string_original (string): An unmodified DNA sequence.
        list_positions (list): A list containing positions where substitution
        should happen.

    Returns:
        string: The modified (degraded) DNA sequence.
    """
    string_modified = deepcopy(string_original)
    for int_position in list_positions:
        if not string_base:
            # We chose a base that is different than the existing one
            string_base = random.choice(
                list(
                    {"A", "T", "G", "C"}.difference(
                        string_original[int_position]
                    )
                )
            )
        string_modified = (
            string_modified[:int_position]
            + string_base
            + string_modified[int_position + 1 :]
        )
    return string_modified


def string_simulate_insertion(
    string_original, list_positions, string_base=None
):
    """
    string_simulate_insertion introduces insertions in the parsed DNA sequences
    on the parsed positions.

    Args:
        string_original (string): An unmodified DNA sequence.
        list_positions (list): A list containing positions where insertion
        should happen.

    Returns:
        string: The modified (degraded) DNA sequence.
    """
    string_modified = deepcopy(string_original)
    int_shift = 0
    list_positions.sort()
    for int_position in list_positions:
        if not string_base:
            # We chose any base
            string_base = random.choice(list({"A", "T", "G", "C"}))
        string_modified = (
            string_modified[: int_position + int_shift]
            + string_base
            + string_modified[int_position + int_shift :]
        )
        int_shift += 1
    return string_modified


def string_simulate_deletion(string_original, list_positions):
    """
    string_simulate_deletion introduces deletion in the parsed DNA sequences
    on the parsed positions.

    Args:
        string_original (string): An unmodified DNA sequence.
        list_positions (list): A list containing positions where deletion
        should happen.

    Returns:
        string: The modified (degraded) DNA sequence.
    """
    string_modified = deepcopy(string_original)
    int_shift = 0
    list_positions.sort()
    for int_position in list_positions:
        string_modified = (
            string_modified[: int_position - int_shift]
            + string_modified[int_position - int_shift + 1 :]
        )
        int_shift += 1
    return string_modified


def string_modify_sequence(
    string_original, list_positions_sub, list_positions_ins, list_positions_del
):
    """
    string_modify_sequence takes a DNA sequence and applies errors on specified
    positions within the sequences. It returns the degraded DNA sequence.

    Args:
        string_original (string): An unmodified DNA sequence.
        list_positions_sub (list): A list containing the positions where
        substitution should happen.
        list_positions_ins (list): A list containing the positions where
        insertion should happen.
        list_positions_del (list): A list containing the positions where
        deletion should happen.

    Returns:
        string: The modified (degraded) DNA sequence.
    """
    string_modified = deepcopy(string_original)
    if list_positions_sub:
        string_modified = string_simulate_substitution(
            string_modified, list_positions_sub
        )
    if list_positions_ins:
        string_modified = string_simulate_insertion(
            string_modified, list_positions_ins
        )
    if list_positions_del:
        string_modified = string_simulate_deletion(
            string_modified, list_positions_del
        )
    return string_modified


def list_modify_sequences(
    list_seqs, int_number_of_subs, int_number_of_dels, int_number_of_ins
):
    """
    list_modify_sequences takes a list of sequences, calculates random
    positions where errors will occur, and introduces errors on those
    positions. Some sequences might change, and some might not. It returns a
    list of modified sequences.

    Args:
        list_seqs (list): A list of DNA sequences.
        int_number_of_subs (int): A number of substitutions.
        int_number_of_dels (int): A number of deletions.
        int_number_of_ins (int): A number of insertions.

    Returns:
        list: A list of modified (degraded) DNA sequences.
    """

    int_total_number_of_nucleotides = sum([
        len(string_seq) for string_seq in list_seqs
    ])

    numpy_all_positions_subs = np.random.choice(
        int_total_number_of_nucleotides, int_number_of_subs, replace=False
    )
    numpy_all_positions_ins = np.random.choice(
        int_total_number_of_nucleotides, int_number_of_ins, replace=False
    )
    numpy_all_positions_dels = np.random.choice(
        int_total_number_of_nucleotides, int_number_of_dels, replace=False
    )

    list_modified_seqs = []
    int_current_low = 0
    int_current_high = 0
    for string_seq in list_seqs:
        int_one_seq_len = len(string_seq)
        int_current_high += int_one_seq_len

        list_positions_sub = [
            int_num - int_current_low - 1
            for int_num in numpy_all_positions_subs
            if (int_current_high >= int_num > int_current_low)
        ]
        list_positions_ins = [
            int_num - int_current_low - 1
            for int_num in numpy_all_positions_ins
            if (int_current_high >= int_num > int_current_low)
        ]
        list_positions_del = [
            int_num - int_current_low - 1
            for int_num in numpy_all_positions_dels
            if (int_current_high >= int_num > int_current_low)
        ]

        list_modified_seqs.append(
            string_modify_sequence(
                string_seq,
                list_positions_sub,
                list_positions_ins,
                list_positions_del,
            )
        )

        int_current_low = int_current_high

    return list_modified_seqs


def tuple_simulate_errors(list_encoded_sequences, float_multiplier=0):
    """
    tuple_simulate_errors takes a list of DNA sequences and an error multiplier
    and returns a list of degraded sequences with the base error ratio

    Args:
        list_encoded_sequences (list): This list contains string elements where
        each string is a DNA sequences
        float_multiplier (float, optional): Multiplier increases or decreases
        probability of each error happening by its value. If it is higher than
        1 then it increases the chances of errors happening. If it is less than
        1 but greater than 0, then it decreases the error probabilites. If it
        is 0, then no errors are simulated. Defaults to 0.

    Returns:
        tuple: The first element of a tuple is a list of degraded sequences,
        while the second element is the base error ratio.
    """

    dict_error_probabilities = dict_initialize_probabilities(float_multiplier)
    dict_results = {}
    dict_results["Total_number_of_nucleotides"] = sum(
        len(string_sequence.strip())
        for string_sequence in list_encoded_sequences
    )

    dict_results["Number_of_substitutions"] = int(
        dict_error_probabilities["Substitutions"]
        * dict_results["Total_number_of_nucleotides"]
    )
    dict_results["Number_of_deletions"] = int(
        dict_error_probabilities["Deletions"]
        * dict_results["Total_number_of_nucleotides"]
    )
    dict_results["Number_of_insertions"] = int(
        dict_error_probabilities["Insertions"]
        * dict_results["Total_number_of_nucleotides"]
    )

    dict_results["Total_number_of_errors"] = sum([
        dict_results["Number_of_substitutions"],
        dict_results["Number_of_deletions"],
        dict_results["Number_of_insertions"],
    ])

    dict_results["Base_error_ratio"] = (
        dict_results["Total_number_of_errors"]
        / dict_results["Total_number_of_nucleotides"]
    )

    list_modified_seqs = list_modify_sequences(
        list_encoded_sequences,
        dict_results["Number_of_substitutions"],
        dict_results["Number_of_deletions"],
        dict_results["Number_of_insertions"],
    )
    # print(dict_results)

    return list_modified_seqs, dict_results
