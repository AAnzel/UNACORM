import os
import time

import numpy as np
import pandas as pd
import streamlit as st
import text_content as tc
import utilities as uti
import visualize as vis

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"

st.header(":primary[︱]File Upload")
st.markdown("")
list_file_type = ["txt", "jpg", "wav"]

imported_file = st.file_uploader(
    label="Upload a file",
    type=list_file_type,
    accept_multiple_files=False,
    key="Upload_file_",
)

string_input_file = ""
path_input_file = ""

if imported_file is not None:
    float_time_uploaded = str(time.time()).replace(".", "_")
    string_input_file = imported_file.name
    string_new_name = float_time_uploaded + "_" + imported_file.name
    path_input_file = os.path.join(uti._PATH_UPLOADED_DATA, string_new_name)
    with open(path_input_file, mode="wb") as w:
        w.write(imported_file.getvalue())

    if os.path.exists(path_input_file):
        st.success("The file is successfully uploaded")

st_col_1, st_col_2 = st.columns([1.5, 1], gap="medium")

with st_col_1:
    st.write("Uploaded data path:\t", path_input_file)
with st_col_2:
    st.info(
        "Your data is automatically deleted after changing the tab"
        + " or closing the window."
    )

if path_input_file != "":
    np_binary_encoding, original_file_size = uti.np_data_to_binary_array(
        path_input_file
    )
else:
    np_binary_encoding = None
    original_file_size = None

st.markdown("---")

st.header(":primary[︱]DNA Encoding")
list_chosen_dna_encoding = st.multiselect(
    "Select preferred DNA Encoding Methods",
    uti.LIST_ENCODING_METHODS,
    placeholder="Choose DNA encoding methods",
)

st.warning("The length of processing time depends on chosen methods")

st_cont_0 = st.container(border=True)

with st_cont_0:
    st.markdown("#### Error Simulation")

    st_col_1, _, st_col_2 = st.columns([4, 1, 4])

    with st_col_1:
        int_chosen_storage_length = st.number_input(
            "Choose length of storage (in months) or leave it empty to skip"
            + " (uses [MESA](https://mesa.mosla.de/) API)",
            value=None,
            min_value=1,
            step=1,
            disabled=True,
        )

    with st_col_2:
        float_error_multiplier = st.number_input(
            "Choose error multiplier value or leave it 0 to skip",
            value=0.0,
            min_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[0],
            max_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[-1],
            step=0.5,
            help=tc.STRING_MUTAGENESIS_HELP,
        )

if int_chosen_storage_length is None and float_error_multiplier == 0.0:
    bool_simulate_errors = False
else:
    bool_simulate_errors = True

df_new_detail = None
df_new_summary = None

list_results = []
list_cannot_encode_decode = []
if list_chosen_dna_encoding != [] and np_binary_encoding is not None:
    for string_encoding_method in list_chosen_dna_encoding:
        # ! Runtime errors can occur if we simulate DNA degradation using
        # ! MESA. These errors occur with some DNA Encoding methods, such
        # ! as The2DCode that breaks if the error creates a homopolymer of
        # ! length 3. This is why we have to catch errors
        list_encoded_info = []

        (
            list_encoded_info,
            list_decoded_info,
            np_decoded_array,
            dict_error_results,
        ) = uti.tuple_pipeline(
            string_encoding_method,
            np_binary_encoding,
            path_input_file,
            string_input_file,
            original_file_size,
            bool_simulate_errors,
            False,  # TODO: Add logic for this (bool_use_mesa)
            int_chosen_storage_length,
            float_error_multiplier,
        )

        # If error occured, we note it
        if len(np_decoded_array) == 0:
            list_cannot_encode_decode.append(string_encoding_method)

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

    if list_cannot_encode_decode:
        st.error(
            "Cannot encode/decode using the following methods:\t"
            + str(list_cannot_encode_decode)
        )

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

    df_new_summary = uti.df_generate_summary(df_new_detail)

    if df_new_detail is not None and df_new_summary is not None:
        st.header(":primary[︱]Benchmark")
        uti.display_processed_data(df_new_summary, df_new_detail, True)

    (chart_size, chart_time, chart_cost) = vis.visualize_uploaded(df_new_detail)

    st.header(":primary[︱]Information Density", help=tc.STRING_DENSITY_HELP)
    chart = vis.visualize_density_benchmark(df_new_summary)
    st.plotly_chart(chart, use_container_width=True)
    st.header(":primary[︱]Size", help=tc.STRING_SIZE_HELP)
    st.plotly_chart(chart_size, use_container_width=True)
    st.header(":primary[︱]Time", help=tc.STRING_TIME_HELP)
    st.plotly_chart(chart_time, use_container_width=True)
    st.header(":primary[︱]Cost", help=tc.STRING_COST_HELP)
    st.plotly_chart(chart_cost, use_container_width=True)

elif list_chosen_dna_encoding != [] and np_binary_encoding is not None:
    st.error("Choose a file and length of storage first.")  # TODO: Change
else:
    pass

uti.display_footer()
