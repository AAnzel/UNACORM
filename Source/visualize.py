import plotly.express as px
import streamlit as st

__author__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian']
__copyright__ = ''
__credits__ = ['Aleksandar Anžel', 'Ihsan Tri Heldian', 'Chisom Ezekannagha']
__license__ = 'GNU General Public License v3.0'
__version__ = '1.0.0'
__maintainer__ = 'Aleksandar Anžel'
__email__ = 'AnzelA@rki.de'
__status__ = 'Stable'



_STRING_PLOTLY_THEME = 'simple_white' if st.get_option('theme.base') == 'light' else 'plotly_dark'  # noqa
_STRING_DENSITY_MARKER_COLOR = 'white' if _STRING_PLOTLY_THEME == 'plotly_dark' else '#43464b'  # noqa
_DISCRETE_COLOR_PALLETE = px.colors.qualitative.Dark2 if _STRING_PLOTLY_THEME == 'plotly_dark' else  px.colors.qualitative.D3  # noqa
_INT_CHART_ROW_SIZE = 400
_INT_CHART_TITLE_SIZE = 24


# TODO: Decide if we want to visualize measures only for successful encode
# TODO: and decode processes. If so, we should use the failure rate filter
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

    chart_size = px.bar(
        df_report, x='Method', y='Size', color='Transformation',
        barmode='group', text_auto=True,
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        height=_INT_CHART_ROW_SIZE,
        template=_STRING_PLOTLY_THEME).update_layout(
            yaxis_title='Size(b)', yaxis_showgrid=True)

    chart_time = px.bar(
        df_report, x='Method', y='Time', color='Transformation',
        barmode='group', height=_INT_CHART_ROW_SIZE,
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        text_auto=True, template=_STRING_PLOTLY_THEME).update_layout(
            yaxis_title='Time(s)', yaxis_showgrid=True)

    chart_cost = px.bar(
        df_report, x='Method', y='Cost', color='Transformation',
        barmode='group', height=_INT_CHART_ROW_SIZE,
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        text_auto=True, template=_STRING_PLOTLY_THEME).update_layout(
            yaxis_title='Cost($)', yaxis_showgrid=True)

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
        df_measure_sum_concat.sort_values('Method'),
        y="Information_Density", x='Method',
        height=_INT_CHART_ROW_SIZE * 1.5, template=_STRING_PLOTLY_THEME)
    chart_density.update_traces(
        marker_color=_STRING_DENSITY_MARKER_COLOR)
    chart_density.for_each_xaxis(
        lambda xaxis: xaxis.update(showticklabels=True))
    chart_density.update_layout(yaxis_title='Information_Density (b/nt)')
    # TODO: Make it into a bar chart for uploaded data
    chart_density.update_yaxes(showgrid=True)

    return chart_density


