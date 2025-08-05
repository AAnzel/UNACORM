import argparse
import os

import numpy as np
import pandas as pd
from utilities import (
    LIST_ENCODING_METHODS,
    LIST_FLOAT_ERROR_MULTIPLIERS,
    PATH_ORIGINAL_DATA,
    PATH_PARTIAL_RESULTS,
    np_data_to_binary_array,
    tuple_pipeline,
)

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


def save_intermediary(list_results, string_file_name):
    df_intermediary_detail = pd.DataFrame(
        list_results,
        columns=pd.Series([
            "Filename",
            "Method",
            "Transformation",
            "Type",
            "Size",
            "Cost",
            "Time",
            "OriFile_Size",
            "Similarity",
            "Error_Multiplier",
            "Number_of_substitutions",
            "Number_of_deletions",
            "Number_of_insertions",
            "Total_number_of_errors",
            "Base_error_ratio",
        ]),
    )
    df_intermediary_detail.to_pickle(
        os.path.join(PATH_PARTIAL_RESULTS, "_", string_file_name, ".pkl")
    )

    return None


def run_precalculation(int_num_of_iteration, string_file_to_process):
    path_one_file = os.path.join(PATH_ORIGINAL_DATA, string_file_to_process)
    string_file_name, string_file_extension = os.path.splitext(
        string_file_to_process
    )

    path_existing_detail = os.path.join(
        PATH_PARTIAL_RESULTS, "_", string_file_name, ".pkl"
    )

    bool_detail_exists = os.path.exists(path_existing_detail)

    if bool_detail_exists:
        df_existing_detail = pd.read_pickle(path_existing_detail)
    else:
        df_existing_detail = pd.DataFrame(
            columns=pd.Series([
                "Filename",
                "Method",
                "Transformation",
                "Type",
                "Size",
                "Cost",
                "Time",
                "OriFile_Size",
                "Similarity",
                "Error_Multiplier",
                "Number_of_substitutions",
                "Number_of_deletions",
                "Number_of_insertions",
                "Total_number_of_errors",
                "Base_error_ratio",
            ])
        )

    list_results = []

    int_total_missing = 0
    for float_error_multiplier in LIST_FLOAT_ERROR_MULTIPLIERS:
        for string_encoding_method in LIST_ENCODING_METHODS:
            int_existing_runs = df_existing_detail[
                (df_existing_detail["Filename"] == string_file_name)
                & (df_existing_detail["Method"] == string_encoding_method)
                & (
                    df_existing_detail["Error_Multiplier"]
                    == float_error_multiplier
                )
            ].shape[0]
            int_required = max(0, int_num_of_iteration - int_existing_runs)
            int_total_missing += int_required

    int_total_runs = int_total_missing
    int_counter = 0

    for float_error_multiplier in LIST_FLOAT_ERROR_MULTIPLIERS:
        if not os.path.isfile(path_one_file):
            print(
                f"WARNING: File {string_file_to_process} does not exist, skipping"
            )
            continue

        for string_encoding_method in LIST_ENCODING_METHODS:
            int_existing_runs = df_existing_detail[
                (df_existing_detail["Filename"] == string_file_name)
                & (df_existing_detail["Method"] == string_encoding_method)
                & (
                    df_existing_detail["Error_Multiplier"]
                    == float_error_multiplier
                )
            ].shape[0]

            int_runs_to_do = int_num_of_iteration - int_existing_runs
            if int_runs_to_do <= 0:
                continue  # All runs done for this combo

            np_binary_encoding, int_file_size_bits = np_data_to_binary_array(
                path_one_file
            )

            for int_i in range(int_runs_to_do):
                int_counter += 1
                print(
                    f"[{int_counter}/{int_total_runs}] "
                    f"{string_file_name}_{string_encoding_method}_MULT:{float_error_multiplier}_RUN:{int_i}"
                )

                (
                    list_encoded_info,
                    list_decoded_info,
                    np_decoded_array,
                    dict_error_results,
                ) = tuple_pipeline(
                    string_encoding_method,
                    np_binary_encoding,
                    path_one_file,
                    string_file_to_process,
                    int_file_size_bits,
                    True,
                    False,
                    None,
                    float_error_multiplier,
                )

                bool_similar_files = np.array_equal(
                    np_binary_encoding, np_decoded_array
                )

                list_results.append(
                    list_encoded_info
                    + [
                        bool_similar_files,
                        float_error_multiplier,
                        dict_error_results["Number_of_substitutions"],
                        dict_error_results["Number_of_deletions"],
                        dict_error_results["Number_of_insertions"],
                        dict_error_results["Total_number_of_errors"],
                        dict_error_results["Base_error_ratio"],
                    ]
                )
                list_results.append(
                    list_decoded_info
                    + [
                        bool_similar_files,
                        float_error_multiplier,
                        dict_error_results["Number_of_substitutions"],
                        dict_error_results["Number_of_deletions"],
                        dict_error_results["Number_of_insertions"],
                        dict_error_results["Total_number_of_errors"],
                        dict_error_results["Base_error_ratio"],
                    ]
                )

                if int_counter % 2 == 0:
                    # Save intermediary results frequently to minimize data loss
                    save_intermediary(list_results, string_file_name)

    # Final save after all runs
    save_intermediary(list_results, string_file_name)


def main():
    parser = argparse.ArgumentParser(
        description="HPC mode DNA encoding benchmark"
    )

    parser.add_argument(
        "--num_of_runs",
        help="Number of runs: run the benchmark this many times",
        required=True,
    )
    parser.add_argument(
        "--file",
        help="Filter: run only on this file (basename without extension)",
        required=True,
    )
    args = parser.parse_args()

    run_precalculation(
        int_num_of_iteration=args.num_of_runs,
        string_file_to_process=args.file,
    )


if __name__ == "__main__":
    main()
