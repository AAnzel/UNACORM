import plotly.express as px

_DISCRETE_COLOR_PALLETE = px.colors.qualitative.Dark2
_STRING_PLOTLY_THEME = 'plotly_dark'


def visualize_uploaded_plotly(df_report):
    """
    visualize_uploaded_plotly function is used for visualizing the time, cost,
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
        title='Size (in bytes)', barmode='group', text_auto=True,
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        template=_STRING_PLOTLY_THEME)  # ",.0f"

    chart_time = px.bar(
        df_report, x='Method', y='Time', color='Transformation',
        title='Process Time (in seconds)', barmode='group',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        text_auto=True, template=_STRING_PLOTLY_THEME)  # ",.0f"

    chart_cost = px.bar(
        df_report, x='Method', y='Cost', color='Transformation',
        title='Cost (based on length of nucleotides)', barmode='group',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        text_auto=True, template=_STRING_PLOTLY_THEME)

    return chart_size, chart_time, chart_cost


def visualize_size_benchmark_plotly(df_measure_sum_concat):
    """
    visualize_size_benchmark_plotly function is used for visualizing the size
    multipliers from the benchmarking dataset. These multipliers tell us how
    much the size of the encoded file differes from the size of the decoded
    file

    Args:
        df_measure_sum_concat (pd.DataFrame): summary benchmark DataFrame

    Returns:
        chart_multiplier (px.Chart): chart with size multipliers
    """
    chart_multiplier = px.box(
        df_measure_sum_concat, y="Encoding_Multipliers", x='Method',
        template=_STRING_PLOTLY_THEME)
    chart_multiplier.update_traces(marker_color='white')

    return chart_multiplier


def visualize_cost_benchmark_plotly(string_file_chosen, df_concat):
    """
    visualize_cost_benchmark_plotly function is used for visualizing the
    encoding/decoding costs for each encoding method

    Args:
        string_file_chosen (str): name of file that want to be showed
        df_concat (dataframe): detail benchmarking dataset

    Returns:
        chart_cost (px.Chart): chart with costs
    """
    df_tmp = df_concat[df_concat['Filename'].isin(string_file_chosen)].groupby(
        ['Filename', 'Method', 'Transformation',
         'Size', 'Type']).mean().reset_index()

    chart_cost = px.bar(
        df_tmp,
        x='Method', y='Cost', color='Transformation', facet_col='Filename',
        title='Cost (based on length of nucleotides)', barmode='group',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE, text_auto=True,
        template=_STRING_PLOTLY_THEME)

    return chart_cost


def visualize_time_benchmark_plotly(string_file_chosen, df_concat):
    """
    visualize_time_benchmark_plotly function is used for visualizing run times
    it took each method to encode/decode files

    Args:
        string_file_chosen (str): chosen filename will be used for filtering
        which data will be shown
        df_concat (dataframe): concanated detail precalculated data and data
        from uploaded file

    Returns:
        chart_time (px.Chart): chart with times
    """
    df_tmp = df_concat[df_concat['Filename'].isin(string_file_chosen)]

    chart_time = px.box(
        df_tmp, x='Method', y='Time', color='Transformation',
        title='Process Time (in seconds)', facet_col='Filename',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        template=_STRING_PLOTLY_THEME)  # ",.0f"

    return chart_time
