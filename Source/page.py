import os
from pathlib import Path
import pandas as pd
import time
import shutil
import streamlit as st
import string
# import import_ipynb
# import data_set_creation as dsc
import json
import requests
# from Bio import SeqIO
from time import sleep
import numpy as np
import bitarray as ba
import bits2DNA as sim_dna
import DNA2Bits as sim_dec_dna
import goldman as gold_dna
import altair as alt
# import testreedsolomon as rs
import xor_code_python as xor
import subprocess as sp

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
data_original = []
for file_name in os.listdir(path_original_data):
    data_original.append(os.path.splitext(file_name)[0])


path_uploaded_list = \
    [path_uploaded_txt, path_uploaded_jpg, path_uploaded_wav, path_encoded_data, path_decoded_data,
        path_encoded_dna, path_decoded_dna, path_uploaded_decoded]


url = 'https://mesa.mosla.de/api/all'
header = {'content-type': 'application/json;charset=UTF-8'}
with open("mesa.json") as json_file:  # You can generate this file under simulate -> Download current config
    config_api = json.load(json_file)

df_metrics = pd.read_excel('synthesis_cost.xlsx')


# Removing old uploaded data
def remove_cached_data():

    SAVE_TIME = 3600  # Time is given in seconds, 5400s = 1.5h, 3600 = 1h
    time_limit = time.time() - SAVE_TIME

    # Traversing every cache directory and deleting everything from it
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

    return None


# Upload function general
def upload_file(key_suffix, cache_folder_path):
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
        file_details = {"filename": imported_file.name, "filetype": imported_file.type, "filesize": imported_file.size}
        st.write(file_details)
        # st.write(save_path)

    return save_path_os, uploaded_filename


def upload_txt():

    key_suffix = 'txt'
    cache_folder_path = path_uploaded_txt

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    output = upload_file(key_suffix, cache_folder_path)
    save_path = output[0]
    file_uploaded_name = output[1]

    return save_path, file_uploaded_name


def upload_jpg():

    key_suffix = 'jpg'
    cache_folder_path = path_uploaded_jpg

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    output = upload_file(key_suffix, cache_folder_path)
    save_path = output[0]
    file_uploaded_name = output[1]

    return save_path, file_uploaded_name


def upload_wav():

    key_suffix = 'wav'
    cache_folder_path = path_uploaded_wav

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    output = upload_file(key_suffix, cache_folder_path)
    save_path = output[0]
    file_uploaded_name = output[1]

    return save_path, file_uploaded_name


# Running API
def run_requests(i, res_all, entry_list, c, payload, header, url):
    start_time = time.time()
    try:
        for j in range(i, len(entry_list)):
            # payload['sequence'] = entry_list[i][0].decode()
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
    entry_list = encoded_dna
    payload = config_api
    payload['asHTML'] = False
    payload["key"] = "9z5NOwZE5QEmU2h4-sAPIx7VhlGOxoEroK5Li2CjyaI"
    payload["err_simulation_order"]["Storage/PCR"][0]["cycles"] = storage_length
    c = 0
    res_all = list()
    i = 0
    time_used = run_requests(i, res_all, entry_list, c, payload, header, url)
    print(time_used)

    for ent in res_all:
        result = ent.json()

    for key, value in result.items():
        modified_sequence = result[key]["res"]["modified_sequence"]
    return modified_sequence


def cost_encoding(max_nt, oligos):
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
def encoding(em, binary, file_basename, save_path):
    numblocks = 0
    if em == 'Simple Code':
        generated_seq = sim_dna.encode('', binary)
    elif em == 'Repetition Code':
        generated_seq = gold_dna.encode(binary, '')
    elif em == 'The 2D Code':
        output_path = os.path.join(path_encoded_dna, file_basename + "_2d.txt")
        output = sp.check_output("2D_Code.exe --encode --input=" + save_path + " --output=" + output_path)
        numblocks = output[output.find(b'to')+3:output.find(b'to')+3+output[output.find(b'to')+3:].find(b' ')]
        numblocks = numblocks.decode("utf-8")
        # os.system("2D_Code.exe --encode --input=" + save_path + " --output=" + output_path)
        generated_seq = open(output_path).readlines()
    elif em == 'XOR-Based Code':
        generated_seq = xor.encode('', binary)

    return generated_seq, numblocks


def check_text_equal(path_original_file, path_decoded_file):

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


