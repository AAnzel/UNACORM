import os

import pandas as pd
import plotly.express as px
import streamlit as st
from utilities import PATH_CACHE_DATA

__author__ = ["Aleksandar Anžel", "Ihsan Tri Heldian"]
__copyright__ = ""
__credits__ = ["Aleksandar Anžel", "Ihsan Tri Heldian", "Chisom Ezekannagha"]
__license__ = "GNU General Public License v3.0"
__version__ = "1.0.0"
__maintainer__ = "Aleksandar Anžel"
__email__ = "AnzelA@rki.de"
__status__ = "Stable"


_STRING_PLOTLY_THEME = (
    "simple_white" if st.get_option("theme.base") == "light" else "plotly_dark"
)
_STRING_DENSITY_MARKER_COLOR = (
    "white" if _STRING_PLOTLY_THEME == "plotly_dark" else "#43464b"
)
_DISCRETE_COLOR_PALLETE = (
    px.colors.qualitative.Dark2
    if _STRING_PLOTLY_THEME == "plotly_dark"
    else px.colors.qualitative.Set2
)
_INT_CHART_ROW_SIZE = 400
_INT_CHART_TITLE_SIZE = 24
_BOOL_SAVE_FIGURES = False


# TODO: Decide if we want to visualize measures only for successful encode
# TODO: and decode processes. If so, we should use the Success Rate filter
def visualize_uploaded(df_report):
    """
    visualize_uploaded function is used for visualizing the time, cost,
    and size results for data given in df_report

    Args:
        df_report (pd.DataFrame): DataFrame containing detailed benchmark
        results

    Returns:
        chart_size (px.Chart): chart with sizes
        chart_time (px.Chart): chart with run times
        chart_cost (px.Chart): chart with encoding/decoding costs
    """

    chart_size = (
        px
        .bar(
            df_report,
            x="Method",
            y="Size",
            color="Transformation",
            barmode="group",
            text_auto=True,
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            height=_INT_CHART_ROW_SIZE,
            template=_STRING_PLOTLY_THEME,
        )
        .update_layout(yaxis_title="Size(b)", yaxis_showgrid=True)
        .update_traces(
            marker_cornerradius="5%",
        )
    )

    chart_time = (
        px
        .bar(
            df_report,
            x="Method",
            y="Time",
            color="Transformation",
            barmode="group",
            height=_INT_CHART_ROW_SIZE,
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            text_auto=True,
            template=_STRING_PLOTLY_THEME,
        )
        .update_layout(yaxis_title="Time(s)", yaxis_showgrid=True)
        .update_traces(
            marker_cornerradius="5%",
        )
    )

    chart_cost = (
        px
        .bar(
            df_report,
            x="Method",
            y="Cost",
            color="Transformation",
            barmode="group",
            height=_INT_CHART_ROW_SIZE,
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            text_auto=True,
            template=_STRING_PLOTLY_THEME,
        )
        .update_layout(yaxis_title="Cost($)", yaxis_showgrid=True)
        .update_traces(
            marker_cornerradius="5%",
        )
    )

    return chart_size, chart_time, chart_cost


def visualize_density_benchmark(df_measure_sum_concat):
    """
    visualize_density_benchmark function is used for visualizing the
    information densities from the benchmarking dataset. These densities tell
    us how much the size of the encoded file differes from the size of the
    decoded file

    Args:
        df_measure_sum_concat (pd.DataFrame): summary benchmark DataFrame

    Returns:
        chart_density (px.Chart): chart with information density
    """
    chart_density = px.box(
        df_measure_sum_concat.sort_values("Method"),
        y="Information_Density",
        x="Method",
        height=_INT_CHART_ROW_SIZE,
        template=_STRING_PLOTLY_THEME,
    )
    chart_density.update_traces(marker_color=_STRING_DENSITY_MARKER_COLOR)

    chart_density.update_xaxes(showticklabels=True)
    chart_density.update_layout(yaxis_title="Information_Density (b/nt)")
    # TODO: Make it into a bar chart for uploaded data
    chart_density.update_yaxes(showgrid=True)

    if _BOOL_SAVE_FIGURES:
        chart_density.write_image(
            os.path.join(PATH_CACHE_DATA, "benchmark_figures", "density.pdf")
        )

    return chart_density


