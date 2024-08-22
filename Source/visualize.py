import plotly.express as px

_DISCRETE_COLOR_PALLETE = px.colors.qualitative.Dark2


def visualize_uploaded_plotly(df_report):
    """This function is used for visualizing the results (time, cost, size)
    for uploaded file

    Args:
        df_report (dataframe): dataframe of detail results of uploaded file
    """

    chart_size = px.bar(
        df_report, x='Method', y='Size', color='Transformation',
        title='Size (in bytes)', barmode='group', text_auto=True,
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE)  # ",.0f"

    chart_time = px.bar(
        df_report, x='Method', y='Time', color='Transformation',
        title='Process Time (in seconds)', barmode='group',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        text_auto=True)  # ",.0f"

    chart_cost = px.bar(
        df_report, x='Method', y='Cost', color='Transformation',
        title='Cost (based on length of nucleotides)', barmode='group',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE,
        text_auto=True)

    return chart_size, chart_time, chart_cost


def visualize_size_benchmark_plotly(df_measure_sum_concat):
    """This function is used for visualizing the size multipliers from the
    benchmarking dataset

    Args:
        df_measure_sum_concat (dataframe): summary dataframe from concanated
        precalculated data with result of uploaded
        file (benchmarking dataset)
    """
    chart_multiplier = px.box(
        df_measure_sum_concat, y="Encoding_Multipliers", x='Method')
    chart_multiplier.update_traces(marker_color='white')
    return chart_multiplier


def visualize_cost_benchmark_plotly(file_chosen, df_concat):
    """This function is used for visualizing cost chart for chosen files from
    benchmarking dataset

    Args:
        file_chosen (str): name of file that want to be showed
        df_concat (dataframe): detail benchmarking dataset
    """
    df_tmp = df_concat[df_concat['Filename'].isin(file_chosen)].groupby(
        ['Filename', 'Method', 'Transformation',
         'Size', 'Type']).mean().reset_index()

    chart_cost = px.bar(
        df_tmp,
        x='Method', y='Cost', color='Transformation', facet_col='Filename',
        title='Cost (based on length of nucleotides)', barmode='group',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE, text_auto=True)

    return chart_cost


def visualize_time_benchmark_plotly(file_chosen, df_concat):
    """This function is used for visualizing time charts for benchmarking

    Args:
        file_chosen (str): chosen filename will be used for filtering which
        data will be shown
        df_concat (dataframe): concanated detail precalculated data and data
        from uploaded file
    """
    df_tmp = df_concat[df_concat['Filename'].isin(file_chosen)]

    chart_time = px.box(
        df_tmp, x='Method', y='Time', color='Transformation',
        title='Process Time (in seconds)', facet_col='Filename',
        color_discrete_sequence=_DISCRETE_COLOR_PALLETE)  # ",.0f"

    return chart_time
