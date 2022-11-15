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
import testreedsolomon as rs
import xor_code_python as xor

path_uploaded = os.path.join('..', 'Data', 'uploaded')
path_uploaded_txt = os.path.join(path_uploaded, 'txt')
path_uploaded_jpg = os.path.join(path_uploaded, 'jpg')
path_uploaded_wav = os.path.join(path_uploaded, 'wav')
path_encoded_data = os.path.join('..', 'Data', 'Encoded')
path_decoded_data = os.path.join('..', 'Data', 'Decoded')
path_encoded_dna = os.path.join('..', 'Data', 'Encoded', 'DNA')
path_decoded_dna = os.path.join('..', 'Data', 'Decoded', 'DNA')

path_uploaded_dict = {
    'txt': path_uploaded_txt,
    'jpg': path_uploaded_jpg,
    'wav': path_uploaded_wav
}

url = 'https://mesa.mosla.de/api/all'
header = {'content-type': 'application/json;charset=UTF-8'}
with open("mesa.json") as json_file:  # You can generate this file under simulate -> Download current config
    config_api = json.load(json_file)


def remove_cached_data():

    SAVE_TIME = 3600  # Time is given in seconds, 5400s = 1.5h, 3600 = 1h
    time_limit = time.time() - SAVE_TIME

    # Traversing every cache directory and deleting everything from it
    for subdir in os.listdir(path_uploaded):
        subdir_path = os.path.join(path_uploaded, subdir)
        for file_name in os.listdir(subdir_path):
            if 'gitkeep' in file_name:
                continue
            else:
                file_path = os.path.join(subdir_path, file_name)

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

                    print('Successfully removed everything from ' + subdir +
                          ' data set')

                else:
                    pass

    return None


def upload_file(key_suffix, cache_folder_path):
    save_path_os = ''
    imported_file = st.file_uploader(
        label='Upload your file', type=key_suffix, accept_multiple_files=False,
        key='Upload_file_' + key_suffix)

    if imported_file is not None:
        save_path = Path(cache_folder_path, imported_file.name)
        save_path_os = os.path.join(cache_folder_path, imported_file.name)
        with open(save_path, mode='wb') as w:
            w.write(imported_file.getvalue())

        if save_path.exists():
            st.success('Your file successfully uploaded!')
        st.write(type(imported_file))
        file_details = {"filename": imported_file.name, "filetype": imported_file.type, "filesize": imported_file.size}
        st.write(file_details)
        # st.write(save_path)

    return save_path_os


def upload_txt():

    key_suffix = 'txt'
    cache_folder_path = path_uploaded_txt

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    save_path = upload_file(key_suffix, cache_folder_path)

    return save_path


def upload_jpg():

    key_suffix = 'jpg'
    cache_folder_path = path_uploaded_jpg

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    save_path = upload_file(key_suffix, cache_folder_path)

    return save_path


def upload_wav():

    key_suffix = 'wav'
    cache_folder_path = path_uploaded_wav

    st.header('Choose your ' + key_suffix + ' data')
    st.markdown('')

    save_path = upload_file(key_suffix, cache_folder_path)

    return save_path


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


@st.cache(allow_output_mutation=True)
def dna_encoding(encoding_method, bit_path, file_type, storage_length):
    df_report = pd.DataFrame(columns=['Filename', 'Method', 'Transformation', 'Size', 'Cost', 'Time', 'Type'])
    for em in encoding_method:
        if em == 'Simple Code':
            binary = np.load(bit_path)
            start_time = time.time()
            generated_seq = sim_dna.encode('', binary)
            time_used = time.time() - start_time
            cost = 0
            for seq in generated_seq:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_basename = os.path.basename(bit_path)
            file_name = os.path.splitext(file_basename)[0] + '_simple.txt'
            file_path = os.path.join(path_encoded_dna, file_name)
            with open(file_path, 'w') as f:
                for i in generated_seq:
                    f.write(i)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Encoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list

            modified_sequence = []
            i = 0
            while i < len(generated_seq):
                seq = [str(generated_seq[i])]
                result = api_call(seq, storage_length)
                modified_sequence.append(result)
                i += 1

            start_time = time.time()
            decoded_seq = sim_dec_dna.decode('', modified_sequence)
            time_used = time.time() - start_time
            cost = 0
            for seq in modified_sequence:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_name = os.path.splitext(file_basename)[0] + '_simple.npy'
            file_path = os.path.join(path_decoded_dna, file_name)
            np.save(file_path, decoded_seq)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Decoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list
        elif em == 'Repetition Code':
            binary = np.load(bit_path)
            start_time = time.time()
            generated_seq = gold_dna.encode(binary, '')
            time_used = time.time() - start_time
            cost = 0
            for seq in generated_seq:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_basename = os.path.basename(bit_path)
            file_name = os.path.splitext(file_basename)[0] + '_repetition.txt'
            file_path = os.path.join(path_encoded_dna, file_name)
            with open(file_path, 'w') as f:
                for i in generated_seq:
                    f.write(i)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Encoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list

            modified_sequence = []
            i = 0
            while i < len(generated_seq):
                seq = [str(generated_seq[i])]
                result = api_call(seq, storage_length)
                modified_sequence.append(result)
                i += 1

            start_time = time.time()
            decoded_seq = gold_dna.decode(modified_sequence)
            time_used = time.time() - start_time
            cost = 0
            for seq in modified_sequence:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_name = os.path.splitext(file_basename)[0] + '_repetition.npy'
            file_path = os.path.join(path_decoded_dna, file_name)
            np.save(file_path, decoded_seq)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Decoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list
        elif em == 'The 2D Code':
            binary = np.load(bit_path)
            start_time = time.time()
            generated_seq = rs.encode('', binary)
            time_used = time.time() - start_time
            cost = 0
            for seq in generated_seq:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_basename = os.path.basename(bit_path)
            file_name = os.path.splitext(file_basename)[0] + '_2d'
            file_path = os.path.join(path_encoded_dna, file_name)
            with open(file_path, 'w') as f:
                for i in generated_seq:
                    f.write(i)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Encoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list

            modified_sequence = []
            i = 0
            while i < len(generated_seq):
                seq = [str(generated_seq[i])]
                result = api_call(seq, storage_length)
                modified_sequence.append(result)
                i += 1

            start_time = time.time()
            decoded_seq = rs.decode('', modified_sequence)
            time_used = time.time() - start_time
            cost = 0
            for seq in modified_sequence:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_name = os.path.splitext(file_basename)[0] + '_2d.npy'
            file_path = os.path.join(path_decoded_dna, file_name)
            np.save(file_path, decoded_seq)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Decoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list
        elif em == 'XOR-Based Code':
            binary = np.load(bit_path)
            start_time = time.time()
            generated_seq = xor.encode('', binary)
            time_used = time.time() - start_time
            cost = 0
            for seq in generated_seq:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_basename = os.path.basename(bit_path)
            file_name = os.path.splitext(file_basename)[0] + '_xor'
            file_path = os.path.join(path_encoded_dna, file_name)
            with open(file_path, 'w') as f:
                for i in generated_seq:
                    f.write(i)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Encoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list

            modified_sequence = []
            i = 0
            while i < len(generated_seq):
                seq = [str(generated_seq[i])]
                result = api_call(seq, storage_length)
                modified_sequence.append(result)
                i += 1

            start_time = time.time()
            decoded_seq = xor.decode('', modified_sequence)
            time_used = time.time() - start_time
            cost = 0
            for seq in modified_sequence:
                cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            file_name = os.path.splitext(file_basename)[0] + '_xor.npy'
            file_path = os.path.join(path_decoded_dna, file_name)
            np.save(file_path, decoded_seq)
            size = os.path.getsize(file_path)
            list = [os.path.splitext(file_basename)[0], em, 'Decoding', size, cost, time_used, '.'+file_type]
            df_report.loc[len(df_report)] = list
        else:
            pass

    df_summary = df_report.groupby(['Filename', 'Method', 'Type'], as_index=False).agg(
            Size=('Size', sum),
            Cost=('Cost', sum),
            Time=('Time', sum)
    )

    return df_report, df_summary