def compare2ori(save_path, decoded_path, em, binary, decoded_seq):
    if em == 'The 2D Code':
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
def pipeline(em, binary, file_basename, file_type, storage_length, save_path, uploaded_filename):
    start_time = time.time()
    enc_output = encoding(em, binary, file_basename, save_path)
    time_used = time.time() - start_time
    generated_seq = enc_output[0]
    numblocks = enc_output[1]
    len_oligos = len(generated_seq)
    max_nt = 0
    generated_seq_upper = []
    for seq in generated_seq:
        # cost += len(seq.translate({ord(c): None for c in string.whitespace}))
        nt = len(seq.translate({ord(c): None for c in string.whitespace}))
        generated_seq_upper.append(seq.upper())
        if nt > max_nt:
            max_nt = nt
    print('len_oligos = ' + str(len_oligos) + ' max_nt = ' + str(max_nt))
    cost = cost_encoding(max_nt, len_oligos)

    if em == 'Simple Code':
        file_name = file_basename + '_simple.txt'
    elif em == 'Repetition Code':
        file_name = file_basename + '_repetition.txt'
    elif em == 'The 2D Code':
        file_name = file_basename + '_2d.txt'
    elif em == 'XOR-Based Code':
        file_name = file_basename + '_xor.txt'

    file_path = os.path.join(path_encoded_dna, file_name)
    if em != 'The 2D Code':
        with open(file_path, 'w') as f:
            for i in generated_seq_upper:
                f.write(i + '\n')
    size = os.path.getsize(file_path)
    list_encoded = [uploaded_filename, em, 'Encoding', size, cost, time_used, '.'+file_type]

    modified_sequence = []
    i = 0
    if em == 'The 2D Code':
        # input_path = os.path.join(path_encoded_dna, file_name)
        # output_path = os.path.join(path_decoded_dna, file_name)
        # os.system("2D_Code.exe --encode --input=" + input_path + " --output=" + output_path)
        # file_path = output_path
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

    start_time = time.time()
    decoded_path = ''
    if em == 'Simple Code':
        decoded_seq = sim_dec_dna.decode('', modified_sequence)
    elif em == 'Repetition Code':
        decoded_seq = gold_dna.decode(modified_sequence)
    elif em == 'The 2D Code':
        # decoded_seq = rs.decode('', modified_sequence)
        decoded_path = os.path.join(path_uploaded_decoded, file_basename + "_2d." + file_type)
        os.system("2D_Code.exe --decode --numblocks=" + numblocks + " --input=" + file_path + " --output="
                  + decoded_path)
        decoded_seq = ''
    elif em == 'XOR-Based Code':
        decoded_seq = xor.decode('', modified_sequence)

    time_used = time.time() - start_time
    cost = 0
    # for seq in modified_sequence:
    #     cost += len(seq.translate({ord(c): None for c in string.whitespace}))

    if em == 'Simple Code':
        file_name = file_basename + '_simple.npy'
    elif em == 'Repetition Code':
        file_name = file_basename + '_repetition.npy'
    elif em == 'The 2D Code':
        file_name = file_basename + '_2d.npy'
    elif em == 'XOR-Based Code':
        file_name = file_basename + '_xor.npy'

    file_path = os.path.join(path_decoded_data, file_name)
    np.save(file_path, decoded_seq)
    list_decoded = [uploaded_filename, em, 'Decoding', size, cost, time_used, '.'+file_type]

    status = compare2ori(save_path, decoded_path, em, binary, decoded_seq)
    sum_size = list_encoded[3] + list_decoded[3]
    sum_cost = list_encoded[4] + list_decoded[4]
    sum_time_used = list_encoded[5] + list_decoded[5]
    list_summary = [uploaded_filename, em, sum_size, sum_cost, sum_time_used, '.'+file_type,
                    status]
    if uploaded_filename not in data_original:
        data_original.append(uploaded_filename)
    return list_encoded, list_decoded, list_summary


def visualize_uploaded(df_report):
    method = df_report.Method.unique()
    for em in method:
        chart1 = alt.Chart(df_report, width=alt.Step(50)).mark_bar().encode(
            alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
            alt.Y('Size:Q', title='Size (in bytes)'),
            # alt.Column('Method:N', title='Original File Type'),
            alt.Color('Transformation:N'),
            tooltip=['Size:Q', 'Method', 'Transformation']
        ).transform_filter(
            alt.datum.Method == em
        ).properties(title=em+' Size')
        text1 = chart1.mark_text(
            align='center',
            baseline='middle',
            dy=-5
        ).encode(
            alt.Text('Size:Q', format=",.0f")
        )

        chartsize = text1 + chart1

        chart2 = alt.Chart(df_report, width=alt.Step(50)).mark_bar().encode(
            alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
            alt.Y('Time:Q', title='Process Time (in seconds)'),
            # alt.Column('Method:N', title='Original File Type'),
            alt.Color('Transformation:N'),
            tooltip=['Time:Q', 'Method', 'Transformation']
        ).transform_filter(
            alt.datum.Method == em
        ).properties(title=em+' Time')

        text2 = chart2.mark_text(
            align='center',
            baseline='middle',
            dy=-5
        ).encode(
            alt.Text('Time:Q', format=",.5f")
        )

        charttime = text2 + chart2

        chart3 = alt.Chart(df_report, width=alt.Step(50)).mark_bar().mark_bar().encode(
            alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
            alt.Y('Cost:Q', title='Cost (based on length of chars)'),
            # alt.Column('Method:N', title='Original File Type'),
            alt.Color('Transformation:N'),
            tooltip=['Cost:Q', 'Method', 'Transformation']
        ).transform_filter(
            alt.datum.Method == em
        ).properties(title=em+' Cost')

        text3 = chart3.mark_text(
            align='center',
            baseline='middle',
            dy=-5
        ).encode(
            alt.Text('Cost:Q', format=",.0f")
        )

        chartcost = text3 + chart3

        col1, col2, col3 = st.columns(3)

        with col1:
            st.altair_chart(chartsize, use_container_width=True)
        with col2:
            st.altair_chart(charttime, use_container_width=True)
        with col3:
            st.altair_chart(chartcost, use_container_width=True)


