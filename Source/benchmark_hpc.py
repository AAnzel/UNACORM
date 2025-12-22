import glob
import os

import numpy as np
import pandas as pd
from utilities import (
    LIST_ENCODING_METHODS,
    LIST_FLOAT_ERROR_MULTIPLIERS,
    PATH_INTERMEDIARY_DETAIL,
    PATH_INTERMEDIARY_SUMMARY,
    PATH_ORIGINAL_DATA,
    PATH_PARTIAL_RESULTS,
    df_generate_summary,
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


PATH_PARTIAL_DETAIL_PATTERN = os.path.join(PATH_PARTIAL_RESULTS, "*.pkl")
_NUMBER_OF_EXPERIMENT_RUNS = 5


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
        os.path.join(PATH_PARTIAL_RESULTS, string_file_name + ".pkl")
    )

    return None


def run_precalculation(int_num_of_iteration):
    """
    run_precalculation function is used to run the precalculation dashboard
    num_of_iteration times in order to benchmark all coding schemes
    across all original files.

    The function only precalculates the original files that were not already
    processed. The user can add new files into the PATH_ORIGINAL_DATA directory
    and append the benchmark runs of these files to the existing benchmark
    precalculated data. The dashboard allows users to choose if they want to
    append the new data or not.

    Args:
        num_of_iteration (int): number of iteration for each file

    Returns:
        None
    """

    list_original_files = os.listdir(PATH_ORIGINAL_DATA)

    int_total_missing = 0
    for string_file in list_original_files:
        path_one_file = os.path.join(PATH_ORIGINAL_DATA, string_file)

        if not os.path.isfile(path_one_file):
            continue

        string_file_name, _ = os.path.splitext(string_file)

        path_existing_detail = os.path.join(
            PATH_PARTIAL_RESULTS, string_file_name + ".pkl"
        )
        bool_detail_exists = os.path.exists(path_existing_detail)
        if bool_detail_exists:
            df_existing_detail = pd.read_pickle(path_existing_detail)

            for float_error_multiplier in LIST_FLOAT_ERROR_MULTIPLIERS:
                for string_encoding_method in LIST_ENCODING_METHODS:
                    int_existing_runs = df_existing_detail[
                        (df_existing_detail["Filename"] == string_file_name)
                        & (
                            df_existing_detail["Method"]
                            == string_encoding_method
                        )
                        & (
                            df_existing_detail["Error_Multiplier"]
                            == float_error_multiplier
                        )
                    ].shape[0]
                    int_required = max(
                        0, int_num_of_iteration - int_existing_runs
                    )
                    int_total_missing += int_required
        else:
            int_total_missing += len(LIST_FLOAT_ERROR_MULTIPLIERS) * len(
                LIST_ENCODING_METHODS * int_num_of_iteration
            )

    int_total_runs = int_total_missing
    int_counter = 0

    for string_file in list_original_files:
        list_partial_results = []
        path_one_file = os.path.join(PATH_ORIGINAL_DATA, string_file)

        if not os.path.isfile(path_one_file):
            continue

        string_file_name, _ = os.path.splitext(string_file)

        path_existing_detail = os.path.join(
            PATH_PARTIAL_RESULTS, string_file_name + ".pkl"
        )
        bool_detail_exists = os.path.exists(path_existing_detail)
        if bool_detail_exists:
            df_existing_detail = pd.read_pickle(path_existing_detail)
            list_partial_results.append(df_existing_detail.values.tolist()[0])
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

                int_runs_to_do = int_num_of_iteration - int_existing_runs

                if int_runs_to_do <= 0:
                    continue  # All runs for this combination are done

                (np_binary_encoding, int_file_size_bits) = (
                    np_data_to_binary_array(path_one_file)
                )

                for int_i in range(int_runs_to_do):
                    int_counter += 1

                    print(
                        "\n["
                        + str(int_counter)
                        + "/"
                        + str(int_total_runs)
                        + "] "
                        + string_file
                        + "_"
                        + string_encoding_method
                        + "_MULT: "
                        + str(float_error_multiplier)
                        + "_RUN: "
                        + str(int_i)
                        + "\n"
                    )

                    # Error simulation without MESA
                    (
                        list_encoded_info,
                        list_decoded_info,
                        np_decoded_array,
                        dict_error_results,
                    ) = tuple_pipeline(
                        string_encoding_method,
                        np_binary_encoding,
                        path_one_file,
                        string_file,
                        int_file_size_bits,
                        True,
                        False,
                        None,
                        float_error_multiplier,
                    )

                    bool_similar_files = np.array_equal(
                        np_binary_encoding, np_decoded_array
                    )
                    list_partial_results.append(
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
                    list_partial_results.append(
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
                        save_intermediary(
                            list_partial_results, string_file_name
                        )

            # We save the intermediary result
            save_intermediary(list_partial_results, string_file_name)

        # We save the intermediary result
        save_intermediary(list_partial_results, string_file_name)

    return None


def merge_details_and_generate_summary():
    partial_detail_files = glob.glob(PATH_PARTIAL_DETAIL_PATTERN)

    if not partial_detail_files:
        print("No partial detail pickle files found to merge.", flush=True)
        return

    # Load and concatenate partial detail dataframes
    list_detail_dfs = [pd.read_pickle(f) for f in partial_detail_files]
    df_merged_detail = pd.concat(list_detail_dfs, ignore_index=True)

    # Save the merged detail dataframe
    df_merged_detail.to_pickle(PATH_INTERMEDIARY_DETAIL)
    print(
        f"Merged detail pickle saved to {PATH_INTERMEDIARY_DETAIL}", flush=True
    )

    # Generate a summary dataframe from the merged detail
    merged_summary = df_generate_summary(df_merged_detail)

    # Save the generated summary dataframe
    merged_summary.to_pickle(PATH_INTERMEDIARY_SUMMARY)
    print(
        f"Summary pickle generated and saved to {PATH_INTERMEDIARY_SUMMARY}",
        flush=True,
    )

    return None


def main():
    #run_precalculation(_NUMBER_OF_EXPERIMENT_RUNS)
    merge_details_and_generate_summary()

    return None


if __name__ == "__main__":
    main()
