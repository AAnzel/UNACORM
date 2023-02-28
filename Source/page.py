import os
from pathlib import Path
import pandas as pd
import time
import shutil
import streamlit as st
import string
import json
import requests
from time import sleep
import numpy as np
import bitarray as ba
import altair as alt
import xor_code_python as xor
import subprocess as sp
import importlib

# List Path of Directories
path_uploaded = os.path.join('..', 'Data', 'uploaded')
path_uploaded_txt = os.path.join(path_uploaded, 'txt')
path_uploaded_jpg = os.path.join(path_uploaded, 'jpg')
path_uploaded_wav = os.path.join(path_uploaded, 'wav')
path_uploaded_decoded = os.path.join(path_uploaded, 'decoded')
path_encoded_data = os.path.join('..', 'Data', 'Encoded')
path_decoded_data = os.path.join('..', 'Data', 'Decoded')
path_encoded_dna = os.path.join('..', 'Data', 'Encoded', 'DNA')
path_decoded_dna = os.path.join('..', 'Data', 'Decoded', 'DNA')
path_original_data = os.path.join('..', 'Data', 'Original')
path_encoding_methods = os.path.join('Encodings')

# List of name of files for showing charts in benchmarking
data_original = []
for file_name in os.listdir(path_original_data):
    path = os.path.join(path_original_data, file_name)
    if os.path.isfile(path):
        data_original.append(os.path.splitext(file_name)[0])

# List of directories for uploaded file
path_uploaded_list = \
    [path_uploaded_txt, path_uploaded_jpg, path_uploaded_wav, path_encoded_data, path_decoded_data,
        path_encoded_dna, path_decoded_dna, path_uploaded_decoded]

# Attributes for API calling
url = 'https://mesa.mosla.de/api/all'
header = {'content-type': 'application/json;charset=UTF-8'}
with open("mesa.json") as json_file:  # Config file for API
    config_api = json.load(json_file)

# Based file for calculating synthesis cost
df_metrics = pd.read_excel('synthesis_cost.xlsx')


# Removing old uploaded data
def remove_cached_data():
    """This function is used for deleting old uploaded files by user that was uploaded older than 1 hour ago

    """

    SAVE_TIME = 3600  # 3600 seconds = 1h
    time_limit = time.time() - SAVE_TIME

    # Traversing directories for uploaded files and deleting everything from it
    for dir in path_uploaded_list:
        for file_name in os.listdir(dir):
            path = os.path.join(dir, file_name)
            if 'gitkeep' in file_name or os.path.isdir(path):
                continue
            else:
                file_path = os.path.join(dir, file_name)

                # Check if file is older than 1h, and if yes, delete it
                if os.stat(file_path).st_mtime < time_limit:
                    try:
                        if os.path.isfile(file_path) or\
                                os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except OSError as e:
                        print('Failed to delete ' + file_path + '. Reason: '
                              + e)

                    print('Successfully removed old data from uploaded directory')

                else:
                    pass


# Upload function general
def upload_file(key_suffix, cache_folder_path):
    """This function is used for saving uploaded files

    Args:
        key_suffix (string): data type that was chosen by user
        cache_folder_path (string): name of directory

    Returns:
        save_path_os (str): full path of uploaded file
        uploaded_filename (str): name of uploaded file

    """
    save_path_os = ''
    imported_file = st.file_uploader(
        label='Upload your file', type=key_suffix, accept_multiple_files=False,
        key='Upload_file_' + key_suffix)

    uploaded_filename = ''

    if imported_file is not None:
        time_uploaded = str(time.time())
        uploaded_filename = os.path.splitext(imported_file.name)[0]
        filename = time_uploaded+'_'+imported_file.name
        save_path = Path(cache_folder_path, filename)
        save_path_os = os.path.join(cache_folder_path, filename)
        with open(save_path, mode='wb') as w:
            w.write(imported_file.getvalue())

        if save_path.exists():
            st.success('Your file successfully uploaded!')
        st.write(type(imported_file))
        file_details = {"filename": imported_file.name, "filetype": imported_file.type}
        st.write(file_details)

    return save_path_os, uploaded_filename


