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


df_existing_summary = pd.read_pickle(uti.PATH_EXISTING_SUMMARY)
df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)
list_files_to_visualize = list(pd.unique(df_existing_summary["Filename"]))

st.header(":primary[︱]Benchmark", help=tc.STRING_MAIN_BENCHMARK_HELP)
st.space(size="medium")
uti.display_processed_data(df_existing_summary, df_existing_detail)
st.divider()

st.header(":primary[︱]Information Density", help=tc.STRING_DENSITY_HELP)
chart_density = vis.visualize_density_benchmark(df_existing_summary)
st.plotly_chart(chart_density, width="stretch")

st.header(":primary[︱]Success Rate", help=tc.STRING_SUCCESS_RATE_HELP)
chart_success_rate = vis.visualize_success_rate_general(df_existing_detail)
st.plotly_chart(chart_success_rate, width="stretch")

st.header(":primary[︱]Base Error", help=tc.STRING_BASE_ERROR_HELP)
chart_base_error = vis.visualize_base_error_general(
    df_existing_detail, list_files_to_visualize
)
st.plotly_chart(chart_base_error, width="stretch")


st.header(":primary[︱]Detailed Charts per File and Error Multiplier")
st.space(size="small")

with st.container(
    border=True,
    horizontal=True,
    horizontal_alignment="distribute",
    gap="medium",
):
    with st.container(width=500):
        float_error_multiplier = st.select_slider(
            "Choose error multiplier value or leave it 0 to skip",
            value=uti.LIST_FLOAT_ERROR_MULTIPLIERS[0],
            options=uti.LIST_FLOAT_ERROR_MULTIPLIERS,
            key="detailed_charts_error_multiplier_slider",
        )
        with st.popover(
            "What is error multiplier?", icon=":material/help:", width="stretch"
        ):
            st.markdown(tc.STRING_MUTAGENESIS_HELP)

    list_files_chosen = st.multiselect(
        "Select the files to review (This will affect charts below)",
        default=list_files_to_visualize,
        options=list_files_to_visualize,
        placeholder="Choose files",
        key="detailed_charts_multiselect",
        width=800,
    )

chart_success_rate_per_multiplier = vis.visualize_success_rate_per_multiplier(
    list_files_chosen, df_existing_detail, float_error_multiplier
)

chart_success_rate_per_multiplier_and_file = (
    vis.visualize_success_rate_per_multiplier_and_file(
        list_files_chosen, df_existing_detail, float_error_multiplier
    )
)

chart_information_density_per_multiplier = vis.visualize_density_per_multiplier(
    list_files_chosen, df_existing_summary, float_error_multiplier
)

chart_information_density_per_multiplier_and_file = (
    vis.visualize_density_per_multiplier_and_file(
        list_files_chosen, df_existing_summary, float_error_multiplier
    )
)

st.subheader(
    "Success Rate"
    + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    + ":small[Error Multiplier: "
    + ":primary-background[ "
    + str(float_error_multiplier)
    + "]]",
    help=tc.STRING_SUCCESS_RATE_HELP,
)
st.plotly_chart(chart_success_rate_per_multiplier, width="stretch")
st.plotly_chart(chart_success_rate_per_multiplier_and_file, width="stretch")

st.subheader(
    "Information Density"
    + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    + ":small[Error Multiplier: "
    + ":primary-background[ "
    + str(float_error_multiplier)
    + "]]",
    help=tc.STRING_DENSITY_HELP,
)
st.plotly_chart(chart_information_density_per_multiplier, width="stretch")
st.plotly_chart(
    chart_information_density_per_multiplier_and_file, width="stretch"
)

with st.container(
    border=False,
    horizontal=True,
    horizontal_alignment="center",
    vertical_alignment="bottom",
):
    st.header(
        ":primary[︱]Cost and Runtime per File and Error Multiplier",
        help=tc.STRING_COST_RUNTIME,
    )

    string_selected_visualization = st.pills(
        "Visualize using",
        [
            ":material/bar_chart: Bar Chart",
            ":material/candlestick_chart: Whisker Chart",
        ],
        default=":material/bar_chart: Bar Chart",
    )
    st.markdown(
        ":yellow-background[:small[The y-axes use a logarithmic scale]]"
    )

if (
    string_selected_visualization
    == ":material/candlestick_chart: Whisker Chart"
):
    bool_whisker_chart = True
else:
    bool_whisker_chart = False

st.space(size="small")

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

st.subheader(
    "Cost"
    + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    + ":small[Error Multiplier: "
    + ":primary-background[ "
    + str(float_error_multiplier)
    + "]]",
    help=tc.STRING_COST_HELP,
)

st.plotly_chart(chart_cost_all, width="stretch")
st.subheader(
    "Runtime"
    + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    + ":small[Error Multiplier: "
    + ":primary-background[ "
    + str(float_error_multiplier)
    + "]]",
    help=tc.STRING_TIME_HELP,
)

st.plotly_chart(chart_time_all, width="stretch")


uti.display_footer()