def visualize_cost_benchmark(
    list_files_chosen, df_detail, float_error_multiplier, bool_whisker
):
    """
    visualize_cost_benchmark function is used for visualizing the
    encoding/decoding costs for each codec

    Args:
        list_files_chosen (list): names of files that are to be visualized
        df_detail (pd.DataFrame): detail benchmarking dataset
        float_error_multiplier (float): selected error multiplier to filter the
        df_detail
        bool_whisker (bool): determines if the chart should be whisker or bar.
        Default: True

    Returns:
        chart_cost (px.Chart): chart with costs
    """

    df_tmp = df_detail[
        (
            df_detail["Filename"].isin(list_files_chosen)
            & (df_detail["Error_Multiplier"] == float_error_multiplier)
        )
    ]

    chart_cost = None

    if bool_whisker:
        df_tmp = (
            df_tmp[["Filename", "Method", "Transformation", "Cost"]]
            .sort_values("Method")
            .rename(columns={"Cost": "Cost($)"})
        )

        chart_cost = px.box(
            df_tmp,
            x="Method",
            y="Cost($)",
            log_y=True,
            color="Transformation",
            facet_col="Filename",
            facet_col_wrap=4,
            facet_row_spacing=0.16,  # Default=0.07 when facet_col_wrap is used
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            height=_INT_CHART_ROW_SIZE
            * (int((len(list_files_chosen) - 1) / 4) + 1),
            template=_STRING_PLOTLY_THEME,
            category_orders={"Filename": list_files_chosen},
        )

    else:
        df_tmp = (
            df_tmp[["Filename", "Method", "Transformation", "Cost"]]
            .groupby(["Filename", "Method", "Transformation"])
            .median()
            .sort_values("Method")
            .reset_index()
            .rename(columns={"Cost": "Cost($)"})
        )

        chart_cost = px.bar(
            df_tmp,
            x="Method",
            y="Cost($)",
            log_y=True,
            color="Transformation",
            facet_col="Filename",
            facet_col_wrap=4,
            facet_row_spacing=0.16,  # Default=0.07 when facet_col_wrap is used
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            height=_INT_CHART_ROW_SIZE
            * (int((len(list_files_chosen) - 1) / 4) + 1),
            template=_STRING_PLOTLY_THEME,
            barmode="group",
            category_orders={"Filename": list_files_chosen},
        ).update_traces(
            marker_cornerradius="5%",
        )

    chart_cost.update_xaxes(showticklabels=True)
    chart_cost.update_yaxes(showgrid=True)

    if _BOOL_SAVE_FIGURES:
        chart_cost.write_image(
            os.path.join(PATH_CACHE_DATA, "benchmark_figures", "cost.pdf")
        )

    return chart_cost


def visualize_time_benchmark(
    list_files_chosen, df_detail, float_error_multiplier, bool_whisker=True
):
    """
    visualize_time_benchmark function is used for visualizing run times it took
    each method to encode/decode files

    Args:
        list_files_chosen (list): names of files that are to be visualized
        df_detail (pd.DataFrame): detail benchmarking dataset
        float_error_multiplier (float): selected error multiplier to filter the
        df_detail
        bool_whisker (bool): determines if the chart should be whisker or bar.
        Default: True

    Returns:
        chart_time (px.Chart): chart with times
    """

    df_tmp = df_detail[
        (
            df_detail["Filename"].isin(list_files_chosen)
            & (df_detail["Error_Multiplier"] == float_error_multiplier)
        )
    ]

    chart_time = None

    if bool_whisker:
        df_tmp = (
            df_tmp[["Filename", "Method", "Transformation", "Time"]]
            .sort_values("Method")
            .rename(columns={"Time": "Time(s)"})
        )

        chart_time = px.box(
            df_tmp,
            x="Method",
            y="Time(s)",
            color="Transformation",
            log_y=True,
            facet_col="Filename",
            facet_row_spacing=0.16,  # Default=0.07 when facet_col_wrap is used
            height=_INT_CHART_ROW_SIZE
            * (int((len(list_files_chosen) - 1) / 4) + 1),
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            facet_col_wrap=4,
            template=_STRING_PLOTLY_THEME,
            category_orders={"Filename": list_files_chosen},
        )
    else:
        df_tmp = (
            df_tmp[["Filename", "Method", "Transformation", "Time"]]
            .groupby(["Filename", "Method", "Transformation"])
            .median()
            .sort_values("Method")
            .reset_index()
            .rename(columns={"Time": "Time(s)"})
        )

        chart_time = px.bar(
            df_tmp,
            x="Method",
            y="Time(s)",
            color="Transformation",
            log_y=True,
            facet_col="Filename",
            facet_row_spacing=0.16,  # Default=0.07 when facet_col_wrap is used
            height=_INT_CHART_ROW_SIZE
            * (int((len(list_files_chosen) - 1) / 4) + 1),
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            facet_col_wrap=4,
            template=_STRING_PLOTLY_THEME,
            barmode="group",
            category_orders={"Filename": list_files_chosen},
        ).update_traces(
            marker_cornerradius="5%",
        )

    chart_time.update_xaxes(showticklabels=True)
    chart_time.update_yaxes(showgrid=True)  # , title="log(Time(s))")

    if _BOOL_SAVE_FIGURES:
        chart_time.write_image(
            os.path.join(PATH_CACHE_DATA, "benchmark_figures", "time.pdf")
        )

    return chart_time