def visualize_cost_benchmark(list_files_chosen, df_detail,
                             float_error_multiplier, bool_whisker):
    """
    visualize_cost_benchmark function is used for visualizing the
    encoding/decoding costs for each encoding method

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
        (df_detail['Filename'].isin(list_files_chosen)
         & (df_detail['Error_Multiplier'] == float_error_multiplier))].groupby(
             ['Filename', 'Method', 'Transformation',
              'Size', 'Type']).mean().sort_values('Method').reset_index(
                  ).rename(columns={'Cost': 'Cost($)'})

    chart_cost = None

    if bool_whisker:
        chart_cost = px.box(
            df_tmp,
            x='Method', y='Cost($)', color='Transformation',
            facet_col='Filename', facet_col_wrap=4,
            facet_row_spacing=0.12,  # Default=0.07 when facet_col_wrap is used
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            height=_INT_CHART_ROW_SIZE * (
                int((len(list_files_chosen) - 1) / 4) + 1),
            template=_STRING_PLOTLY_THEME,
            category_orders={'Filename': list_files_chosen})

    else:
        chart_cost = px.bar(
            df_tmp,
            x='Method', y='Cost($)', color='Transformation',
            facet_col='Filename', facet_col_wrap=4,
            facet_row_spacing=0.12,  # Default=0.07 when facet_col_wrap is used
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
            height=_INT_CHART_ROW_SIZE * (
                int((len(list_files_chosen) - 1) / 4) + 1),
            template=_STRING_PLOTLY_THEME, barmode='group',
            category_orders={'Filename': list_files_chosen})

    chart_cost.for_each_xaxis(
        lambda xaxis: xaxis.update(showticklabels=True))

    chart_cost.update_yaxes(showgrid=True)

    return chart_cost


def visualize_time_benchmark(list_files_chosen, df_detail,
                             float_error_multiplier, bool_whisker=True):
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
        (df_detail['Filename'].isin(list_files_chosen)
         & (df_detail['Error_Multiplier']
            == float_error_multiplier))].sort_values('Method').rename(
                columns={'Time': 'log(Time(s))'})

    chart_time = None

    if bool_whisker:
        chart_time = px.box(
            df_tmp, x='Method', y='log(Time(s))', color='Transformation',
            log_y=True, facet_col='Filename',
            facet_row_spacing=0.12,  # Default=0.07 when facet_col_wrap is used
            height=_INT_CHART_ROW_SIZE * (
                int((len(list_files_chosen) - 1) / 4) + 1),
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE, facet_col_wrap=4,
            template=_STRING_PLOTLY_THEME,
            category_orders={'Filename': list_files_chosen})
    else:
        chart_time = px.bar(
            df_tmp, x='Method', y='log(Time(s))', color='Transformation',
            log_y=True, facet_col='Filename',
            facet_row_spacing=0.12,  # Default=0.07 when facet_col_wrap is used
            height=_INT_CHART_ROW_SIZE * (
                int((len(list_files_chosen) - 1) / 4) + 1),
            color_discrete_sequence=_DISCRETE_COLOR_PALLETE, facet_col_wrap=4,
            template=_STRING_PLOTLY_THEME, barmode='group',
            category_orders={'Filename': list_files_chosen})

    chart_time.for_each_xaxis(
        lambda xaxis: xaxis.update(showticklabels=True))
    chart_time.update_yaxes(showgrid=True)

    return chart_time


def visualize_base_error_per_file(list_files_chosen, df_measure_sum_concat,
                                  float_error_multiplier):
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
    df_tmp = df_measure_sum_concat[(
        df_measure_sum_concat['Filename'].isin(
            list_files_chosen))].sort_values('Method')

    chart_base_error = px.line(
        df_tmp, x='Base_error_ratio', y='Information_Density', color='Method',
        facet_col='Filename',
        facet_row_spacing=0.12,  # Default is 0.07 when facet_col_wrap is used
        height=_INT_CHART_ROW_SIZE * (
            int((len(list_files_chosen) - 1) / 4) + 1),
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE, facet_col_wrap=4,
        template=_STRING_PLOTLY_THEME,
        category_orders={'Filename': list_files_chosen})

    chart_base_error.for_each_xaxis(
        lambda xaxis: xaxis.update(showticklabels=True))

    chart_base_error.update_yaxes(showgrid=True)

    return chart_base_error


def visualize_base_error_general(df_measure_sum_concat):
    """
    visualize_base_error_general function is used for visualizing base error
    values for each method across all runs and files

    Args:
        df_measure_sum_concat (pd.DataFrame): summary benchmark DataFrame

    Returns:
        chart_base_error (px.Chart): chart with base error values
    """
    chart_base_error = px.line(
        df_measure_sum_concat.sort_values('Method'), x='Mean_Base_Error_Ratio',
        y='Information_Density', color='Method',
        facet_col='Error_Multiplier', facet_col_wrap=3,
        facet_row_spacing=0.12,  # Default is 0.07 when facet_col_wrap is used
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        height=_INT_CHART_ROW_SIZE * 1.5, template=_STRING_PLOTLY_THEME)

    chart_base_error.update_layout(yaxis_title='Information Density (b/nt)')
    chart_base_error.for_each_xaxis(
        lambda xaxis: xaxis.update(showticklabels=True))
    # ! FIX: Find the appropriate aggregation
    chart_base_error.update_yaxes(showgrid=True)

    return chart_base_error


def visualize_failure_rate_general(df_detail):
    """
    visualize_failure_rate_general function is used for visualizing the failure
    rates for each method across all runs, files, and error multipliers

    Args:
        df_detail (pd.DataFrame): detail benchmarking dataset

    Returns:
        chart_density (px.Chart): chart with information density
    """
    df_tmp = df_detail.copy()
    df_tmp['Is_Failure'] = (df_tmp['Mean_Num_of_Errors'] == 0) \
        & (df_tmp['Mean_Base_Error_Ratio'] == 0)

    df_failure_counts = df_tmp.groupby('Method')[
        'Is_Failure'].sum().reset_index()
    df_failure_counts.rename(columns={'Is_Failure': 'Number_of_Failures'},
                             inplace=True)

    df_total_counts = df_tmp.groupby('Method').size().reset_index(
        name='Total_Attempts')

    failure_rate_df = df_failure_counts.merge(df_total_counts, on='Method')
    failure_rate_df['Failure Rate (%)'] = (
        failure_rate_df['Number_of_Failures']
        / failure_rate_df['Total_Attempts']) * 100

    df_tmp = df_tmp.merge(failure_rate_df[['Method', 'Failure Rate (%)']],
                          on='Method', how='left')

    df_tmp = df_tmp.filter(['Method', 'Failure Rate (%)']).groupby(
        ['Method']).agg({'Failure Rate (%)': 'first'}).reset_index()

    chart_failure_rate = px.bar(
        df_tmp, x='Method', y='Failure Rate (%)', text='Failure Rate (%)',
        height=_INT_CHART_ROW_SIZE * 1.5, template=_STRING_PLOTLY_THEME)

    chart_failure_rate.update_traces(
        marker_color=_STRING_DENSITY_MARKER_COLOR)
    chart_failure_rate.for_each_xaxis(
        lambda xaxis: xaxis.update(showticklabels=True))

    chart_failure_rate.update_yaxes(range=[0, 100], showgrid=True)
    chart_failure_rate.update_traces(texttemplate='%{y:.2f}%')

    return chart_failure_rate
