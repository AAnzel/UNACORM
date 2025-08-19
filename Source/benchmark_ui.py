import os

import numpy as np
import pandas as pd
import streamlit as st
from utilities import (
    LIST_ENCODING_METHODS,
    LIST_FLOAT_ERROR_MULTIPLIERS,
    PATH_EXISTING_DETAIL,
    PATH_EXISTING_SUMMARY,
    PATH_INTERMEDIARY_DETAIL,
    PATH_INTERMEDIARY_SUMMARY,
    PATH_ORIGINAL_DATA,
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


_NUMBER_OF_EXPERIMENT_RUNS = 5
_BOOL_NO_USER_INTERACTION = True


def save_intermediary(list_results):
    """
    save_intermediary saves intermediary detail and summary benchmark data

    Args:
        list_results (list): a list containing benchmark results calculated so
        far

    Returns:
        None
    """

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

    df_intermediary_summary = df_generate_summary(df_intermediary_detail)
    df_intermediary_detail.to_pickle(PATH_INTERMEDIARY_DETAIL)
    df_intermediary_summary.to_pickle(PATH_INTERMEDIARY_SUMMARY)

    return None


def run_precalculation(int_num_of_iteration):
    """
    run_precalculation function is used to run the precalculation dashboard
    num_of_iteration times in order to benchmark all encoding methods
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
    string_progress_text = ""
    st_progress_bar = st.progress(0, text=string_progress_text)

    bool_summary_exists = os.path.exists(PATH_EXISTING_SUMMARY)
    bool_detail_exists = os.path.exists(PATH_EXISTING_DETAIL)

    if bool_summary_exists:
        df_existing_summary = pd.read_pickle(PATH_EXISTING_SUMMARY)
    else:
        df_existing_summary = pd.DataFrame(
            columns=pd.Series([
                "Filename",
                "Method",
                "Type",
                "Sum_Mean_Time_s",
                "Sum_Cost_$",
                "Information_Density",
                "Similarity",
                "Error_Multiplier",
                "Mean_Num_of_Subs",
                "Mean_Num_of_Dels",
                "Mean_Num_of_Ins",
                "Mean_Num_of_Errors",
                "Mean_Base_Error_Ratio",
            ])
        )
    if bool_detail_exists:
        df_existing_detail = pd.read_pickle(PATH_EXISTING_DETAIL)
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

    st.header("Existing precalculated details")
    st.dataframe(df_existing_detail)
    st.header("Existing precalculated summary")
    st.dataframe(df_existing_summary)

    list_results = []
    list_original_files = os.listdir(PATH_ORIGINAL_DATA)

    int_total_missing = 0
    for float_error_multiplier in LIST_FLOAT_ERROR_MULTIPLIERS:
        for string_file in list_original_files:
            string_file_name, _ = os.path.splitext(string_file)
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

    # We go through error multipliers and list original files
    for float_error_multiplier in LIST_FLOAT_ERROR_MULTIPLIERS:
        for string_file in list_original_files:
            path_one_file = os.path.join(PATH_ORIGINAL_DATA, string_file)
            string_file_name, string_file_extension = os.path.splitext(
                string_file
            )

            if not os.path.isfile(path_one_file):
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
                    continue  # All runs for this combination are done

                (np_binary_encoding, int_file_size_bits) = (
                    np_data_to_binary_array(path_one_file)
                )

                for int_i in range(int_runs_to_do):
                    int_counter += 1
                    st_progress_bar.progress(
                        int_counter / int_total_runs if int_total_runs else 1.0,
                        text=(
                            f"[{int_counter}/{int_total_runs}] {string_file}_{string_encoding_method}_MULT:{float_error_multiplier}"
                        ),
                    )

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

                    # We save the intermediary result
                    save_intermediary(list_results)

    df_new_detail = pd.DataFrame(
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

    df_new_summary = df_generate_summary(df_new_detail)

    st_progress_bar.empty()
    st.header("Recently calculated details")
    st.dataframe(df_new_detail)
    st.header("Recently calculated summary")
    st.dataframe(df_new_summary)

    st.write("Do you want to merge new data into pickle file?")
    if st.button("Merge new data to pickle") or _BOOL_NO_USER_INTERACTION:
        df_detail_concat = pd.concat(
            [df_new_detail, df_existing_detail], ignore_index=True
        )
        df_detail_concat.to_pickle(PATH_EXISTING_DETAIL)
        df_summary_concat = pd.concat(
            [df_new_summary, df_existing_summary], ignore_index=True
        )
        df_summary_concat.to_pickle(PATH_EXISTING_SUMMARY)

        if os.path.exists(PATH_EXISTING_DETAIL) and os.path.exists(
            PATH_EXISTING_SUMMARY
        ):
            st.success("New data has been successfully merged")
            st.header("New Detail Data")
            st.dataframe(df_detail_concat)
            st.header("New Summary Data")
            st.dataframe(df_summary_concat)
        else:
            st.error("There was an error while uploading the pickle file")
    return None


def main():
    """
    main function wraps the precalculation dashboard

    Returns:
        None
    """
    run_precalculation(_NUMBER_OF_EXPERIMENT_RUNS)

    return None


if __name__ == "__main__":
    main()