def visualize_base_error_per_file(
    list_files_chosen, df_measure_sum_concat, float_error_multiplier
):
    """
    visualize_base_errorper_file function is used for visualizing base
    error values for each method per file across all runs

    Args:
        list_files_chosen (list): names of files that are to be visualized
        df_measure_sum_concat (pd.DataFrame): summary benchmark DataFrame
        float_error_multiplier (float): selected error multiplier to filter the
        df_detail

    Returns:
        chart_base_error (px.Chart): chart with base error values
    """
    df_tmp = df_measure_sum_concat[
        (df_measure_sum_concat["Filename"].isin(list_files_chosen))
    ].sort_values("Method")

    chart_base_error = px.line(
        df_tmp,
        x="Base_error_ratio",
        y="Information_Density",
        color="Method",
        facet_col="Filename",
        facet_row_spacing=0.16,  # Default is 0.07 when facet_col_wrap is used
        height=_INT_CHART_ROW_SIZE
        * (int((len(list_files_chosen) - 1) / 4) + 1),
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        facet_col_wrap=4,
        template=_STRING_PLOTLY_THEME,
        category_orders={"Filename": list_files_chosen},
    )

    chart_base_error.update_xaxes(showticklabels=True)
    chart_base_error.update_yaxes(showgrid=True)

    if _BOOL_SAVE_FIGURES:
        chart_base_error.write_image(
            os.path.join(PATH_CACHE_DATA, "benchmark_figures", "base_error.pdf")
        )

    return chart_base_error


def visualize_base_error_general(df_detail):
    """
    visualize_base_error_general function is used for visualizing base error
    values for each method across all runs and files

    Args:
        df_detail (pd.DataFrame): detail benchmark DataFrame

    Returns:
        chart_base_error (px.Chart): chart with base error values
    """
    df_tmp = df_detail.copy()

    df_success_rate = (
        df_tmp
        .groupby(["Method", "Filename", "Error_Multiplier"])
        .agg({"Similarity": "mean", "Base_error_ratio": "max"})
        .reset_index()
    )

    df_success_rate["Similarity"] = df_success_rate["Similarity"] * 100

    df_success_rate = df_success_rate.rename(
        columns={"Similarity": "Success Rate (%)"}
    )

    # Now we calculate the last ratio, in which the code had a 100% success rate
    # (out of 5 repetitions) and up until the first time, the code had a zero
    # percent success rate

    df_success_rate = df_success_rate.sort_values([
        "Method",
        "Filename",
        "Base_error_ratio",
    ]).reset_index(drop=True)

    # Compute previous success rate for each (Method, Filename) group
    df_success_rate["Prev_Success"] = df_success_rate.groupby([
        "Method",
        "Filename",
    ])["Success Rate (%)"].shift(1)

    # Find drops from 100% to <100%
    df_drops = df_success_rate[
        (df_success_rate["Prev_Success"] == 100)
        & (df_success_rate["Success Rate (%)"] < 100)
    ]

    # Rows for (Method, Filename) where drop never happens (always 100%), keep max Base_error_ratio
    df_max_rows = df_success_rate.loc[
        df_success_rate.groupby(["Method", "Filename"])[
            "Base_error_ratio"
        ].idxmax()
    ]

    # Combine, prefer drop rows if available
    df_final = (
        pd
        .concat([
            df_drops,
            df_max_rows[
                ~df_max_rows.set_index(["Method", "Filename"]).index.isin(
                    df_drops.set_index(["Method", "Filename"]).index
                )
            ],
        ])
        .sort_values(["Method", "Filename"])
        .reset_index(drop=True)
    )

    df_final = df_final[
        ["Method", "Filename", "Success Rate (%)", "Base_error_ratio"]
    ]

    chart_base_error = px.line(
        df_final,
        x="Base_error_ratio",
        y="Success Rate (%)",
        color="Method",
        markers=True,
        facet_col="Filename",
        facet_col_wrap=3,
        facet_row_spacing=0.16,  # Default is 0.07 when facet_col_wrap is used
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        height=_INT_CHART_ROW_SIZE * 2,
        template=_STRING_PLOTLY_THEME,
    )

    chart_base_error.update_xaxes(
        showticklabels=True,
        range=[-0.05, 1],
    )
    chart_base_error.update_yaxes(
        showgrid=True,
        range=[-5, 105],
        zeroline=True,
    )
    chart_base_error.update_traces(line=dict(dash="dash"))

    if _BOOL_SAVE_FIGURES:
        chart_base_error.write_image(
            os.path.join(
                PATH_CACHE_DATA, "benchmark_figures", "base_error_general.pdf"
            )
        )

    return chart_base_error