def upload_txt():
    """This function is used for uploading txt file

    Returns:
        save_path_os (str): full path of uploaded file
        uploaded_filename (str): name of uploaded file
    """

    key_suffix = 'txt'
    cache_folder_path = path_uploaded_txt

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    output = upload_file(key_suffix, cache_folder_path)
    save_path = output[0]
    file_uploaded_name = output[1]

    return save_path, file_uploaded_name


def upload_jpg():
    """This function is used for uploading jpg file

    Returns:
        save_path_os (str): full path of uploaded file
        uploaded_filename (str): name of uploaded file
    """

    key_suffix = 'jpg'
    cache_folder_path = path_uploaded_jpg

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    output = upload_file(key_suffix, cache_folder_path)
    save_path = output[0]
    file_uploaded_name = output[1]

    return save_path, file_uploaded_name


def upload_wav():
    """This function is used for uploading wav file

    Returns:
        save_path_os (str): full path of uploaded file
        uploaded_filename (str): name of uploaded file
    """

    key_suffix = 'wav'
    cache_folder_path = path_uploaded_wav

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    output = upload_file(key_suffix, cache_folder_path)
    save_path = output[0]
    file_uploaded_name = output[1]

    return save_path, file_uploaded_name


# Running API
def run_requests(res_all, entry_list, c, payload, header, url):
    """This function is used for running the MESA API

    Args:
        res_all (list): container for API result
        entry_list (list): encoded dna sequence
        c (int): initial number for length of dna list
        payload (dict): API config
        header (dict): API header
        url (str): MESA API URL

    Returns:
        time_used (number): length of API run
    """
    start_time = time.time()
    try:
        for j in range(0, len(entry_list)):
            payload['sequence'] = entry_list[j]
            res = requests.post(url, data=json.dumps(payload), headers=header)
            res_all.append(res)
            c += 1
            print(c)

    except:
        print("Max retries, going to sleep for 100 sec.")
        print("j= " + str(j))
        sleep(100)
        run_requests(j, res_all, entry_list, c, payload, header, url)
    time_used = time.time() - start_time

    return time_used


# Setup parameter and call API
def api_call(encoded_dna, storage_length):
    """This function is used for calling MESA API and setup input parameter

    Args:
        encoded_dna (list): encoded DNA sequence
        storage_length (str): length of storage

    Returns:
        modified_sequence (str): modified sequence sequence
    """
    entry_list = encoded_dna
    payload = config_api
    payload['asHTML'] = False
    payload["key"] = "9z5NOwZE5QEmU2h4-sAPIx7VhlGOxoEroK5Li2CjyaI"
    payload["err_simulation_order"]["Storage/PCR"][0]["cycles"] = storage_length
    c = 0
    res_all = list()
    time_used = run_requests(res_all, entry_list, c, payload, header, url)
    print(time_used)

    for ent in res_all:
        result = ent.json()

    for key, value in result.items():
        modified_sequence = result[key]["res"]["modified_sequence"]
    return modified_sequence


def cost_encoding(max_nt, oligos):
    """This function is used for calculating synthesizing cost

    Args:
        max_nt (int): max nucleutide from dna sequences
        oligos (int): number of oligos

    Returns:
        cost_total (number): synthesising cost
    """
    if max_nt <= 120:
        i = 0
    else:
        i = 1

    if oligos >= 2 and oligos <= 100:
        j = 1
    elif oligos >= 101 and oligos <= 500:
        j = 2
    elif oligos >= 501 and oligos <= 1000:
        j = 3
    else:
        j = 4

    cost = df_metrics.iloc[i, j]
    cost_total = cost * oligos

    return cost_total


