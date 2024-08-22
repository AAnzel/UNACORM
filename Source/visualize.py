import altair as alt


def visualize_uploaded(df_report):
    """This function is used for visualizing the results (time, cost, size)
    for uploaded file

    Args:
        df_report (dataframe): dataframe of detail results of uploaded file
    """
    chart1 = alt.Chart(df_report, width=alt.Step(50)).mark_bar().encode(
        alt.X('Transformation:N', axis=alt.Axis(labels=False, title='')),
        alt.Y('Size:Q', title='Size (in bytes)'),
        alt.Color('Transformation:N'),
        tooltip=['Size:Q', 'Method', 'Transformation']
    ).properties(title='Size')
    text1 = chart1.mark_text(
        align='center',
        baseline='middle',
        dy=-5
    ).encode(
        alt.Text('Size:Q', format=",.0f")
    )
    chartsize = alt.layer(chart1, text1, data=df_report).facet(
        column='Method:N'
    ).configure_axis(
        domainWidth=0.8
    ).configure_view(
        stroke='transparent'
    )

    chart2 = alt.Chart(df_report, width=alt.Step(50)).mark_bar().encode(
        alt.X('Transformation:N', axis=alt.Axis(labels=False, title='')),
        alt.Y('Time:Q', title='Process Time (in seconds)'),
        alt.Color('Transformation:N'),
        tooltip=['Time:Q', 'Method', 'Transformation']
    ).properties(title='Time')
    text2 = chart2.mark_text(
        align='center',
        baseline='middle',
        dy=-5
    ).encode(
        alt.Text('Time:Q', format=",.5f")
    )

    charttime = alt.layer(chart2, text2, data=df_report).facet(
        column='Method:N'
    ).configure_axis(
        domainWidth=0.8
    ).configure_view(
        stroke='transparent'
    )

    chart3 = alt.Chart(
        df_report, width=alt.Step(50)).mark_bar().mark_bar().encode(
        alt.X('Transformation:N', axis=alt.Axis(labels=False, title='')),
        alt.Y('Cost:Q', title='Cost (based on length of chars)'),
        alt.Color('Transformation:N'),
        tooltip=['Cost:Q', 'Method', 'Transformation']
    ).properties(title='Cost')

    text3 = chart3.mark_text(
        align='center',
        baseline='middle',
        dy=-5
    ).encode(
        alt.Text('Cost:Q', format=",.0f")
    )

    chartcost = alt.layer(chart3, text3, data=df_report).facet(
        column='Method:N'
    ).configure_axis(
        domainWidth=0.8
    ).configure_view(
        stroke='transparent'
    )

    return chartsize, charttime, chartcost


def visualize_size_benchmark(df_measure_sum_concat):
    """This function is used for visualizing the size multipliers from the
    benchmarking dataset

    Args:
        df_measure_sum_concat (dataframe): summary dataframe from concanated
        precalculated data with result of uploaded
        file (benchmarking dataset)
    """
    # number of unique encoding methods in dataframe
    chart = alt.Chart(df_measure_sum_concat).transform_density(
        'Encoding_Multipliers',
        as_=['Multipliers', 'density'],
        extent=[0, 35],
        groupby=['Method']
    ).mark_area(orient='horizontal').encode(
        y='Multipliers:Q',
        color='Method:N',
        x=alt.X(
            'density:Q',
            stack='center',
            impute=None,
            title=None,
            axis=alt.Axis(labels=False, values=[0], grid=False, ticks=True),
        ),
        column=alt.Column(
            'Method:N',
            header=alt.Header(
                titleOrient='bottom',
                labelOrient='bottom',
                labelPadding=0,
            ),
        )
    ).properties(
        title='Multipliers'
    ).configure_facet(
        spacing=0
    ).configure_view(
        stroke=None
    )

    return chart


def visualize_cost_benchmark(file_chosen, df_concat):
    """This function is used for visualizing cost chart for chosen files from
    benchmarking dataset

    Args:
        file_chosen (str): name of file that want to be showed
        df_concat (dataframe): detail benchmarking dataset
    """

    chart = alt.Chart(df_concat).mark_bar().encode(
        alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
        alt.Y('mean(Cost):Q', title='Cost'),
        alt.Tooltip(['Method', 'Cost'])
    ).transform_filter(
        (alt.datum.Filename == file_chosen) & (alt.datum.Transformation ==
                                               'Encoding')
    ).properties(title=file_chosen)

    text = chart.mark_text(
        align='center',
        baseline='middle',
        dy=-5
    ).encode(
        alt.Text('mean(Cost):Q', format=",.0f")
    )

    chart = alt.layer(chart, text, data=df_concat).configure_axis(
        domainWidth=0.8
    ).configure_view(
        stroke='transparent'
    )

    return chart


def visualize_time_benchmark(file_chosen, df_concat, flag_filename_uploaded):
    """This function is used for visualizing time charts for benchmarking

    Args:
        file_chosen (str): chosen filename will be used for filtering which
        data will be shown
        df_concat (dataframe): concanated detail precalculated data and data
        from uploaded file
        flag_filename_uploaded (bool): boolean that checks if the name of the
        uploaded file is different than the chosen file to differentiate the
        type of chart
    """

    if flag_filename_uploaded:
        chart = alt.Chart(df_concat).mark_circle(size=60).encode(
            alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
            alt.Y('Time:Q', title='Time (in seconds)'),
            alt.Color('Transformation:N'),
            tooltip=['Method', 'Filename', 'Time', 'Transformation']
        ).transform_filter(
            (alt.datum.Filename == file_chosen)
        ).properties(title=file_chosen)
    else:
        chart = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
            alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
            alt.Y('Time:Q', title='Time (in seconds)'),
            alt.Color('Transformation:N')
        ).transform_filter(
            (alt.datum.Filename == file_chosen)
        ).properties(title=file_chosen)

    return chart