def visualize_success_rate_general(df_detail):
    """
    visualize_success_rate_general function is used for visualizing the success
    rates for each method across all runs, files, and error multipliers

    Args:
        df_detail (pd.DataFrame): detail benchmarking dataset

    Returns:
        chart_success_rate (px.Chart): chart with success rates
    """
    df_tmp = df_detail.copy()

    df_success_rate = (
        df_tmp.groupby("Method")["Similarity"].mean().reset_index()
    )

    df_success_rate["Similarity"] = df_success_rate["Similarity"] * 100

    df_success_rate = df_success_rate.rename(
        columns={"Similarity": "Success Rate (%)"}
    )

    chart_success_rate = px.bar(
        df_success_rate,
        x="Method",
        y="Success Rate (%)",
        text="Success Rate (%)",
        height=_INT_CHART_ROW_SIZE,
        template=_STRING_PLOTLY_THEME,
    )

    chart_success_rate.update_traces(
        marker_color=_STRING_DENSITY_MARKER_COLOR,
        marker_line_color=_STRING_DENSITY_MARKER_COLOR,
        marker_line_width=4,
        marker_cornerradius="5%",
        texttemplate="%{y:.2f}%",
        textposition="outside",
    )
    chart_success_rate.update_xaxes(showticklabels=True)

    chart_success_rate.update_yaxes(
        range=[0, 110],
        showgrid=True,
        zeroline=True,
    )

    if _BOOL_SAVE_FIGURES:
        chart_success_rate.write_image(
            os.path.join(
                PATH_CACHE_DATA, "benchmark_figures", "success_rate.pdf"
            )
        )

    return chart_success_rate


def visualize_success_rate_per_multiplier(
    list_files_chosen, df_detail, float_error_multiplier
):
    """
    visualize_time_benchmark function is used for visualizing run times it took
    each method to encode/decode files

    Args:
        list_files_chosen (list): names of files that are to be visualized
        df_detail (pd.DataFrame): detail benchmarking dataset
        float_error_multiplier (float): selected error multiplier to filter the
        df_detail

    Returns:
        chart_success_rate (px.Chart): chart with success rates
    """

    df_tmp = df_detail[
        (
            df_detail["Filename"].isin(list_files_chosen)
            & (df_detail["Error_Multiplier"] == float_error_multiplier)
            & (df_detail["Transformation"] == "Decoding")
        )
    ]

    df_tmp["Similarity"] = df_tmp["Similarity"] * 100
    df_tmp.reset_index(inplace=True)
    df_tmp["index"] = df_tmp["index"] % 5

    df_tmp = (
        df_tmp[["index", "Filename", "Method", "Similarity"]]
        .sort_values("Method")
        .rename(columns={"Similarity": "Success Rate (%)", "index": "Run"})
    )

    chart_success_rate = px.strip(
        df_tmp,
        x="Method",
        y="Success Rate (%)",
        color="Run",
        facet_col="Filename",
        facet_row_spacing=0.16,  # Default=0.07 when facet_col_wrap is used
        height=_INT_CHART_ROW_SIZE
        * (int((len(list_files_chosen) - 1) / 4) + 1),
        facet_col_wrap=4,
        template=_STRING_PLOTLY_THEME,
        category_orders={"Filename": list_files_chosen},
        stripmode="group",
    )

    chart_success_rate.update_traces(marker_color=_STRING_DENSITY_MARKER_COLOR)
    chart_success_rate.update_xaxes(showticklabels=True)
    chart_success_rate.update_yaxes(showgrid=True)
    chart_success_rate.update_layout(showlegend=False)

    if _BOOL_SAVE_FIGURES:
        chart_success_rate.write_image(
            os.path.join(
                PATH_CACHE_DATA, "benchmark_figures", "success_rate.pdf"
            )
        )

    return chart_success_rate