@st.cache
def encoding(encoding_method, binary, file_basename, save_path):
    """This function is used for encoding the binary

    Args:
        encoding_method (str): chosen encoding method
        binary (array): binary sequence of uploaded file
        file_basename (str): name of file that contains timestamp
        save_path (str): path of original uploaded file

    Returns:
        generated_seq (list): encoded dna list
        numblocks (int): number of blocks from 2D Code that will be used for decoding
    """
    numblocks = 0
    if encoding_method == 'The2DCode':
        output_path = os.path.join(path_encoded_dna, file_basename + '_' + encoding_method + '.txt')
        output = sp.check_output("2D_Code.exe --encode --input=" + save_path + " --output=" + output_path)
        numblocks = output[output.find(b'to')+3:output.find(b'to')+3+output[output.find(b'to')+3:].find(b' ')]
        numblocks = numblocks.decode("utf-8")
        generated_seq = open(output_path).readlines()
    elif encoding_method == 'XORBasedCode':
        generated_seq = xor.encode('', binary)
    else:
        method = importlib.import_module(f'Encodings.{encoding_method}.src.transform')
        generated_seq = method.encode('', binary)

    return generated_seq, numblocks


def check_text_equal(path_original_file, path_decoded_file):
    """This function is used for checking if the original file is equal than generated decoded file

    Args:
        path_original_file (str): path of original uploaded file
        path_decoded_file (str): path of generated decoded file

    Returns:
        status (str): the result of comparison (Same or Different)
    """

    if os.path.isfile(path_original_file):
        with open(path_original_file, 'rb') as fd_original_file,\
                open(path_decoded_file, 'rb') as fd_decoded_file:
            binary_array_original = ba.bitarray()
            binary_array_decoded = ba.bitarray()

            binary_array_original.fromfile(fd_original_file)
            binary_array_decoded.fromfile(fd_decoded_file)

            binary_numpy_original = np.frombuffer(
                binary_array_original.unpack(), dtype=bool)
            binary_numpy_decoded = np.frombuffer(
                binary_array_decoded.unpack(), dtype=bool)

            status = ''
            if np.array_equal(binary_numpy_original, binary_numpy_decoded):
                status = 'Same'
            else:
                status = 'Different'

    return status


def compare2ori(save_path, decoded_path, encoding_method, binary, decoded_seq):
    """This function is used for specifying condition of comparison for different encoding method

    Args:
        save_path (string): path of uploaded file
        decoded_path (strung): path of generated decoded file
        encoding_method (str): chosen encoding method
        binary (array): binary array of uploaded file
        decoded_seq (array): binary array of generated decoded file

    Returns:
        status (str): result of comparison (Same or Different)
    """
    if encoding_method == 'The2DCode':
        status = check_text_equal(save_path, decoded_path)
    else:
        if len(binary) == len(decoded_seq):
            i = 0
            status = 'Same'
            while i < len(binary) and status == 'Same':
                if binary[i] == decoded_seq[i]:
                    status = 'Same'
                else:
                    status = 'Different'
                i += 1
        else:
            status = 'Different'

    return status