def visualize_uploaded(df_report, df_summary):
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

        chart = alt.hconcat(chartsize, charttime, chartcost)

        st.altair_chart(chart, use_container_width=True)

    return chart


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
        save_path = upload_txt()
    elif choose_file_type == 'jpg':
        save_path = upload_jpg()
    elif choose_file_type == 'wav':
        save_path = upload_wav()

    st.write('Your uploaded path data: ', save_path)

    st.markdown('---')

    if save_path != '':
        encoded_binary_path = convert_text_data_to_binary(save_path)
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

    if choose_dna_encoding != [] and encoded_binary_path != '' and storage_length != '':
        result = dna_encoding(choose_dna_encoding, encoded_binary_path, choose_file_type, storage_length)
        df_summary = result[1]
        df_report = result[0]
        st.write('Summary Report')
        st.dataframe(df_summary)

        with st.expander("Expand Detail"):
            st.write('Detail Table')
            st.dataframe(df_report)
        visualize_uploaded(df_report, df_summary)

    elif choose_dna_encoding != [] and encoded_binary_path == '':
        st.error('Choose your file and length of storage first!')
    else:
        pass

    st.write('---')
    st.header('Benchmark')
    df_measure = pd.read_pickle("data/pre_measure.pkl")
    df_concat = pd.concat([df_report, df_measure], ignore_index=True)
    st.dataframe(df_concat)

    chart1 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Size:Q', title='Size (in bytes)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'Simple Code'
    ).properties(title='File Size with Simple Code')

    chart2 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Size:Q', title='Size (in bytes)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'Repetition Code'
    ).properties(title='File Size with Repetition Code')

    chart3 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Size:Q', title='Size (in bytes)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'XOR-Based Code'
    ).properties(title='File Size with XOR-Based Code')

    chart_size = alt.hconcat(chart1, chart2, chart3)

    chart4 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Cost:Q', title='Cost (based on length of chars)'),
        alt.Color('Transformation:N'),
    ).transform_filter(
        alt.datum.Method == 'Simple Code'
    ).properties(title='Cost with Simple Code')

    chart5 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Cost:Q', title='Cost (based on length of chars)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'Repetition Code'
    ).properties(title='Cost with Repetition Code')

    chart6 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Cost:Q', title='Cost (based on length of chars)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'XOR-Based Code'
    ).properties(title='Cost with XOR-Based Code')

    chart_cost = alt.hconcat(chart4, chart5, chart6)

    chart7 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Time:Q', title='Time (in seconds)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'Simple Code'
    ).properties(title='Time with Simple Code')

    chart8 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Time:Q', title='Time (in seconds)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'Repetition Code'
    ).properties(title='Time with Repetition Code')

    chart9 = alt.Chart(df_concat).mark_boxplot(extent='min-max').encode(
        alt.X('Transformation:N', title='', axis=alt.Axis(labelAngle=-45)),
        alt.Y('Time:Q', title='Time (in seconds)'),
        alt.Color('Transformation:N')
    ).transform_filter(
        alt.datum.Method == 'XOR-Based Code'
    ).properties(title='Time with XOR-Based Code')

    chart_time = alt.hconcat(chart7, chart8, chart9)

    chart = alt.vconcat(chart_size, chart_cost, chart_time)

    st.altair_chart(chart, use_container_width=True)
