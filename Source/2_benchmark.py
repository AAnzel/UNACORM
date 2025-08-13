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

_, st_col_2, _ = st.columns([1, 9, 1])
with st_col_2:
    st.info(tc.STRING_INTRODUCTION)

df_existing_summary = pd.read_pickle(uti.PATH_EXISTING_SUMMARY)
df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)

st.header(":primary[︱]Benchmark", help=tc.STRING_MAIN_BENCHMARK_HELP)
uti.display_processed_data(df_existing_summary, df_existing_detail)
st.markdown("---")

st.header(":primary[︱]Information Density", help=tc.STRING_DENSITY_HELP)
chart_density = vis.visualize_density_benchmark(df_existing_summary)
st.plotly_chart(chart_density, use_container_width=True)

st.header(":primary[︱]Success Rate", help=None)  # TODO: Add new help
chart_failure_rate = vis.visualize_failure_rate_general(df_existing_summary)
st.plotly_chart(chart_failure_rate, use_container_width=True)

st.header(":primary[︱]Base Error", help=None)  # TODO: Add new help
chart_base_error = vis.visualize_base_error_general(df_existing_summary)
st.plotly_chart(chart_base_error, use_container_width=True)

st.header(
    ":primary[︱]Cost and Runtime per Error Multiplier", help=None
)  # TODO: Add new help
st.html("<br>")

with st.container(border=True):
    st_col_1, _, st_col_2 = st.columns([4, 1, 8])

    with st_col_1:
        float_error_multiplier = st.slider(
            "Choose error multiplier value or leave it 0 to skip",
            value=0.0,
            min_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[0],
            max_value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[-1],
            step=0.5,
            format="%1f",
        )
        with st.popover(
            "What is error multiplier?",
            icon=":material/help:",
            use_container_width=True,
        ):
            st.markdown(tc.STRING_MUTAGENESIS_HELP)

    list_files_to_visualize = list(pd.unique(df_existing_summary["Filename"]))

    with st_col_2:
        list_files_chosen = st.multiselect(
            "Select the files to review (This will affect Cost"
            + " and Time Charts)",
            default=list_files_to_visualize,
            options=list_files_to_visualize,
            placeholder="Choose files",
        )

    st.html("<br>")
    string_selected_visualization = st.radio(
        "Visualize using", ["Whisker Chart", "Bar Chart"], horizontal=True
    )

    if string_selected_visualization == "Whisker Chart":
        bool_whisker_chart = True
    else:
        bool_whisker_chart = False

chart_cost_all = vis.visualize_cost_benchmark(
    list_files_chosen,
    df_existing_detail,
    float_error_multiplier,
    bool_whisker_chart,
)
chart_time_all = vis.visualize_time_benchmark(
    list_files_chosen,
    df_existing_detail,
    float_error_multiplier,
    bool_whisker_chart,
)

st.subheader("Cost ", help=tc.STRING_COST_HELP)
st.markdown("Error Multiplier: " + str(float_error_multiplier))
st.plotly_chart(chart_cost_all, use_container_width=True)
st.subheader("Runtime", help=tc.STRING_TIME_HELP)
st.markdown("Error Multiplier: " + str(float_error_multiplier))
st.plotly_chart(chart_time_all, use_container_width=True)