def convert_text_data_to_binary(path_original_data):
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
    return df.to_csv().encode('utf-8')


def create_main_upload():

    st.header('File Upload')

    file_type = ['txt', 'jpg', 'wav']

    choose_file_type = st.selectbox('Which type of file do you want to upload:', file_type)

    # st.warning('Your data will be saved for 1 hour on our servers')

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
        OriFileSize = os.path.getsize(encoded_binary_path)
    else:
        encoded_binary_path = ''
    st.write('Your encoded binary: ', encoded_binary_path)

    st.markdown('---')

    st.header('DNA Encoding')
    choose_dna_encoding = st.multiselect(
     'Select your prefered DNA Encoding Methods',
     ["Repetition Code", "Simple Code", "The 2D Code", "XOR-Based Code"])

    st.warning('The length of processing time depends on your chosen methods.')

    storage_length = st.text_input('Choose your length of storage (in hours)')

    df_report = pd.DataFrame(columns=['Filename', 'Method', 'Transformation', 'Size', 'Cost', 'Time', 'Type'])
    df_summary = pd.DataFrame(columns=['Filename', 'Method', 'Size', 'Cost', 'Time', 'Type', 'Similarity'])

    if choose_dna_encoding != [] and encoded_binary_path != '' and storage_length != '':
        binary = np.load(encoded_binary_path)
        file_basename = os.path.basename(encoded_binary_path)
        file_name = os.path.splitext(file_basename)[0]
        for em in choose_dna_encoding:
            output = pipeline(em, binary, file_name, choose_file_type, storage_length, save_path, uploaded_filename)
            list_encoded = output[0]
            list_decoded = output[1]
            list_summary = output[2]
            df_report.loc[len(df_report)] = list_encoded
            df_report.loc[len(df_report)] = list_decoded
            df_summary.loc[len(df_summary)] = list_summary
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
    df_summary1 = df_summary1.rename({'Size': 'Sum_Mean_Size', 'Time': 'Sum_Mean_Time', 'Cost': 'Sum_Mean_Cost'},
                                     axis=1)
    df_measure_sum = pd.read_pickle("data/pre_measure_stat_sum.pkl")
    df_measure = pd.read_pickle("data/pre_measure.pkl")
    df_report1 = df_report
    if save_path != '':
        df_report1['OriFile_Size'] = OriFileSize
        df_summary1['OriFile_Size'] = OriFileSize
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
    df_multipliers = pd.read_pickle("data/encoded_multipliers.pkl")
    st.markdown("<h3 style='text-align: center; color: black;'>File Size </h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.write("")
    with col2:
        chart = alt.Chart(df_multipliers).mark_boxplot(extent='min-max').encode(
            alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
            alt.Y('Multipliers:Q', title='Multipliers')
        ).properties(title='Multipliers ')

        st.altair_chart(chart, use_container_width=True)
    with col3:
        st.write("")

    st.write('---')
    st.markdown("<h3 style='text-align: center; color: black;'>Cost </h3>", unsafe_allow_html=True)
    file_chosen = st.multiselect(
     'Select files that you want to review (This will affect Cost and Time Charts)',
     data_original)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col = [col1, col2, col3, col4, col5, col6, col7, col8, col9]
    i = 0
    for fc in file_chosen:
        chart = alt.Chart(df_concat).mark_bar().encode(
            alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
            alt.Y('mean(Cost):Q', title='Cost (based on length of chars)'),
            alt.Tooltip(['Method', 'Cost'])
        ).transform_filter(
            (alt.datum.Filename == fc) & (alt.datum.Transformation == 'Encoding')
        ).properties(title=fc)

        with col[i]:
            st.altair_chart(chart, use_container_width=True)
        i += 1

    st.write('---')
    st.markdown("<h3 style='text-align: center; color: black;'>Time</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    col7, col8, col9 = st.columns(3)
    col = [col1, col2, col3, col4, col5, col6, col7, col8, col9]
    i = 0
    for fc in file_chosen:
        chart = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
            alt.X('Method:N', title='Method', axis=alt.Axis(labelAngle=-45)),
            alt.Y('Time:Q', title='Time (in seconds)'),
            alt.Color('Transformation:N')
        ).transform_filter(
            (alt.datum.Filename == fc)
        ).properties(title=fc)

        with col[i]:
            st.altair_chart(chart, use_container_width=True)
        i += 1
