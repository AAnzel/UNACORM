import os

import pandas as pd
import utilities as uti
import visualize as vis

_PATH_FIGURES = os.path.join(uti.PATH_CACHE_DATA, "benchmark_figures")
os.makedirs(_PATH_FIGURES, exist_ok=True)
df_existing_summary = pd.read_pickle(uti.PATH_EXISTING_SUMMARY)
df_existing_detail = pd.read_pickle(uti.PATH_EXISTING_DETAIL)
list_files_to_visualize = list(pd.unique(df_existing_summary["Filename"]))


dict_charts_no_multipliers = {
    "density": vis.visualize_density_benchmark(df_existing_summary),
    "sucess_rate": vis.visualize_success_rate_general(df_existing_detail),
    "base_error": vis.visualize_base_error_general(
        df_existing_detail, list_files_to_visualize
    ),
}

dict_charts_with_multipliers = {
    "sucess_rate_per_multiplier": {},
    "sucess_rate_per_multiplier_and_file": {},
    "information_density_per_multiplier": {},
    "information_density_per_multiplier_and_file": {},
    "cost_all_bar": {},
    "cost_all_whisker": {},
    "time_all_bar": {},
    "time_all_whisker": {},
}

for float_error_multiplier in uti.LIST_FLOAT_ERROR_MULTIPLIERS:
    dict_charts_with_multipliers["sucess_rate_per_multiplier"][
        str(float_error_multiplier)
    ] = vis.visualize_sucess_rate_per_multiplier(
        list_files_to_visualize, df_existing_detail, float_error_multiplier
    )

    dict_charts_with_multipliers["sucess_rate_per_multiplier_and_file"][
        str(float_error_multiplier)
    ] = vis.visualize_sucess_rate_per_multiplier_and_file(
        list_files_to_visualize, df_existing_detail, float_error_multiplier
    )

    dict_charts_with_multipliers["information_density_per_multiplier"][
        str(float_error_multiplier)
    ] = vis.visualize_density_per_multiplier(
        list_files_to_visualize, df_existing_summary, float_error_multiplier
    )

    dict_charts_with_multipliers["information_density_per_multiplier_and_file"][
        str(float_error_multiplier)
    ] = vis.visualize_density_per_multiplier_and_file(
        list_files_to_visualize, df_existing_summary, float_error_multiplier
    )

    dict_charts_with_multipliers["cost_all_bar"][
        str(float_error_multiplier)
    ] = vis.visualize_cost_benchmark(
        list_files_to_visualize,
        df_existing_detail,
        float_error_multiplier,
        False,
    )

    dict_charts_with_multipliers["cost_all_whisker"][
        str(float_error_multiplier)
    ] = vis.visualize_cost_benchmark(
        list_files_to_visualize,
        df_existing_detail,
        float_error_multiplier,
        True,
    )
    dict_charts_with_multipliers["time_all_bar"][
        str(float_error_multiplier)
    ] = vis.visualize_time_benchmark(
        list_files_to_visualize,
        df_existing_detail,
        float_error_multiplier,
        False,
    )

    dict_charts_with_multipliers["time_all_whisker"][
        str(float_error_multiplier)
    ] = vis.visualize_time_benchmark(
        list_files_to_visualize,
        df_existing_detail,
        float_error_multiplier,
        True,
    )

# We now save the figures
for string_figure_name, chart_figure in dict_charts_no_multipliers.items():
    path_figure = os.path.join(
        _PATH_FIGURES, string_figure_name + "_general" + ".pdf"
    )
    if string_figure_name in ["success_rate", "density"]:
        chart_figure.write_image(path_figure)
    else:
        chart_figure.write_image(path_figure, width=1000, height=1200, scale=2)

for (
    string_figure_name,
    dict_errors_charts,
) in dict_charts_with_multipliers.items():
    for string_error_multiplier, chart_figure in dict_errors_charts.items():
        path_figure = os.path.join(
            _PATH_FIGURES,
            string_figure_name + "_error_" + string_error_multiplier + ".pdf",
        )

        if string_figure_name in [
            "information_density_per_multiplier",
            "sucess_rate_per_multiplier",
        ]:
            chart_figure.write_image(path_figure)
        else:
            chart_figure.write_image(
                path_figure, width=1000, height=1200, scale=2
            )