@st.cache
def pipeline(encoding_method, binary, file_basename, file_type, storage_length, save_path, uploaded_filename):
    """This function is used for integrating the process for uploaded file

    Args:
        encoding_method (str): chosen encoding method
        binary (array): numpy binary array of uploaded file
        file_basename (str): name of file that contains timestamp
        file_type (str): file extension
        storage_length (int): chosen length of storage in hour
        save_path (str): path of uploaded data
        uploaded_filename (str): uploaded file name without timestamp and extension

    Returns:
        list_encoded [list]: list of result from encoding process including time, cost, and size
        list_decoded [list]: list of result from decoding process including time, cost, and size
        list_summary [list]: list of summary from encoding and decoding process
    """
    start_time = time.time()
    enc_output = encoding(encoding_method, binary, file_basename, save_path)
    time_used = time.time() - start_time  # getting length of encoding process
    generated_seq = enc_output[0]
    numblocks = enc_output[1]
    len_oligos = len(generated_seq)
    max_nt = 0
    generated_seq_upper = []
    # getting maximum nucleotide
    for seq in generated_seq:
        nt = len(seq.translate({ord(c): None for c in string.whitespace}))
        generated_seq_upper.append(seq.upper())
        if nt > max_nt:
            max_nt = nt
    print('len_oligos = ' + str(len_oligos) + ' max_nt = ' + str(max_nt))
    cost = cost_encoding(max_nt, len_oligos)

    file_name = file_basename + '_' + encoding_method + '.txt'

    file_path = os.path.join(path_encoded_dna, file_name)
    if encoding_method != 'The2DCode':
        with open(file_path, 'w') as f:
            for i in generated_seq_upper:
                f.write(i + '\n')
    encoded_size = os.path.getsize(file_path)
    list_encoded = [uploaded_filename, encoding_method, 'Encoding', encoded_size, cost, time_used, '.'+file_type]

    modified_sequence = []
    i = 0
    if encoding_method == 'The2DCode':
        modified_sequence = generated_seq
    else:
        while i < len(generated_seq_upper):
            seq = [str(generated_seq_upper[i])]
            result = api_call(seq, storage_length)
            modified_sequence.append(result)
            i += 1

    file_path = os.path.join(path_decoded_dna, file_name)
    with open(file_path, 'w') as f:
        for i in modified_sequence:
            f.write(i)

    size = os.path.getsize(file_path)

    decoded_path = ''
    start_time = time.time()
    if encoding_method == 'The2DCode':
        decoded_path = os.path.join(path_uploaded_decoded, file_basename + '_' + encoding_method + '.' + file_type)
        os.system("2D_Code.exe --decode --numblocks=" + numblocks + " --input=" + file_path + " --output="
                  + decoded_path)
        decoded_seq = ''
    elif encoding_method == 'XORBasedCode':
        decoded_seq = xor.decode('', modified_sequence)
    else:
        method = importlib.import_module(f'Encodings.{encoding_method}.src.transform')
        decoded_seq = method.decode('', modified_sequence)

    time_used = time.time() - start_time
    cost = 0

    file_name = file_basename + '_' + encoding_method + '.npy'

    file_path = os.path.join(path_decoded_data, file_name)
    np.save(file_path, decoded_seq)
    list_decoded = [uploaded_filename, encoding_method, 'Decoding', size, cost, time_used, '.'+file_type]

    status = compare2ori(save_path, decoded_path, encoding_method, binary, decoded_seq)
    sum_size = list_encoded[3] + list_decoded[3]
    sum_cost = list_encoded[4] + list_decoded[4]
    sum_time_used = list_encoded[5] + list_decoded[5]
    list_summary = [uploaded_filename, encoding_method, sum_size, sum_cost, sum_time_used, '.'+file_type,
                    status, encoded_size]
    if uploaded_filename not in data_original:
        data_original.append(uploaded_filename)
    return list_encoded, list_decoded, list_summary


