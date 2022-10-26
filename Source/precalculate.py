import os
import time
import pandas as pd
import numpy as np
import bits2DNA as sim_dna
import DNA2Bits as sim_dec_dna
import goldman as gold_dna
import string
import xor_code_python as xor
# import testreedsolomon as rs

path_original_data = os.path.join('..', 'Data', 'Original')
path_encoded_data = os.path.join('..', 'Data', 'Encoded')
path_decoded_data = os.path.join('..', 'Data', 'Decoded')
path_encoded_dna = os.path.join('..', 'Data', 'Encoded_DNA')
path_decoded_dna = os.path.join('..', 'Data', 'Decoded_DNA')

encoding_method = ["Repetition Code", "Simple Code", "The 2D Code", "XOR-Based Code"]

df_report = pd.DataFrame(columns=['Filename', 'Method', 'Transformation', 'Size', 'Cost', 'Time',
                                  'Type'])

# list = ['Test', 'Simple Code', 'Decoding', 1, 1, 1, '.txt']
# df_report.loc[len(df_report)] = list


def run_precalculate():
    for list_file in os.listdir(path_original_data):
        string_file_no_extension = os.path.splitext(list_file)[0]
        file_extension = os.path.splitext(list_file)[1]
        string_file = string_file_no_extension+'.npy'
        bit_path = os.path.join(path_encoded_data, string_file)
        for em in encoding_method:
            if em == 'Simple Code':
                start_time = time.time()
                generated_seq = sim_dna.encode('', bit_path)
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
                list = [string_file_no_extension, em, 'Encoding', size, cost, time_used, file_extension]
                df_report.loc[len(df_report)] = list

                start_time = time.time()
                decoded_seq = sim_dec_dna.decode('', generated_seq)
                time_used = time.time() - start_time
                cost = 0
                for seq in decoded_seq:
                    cost += 1
                file_name = os.path.splitext(file_basename)[0] + '_simple.npy'
                file_path = os.path.join(path_decoded_dna, file_name)
                np.save(file_path, decoded_seq)
                size = os.path.getsize(file_path)
                list = [string_file_no_extension, em, 'Decoding', size, cost, time_used, file_extension]
                df_report.loc[len(df_report)] = list
            elif em == 'Repetition Code':
                start_time = time.time()
                binary = np.load(bit_path)
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
                list = [string_file_no_extension, em, 'Encoding', size, cost, time_used, file_extension]
                df_report.loc[len(df_report)] = list

                start_time = time.time()
                decoded_seq = sim_dec_dna.decode('', generated_seq)
                time_used = time.time() - start_time
                cost = 0
                for seq in decoded_seq:
                    cost += 1
                file_name = os.path.splitext(file_basename)[0] + '_repetition.npy'
                file_path = os.path.join(path_decoded_dna, file_name)
                np.save(file_path, decoded_seq)
                size = os.path.getsize(file_path)
                list = [string_file_no_extension, em, 'Decoding', size, cost, time_used, file_extension]
                df_report.loc[len(df_report)] = list
            # elif em == 'The 2D Code':
            #     start_time = time.time()
            #     binary = np.load(bit_path)
            #     generated_seq = rs.encode('', binary)
            #     time_used = time.time() - start_time
            #     for seq in generated_seq:
            #         cost += len(seq.translate({ord(c): None for c in string.whitespace}))
            #     file_basename = os.path.basename(bit_path)
            #     file_name = os.path.splitext(file_basename)[0] + '_2d'
            #     file_path = os.path.join(path_encoded_dna, file_name)
            #     with open(file_path, 'w') as f:
            #         for i in generated_seq:
            #             f.write(i)
            #     size = os.path.getsize(file_path)
            #     list = [string_file_no_extension, em, 'Encoding', size, 1, time_used, file_extension]
            #     df_report.loc[len(df_report)] = list

            #     start_time = time.time()
            #     decoded_seq = rs.decode('', generated_seq)
            #     time_used = time.time() - start_time
            #     cost = 0
            #     for seq in decoded_seq:
            #         cost += 1
            #     file_name = os.path.splitext(file_basename)[0] + '_2d.npy'
            #     file_path = os.path.join(path_decoded_dna, file_name)
            #     np.save(file_path, decoded_seq)
            #     size = os.path.getsize(file_path)
            #     list = [string_file_no_extension, em, 'Decoding', size, 1, time_used, file_extension]
            #     df_report.loc[len(df_report)] = list
            elif em == 'XOR-Based Code':
                start_time = time.time()
                binary = np.load(bit_path)
                generated_seq = xor.encode('', binary)
                time_used = time.time() - start_time
                cost = 0
                for seq in generated_seq:
                    cost += len(seq.translate({ord(c): None for c in string.whitespace}))
                file_basename = os.path.basename(bit_path)
                file_name = os.path.splitext(file_basename)[0] + '_xor.txt'
                file_path = os.path.join(path_encoded_dna, file_name)
                with open(file_path, 'w') as f:
                    for i in generated_seq:
                        f.write(i)
                size = os.path.getsize(file_path)
                list = [string_file_no_extension, em, 'Encoding', size, cost, time_used, file_extension]
                df_report.loc[len(df_report)] = list

                start_time = time.time()
                decoded_seq = xor.decode('', generated_seq)
                time_used = time.time() - start_time
                cost = 0
                for seq in decoded_seq:
                    cost += 1
                file_name = os.path.splitext(file_basename)[0] + '_xor.npy'
                file_path = os.path.join(path_decoded_dna, file_name)
                np.save(file_path, decoded_seq)
                size = os.path.getsize(file_path)
                list = [string_file_no_extension, em, 'Decoding', size, cost, time_used, file_extension]
                df_report.loc[len(df_report)] = list
            else:
                pass


if __name__ == '__main__':
    i = 0
    while i < 10:
        run_precalculate()
        i = i + 1
    df_report.to_pickle('data/pre_measure.pkl')