def visualize_uploaded(df_report):
    """This function is used for visualizing the results (time, cost, size) for uploaded file

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

    chart3 = alt.Chart(df_report, width=alt.Step(50)).mark_bar().mark_bar().encode(
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

    st.altair_chart(chartsize, use_container_width=True)
    st.altair_chart(charttime, use_container_width=True)
    st.altair_chart(chartcost, use_container_width=True)


def convert_text_data_to_binary(path_original_data):
    """This function is used to convert data to binary

    Args:
        path_original_data (str): path of original uploaded file

    Returns:
        bit_encoded_file (str): path of generated binary from uploaded file
    """
    # If we have a file, we convert it into numpy byte file (.npy)
    file_basename = os.path.basename(path_original_data)
    string_file_no_extension = os.path.splitext(file_basename)[0]
    encoded_filename = string_file_no_extension + ".npy"
    if os.path.isfile(path_original_data):
        with open(path_original_data, 'rb') as fd_file:
            binary_array_content = ba.bitarray()
            binary_array_content.fromfile(fd_file)
            binary_numpy_content = np.frombuffer(
                binary_array_content.unpack(), dtype=bool)

            np.save(os.path.join(path_encoded_data, string_file_no_extension), binary_numpy_content, allow_pickle=False)

    bit_encoded_file = os.path.join(path_encoded_data, encoded_filename)

    return bit_encoded_file


@st.cache
def convert_df(df):
    """This function is used to save csv file from dataframe

    Args:
        df (dataframe): dataframe that will be saved into csv

    Returns:
        save file to csv
    """
    return df.to_csv().encode('utf-8')


def visualize_size_benchmark(df_measure_sum_concat):
    """This function is used for visualizing the size multipliers from the benchmarking dataset

    Args:
        df_measure_sum_concat (dataframe): summary dataframe from concanated precalculated data with result of uploaded
        file (benchmarking dataset)
    """
    num_method = df_measure_sum_concat['Method'].nunique()
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

    cols = st.columns(num_method)
    col = cols[0]
    with col:
        st.altair_chart(chart, use_container_width=True)


def visualize_cost_benchmark(file_chosen, df_concat):
    """This function is used for visualizing cost chart for chosen files from benchmarking dataset

    Args:
        file_chosen (str): name of file that want to be showed
        df_concat (dataframe): detail benchmarking dataset
    """
    col1, col2, col3 = st.columns(3)
    i = 0
    for fc in file_chosen:
        col_nr = (i % 3) + 1
        chart = alt.Chart(df_concat).mark_bar().encode(
            alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
            alt.Y('mean(Cost):Q', title='Cost'),
            alt.Tooltip(['Method', 'Cost'])
        ).transform_filter(
            (alt.datum.Filename == fc) & (alt.datum.Transformation == 'Encoding')
        ).properties(title=fc)

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

        if col_nr == 1:
            with col1:
                st.altair_chart(chart, use_container_width=True)
        if col_nr == 2:
            with col2:
                st.altair_chart(chart, use_container_width=True)
        if col_nr == 3:
            with col3:
                st.altair_chart(chart, use_container_width=True)
        i += 1


def visualize_time_benchmark(file_chosen, df_concat, filename_uploaded):
    """This function is used for visualizing time charts for benchmarking

    Args:
        file_chosen (str): chosen filename will be used for filtering which data will be shown
        df_concat (dataframe): concanated detail precalculated data and data from uploaded file
        filename_uploaded (list): name of file that is contained in uploaded file to differentiate the type of chart
    """
    col1, col2, col3 = st.columns(3)
    i = 0
    for fc in file_chosen:
        col_nr = (i % 3) + 1
        if fc == filename_uploaded:
            chart = alt.Chart(df_concat).mark_circle(size=60).encode(
                alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
                alt.Y('Time:Q', title='Time (in seconds)'),
                alt.Color('Transformation:N'),
                tooltip=['Method', 'Filename', 'Time', 'Transformation']
            ).transform_filter(
                (alt.datum.Filename == fc)
            ).properties(title=fc)
        else:
            chart = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
                alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
                alt.Y('Time:Q', title='Time (in seconds)'),
                alt.Color('Transformation:N')
            ).transform_filter(
                (alt.datum.Filename == fc)
            ).properties(title=fc)

        if col_nr == 1:
            with col1:
                st.altair_chart(chart, use_container_width=True)
        if col_nr == 2:
            with col2:
                st.altair_chart(chart, use_container_width=True)
        if col_nr == 3:
            with col3:
                st.altair_chart(chart, use_container_width=True)
        i += 1


def create_main_upload():
    """_summary_
    """

    st.header('File Upload')

    file_type = ['txt', 'jpg', 'wav']

    choose_file_type = st.selectbox('Which type of file do you want to upload:', file_type)

    # Removing previously cached data
    remove_cached_data()

    st.markdown('---')

    save_path = ''
    if choose_file_type == 'txt':
        output = upload_txt()
        save_path = output[0]
        uploaded_filename = output[1]
    elif choose_file_type == 'jpg':
        output = upload_jpg()
        save_path = output[0]
        uploaded_filename = output[1]
    elif choose_file_type == 'wav':
        output = upload_wav()
        save_path = output[0]
        uploaded_filename = output[1]

    st.write('Your uploaded path data: ', save_path)

    st.markdown('---')

    if save_path != '':
        encoded_binary_path = convert_text_data_to_binary(save_path)
        OriFileSize = os.path.getsize(save_path)
    else:
        encoded_binary_path = ''
    st.write('Your encoded binary: ', encoded_binary_path)

    st.markdown('---')

    st.header('DNA Encoding')
    existing_encoding = []
    for encoding_method in os.listdir(path_encoding_methods):
        existing_encoding.append(encoding_method)
    choose_dna_encoding = st.multiselect(
     'Select your prefered DNA Encoding Methods',
     existing_encoding)

    st.warning('The length of processing time depends on your chosen methods.')

    storage_length = st.text_input('Choose your length of storage (in hours)')

    df_report = pd.DataFrame(columns=['Filename', 'Method', 'Transformation', 'Size', 'Cost', 'Time', 'Type'])
    df_summary = pd.DataFrame(columns=['Filename', 'Method', 'Size', 'Cost', 'Time', 'Type', 'Similarity',
                                       'Encoding_Multipliers'])

    if choose_dna_encoding != [] and encoded_binary_path != '' and storage_length != '':
        binary = np.load(encoded_binary_path)
        file_basename = os.path.basename(encoded_binary_path)
        file_name = os.path.splitext(file_basename)[0]
        for encoding_method in choose_dna_encoding:
            try:
                output = pipeline(encoding_method, binary, file_name, choose_file_type, storage_length, save_path,
                                  uploaded_filename)
                list_encoded = output[0]
                list_decoded = output[1]
                list_summary = output[2]
                df_report.loc[len(df_report)] = list_encoded
                df_report.loc[len(df_report)] = list_decoded
                list_summary[7] = list_summary[7]/OriFileSize
                df_summary.loc[len(df_summary)] = list_summary
            except:
                continue
        st.write('Summary Report')
        st.dataframe(df_summary)

        with st.expander("Expand Detail"):
            st.write('Detail Table')
            st.dataframe(df_report)
        visualize_uploaded(df_report)

    elif choose_dna_encoding != [] and encoded_binary_path == '':
        st.error('Choose your file and length of storage first!')
    else:
        pass

    st.write('---')
    st.header('Benchmark')
    df_summary1 = df_summary
    df_summary1 = df_summary1.rename({'Size': 'Sum_Size', 'Time': 'Sum_Mean_Time', 'Cost': 'Sum_Cost'},
                                     axis=1)
    df_measure_sum = pd.read_pickle("data/pre_measure_stat_sum1.pkl")
    df_measure = pd.read_pickle("data/pre_measure1.pkl")
    df_report1 = df_report
    filename_uploaded = df_report1['Filename'].unique()
    if save_path != '':
        df_report1['OriFile_Size'] = OriFileSize
    df_concat = pd.concat([df_report1, df_measure], ignore_index=True)
    df_measure_sum_concat = pd.concat([df_summary1, df_measure_sum], ignore_index=True)
    csv_sum = convert_df(df_measure_sum_concat)
    csv_detail = convert_df(df_concat)
    st.dataframe(df_measure_sum_concat)
    st.download_button(
        label="Download",
        data=csv_sum,
        file_name='summary_data.csv',
        mime='text/csv',
    )
    with st.expander("Expand Detail"):
        st.write('Detail Table')
        st.dataframe(df_concat)
        st.download_button(
            label="Download",
            data=csv_detail,
            file_name='detail_data.csv',
            mime='text/csv',
        )
    st.markdown("<h3 style='text-align: center; color: black;'>File Size </h3>", unsafe_allow_html=True)
    visualize_size_benchmark(df_measure_sum_concat)
    st.write('---')
    st.markdown("<h3 style='text-align: center; color: black;'>Cost </h3>", unsafe_allow_html=True)
    file_chosen = st.multiselect(
     'Select files that you want to review (This will affect Cost and Time Charts)',
     data_original)
    visualize_cost_benchmark(file_chosen, df_concat)
    st.write('---')
    st.markdown("<h3 style='text-align: center; color: black;'>Time</h3>", unsafe_allow_html=True)
    visualize_time_benchmark(file_chosen, df_concat, filename_uploaded)
