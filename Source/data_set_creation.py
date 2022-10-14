import os
import numpy as np
import bitarray as ba


def dictionary_create_extensions(path_original_data):
    dict_name_extension = dict()
    for string_file in os.listdir(path_original_data):
        string_file_no_extension, string_file_extension = os.path.splitext(
            string_file)
        dict_name_extension[string_file_no_extension] = string_file_extension
    
    return dict_name_extension


def convert_text_data_to_binary(path_original_data, path_encoded_data):
    for string_file in os.listdir(path_original_data):
        
        string_file_no_extension = os.path.splitext(string_file)[0]
        path_original_file = os.path.join(path_original_data, string_file)
        path_encoded_file = os.path.join(path_encoded_data,
                                         string_file_no_extension)
        
        # If we have a file, we convert it into numpy byte file (.npy)
        if os.path.isfile(path_original_file):
            with open(path_original_file, 'rb') as fd_file:
                binary_array_content = ba.bitarray()
                binary_array_content.fromfile(fd_file)
                
                binary_numpy_content = np.frombuffer(
                    binary_array_content.unpack(), dtype=bool)
            
                np.save(os.path.join(
                    path_encoded_data, string_file_no_extension),
                        binary_numpy_content, allow_pickle=False)

    return None


def convert_binary_to_text_data(path_encoded_data, path_decoded_data,
                                dict_file_name_extension):
    for string_file in os.listdir(path_encoded_data):
        
        string_file_no_extension = os.path.splitext(string_file)[0]
        path_encoded_file = os.path.join(path_encoded_data, string_file)
        path_decoded_file = os.path.join(
            path_decoded_data,
            string_file_no_extension +
            dict_file_name_extension[string_file_no_extension])

        # If we have a file, we load it
        if os.path.isfile(path_encoded_file):
            with open(path_encoded_file, 'rb') as fd_file:
                binary_numpy_content = np.load(fd_file)
                binary_array_content = ba.bitarray()  
                binary_array_content.pack(binary_numpy_content.tobytes())
                
            with open(path_decoded_file, 'wb+') as fd_file:
                binary_array_content.tofile(fd_file)

    return None


def check_text_equal(path_original_data, path_decoded_data):
    for string_file in os.listdir(path_original_data):
        
        path_original_file = os.path.join(path_original_data, string_file)
        path_decoded_file = os.path.join(path_decoded_data, string_file)
        
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
                
                if np.array_equal(binary_numpy_original, binary_numpy_decoded):
                    print('{: <40}'.format(string_file) +
                          ': Original and decoded data are EQUAL')
                else:
                    print('{: <40}'.format(string_file) +
                          ': Original and decoded data are NOT EQUAL')

    return None


def perform_encode_decode_check():
    path_root_data = os.path.join('..', 'Data')
    path_original_data = os.path.join(path_root_data, 'Original')
    path_encoded_data = os.path.join(path_root_data, 'Encoded')
    path_decoded_data = os.path.join(path_root_data, 'Decoded')
    
    dict_file_name_extension = dictionary_create_extensions(path_original_data)
    convert_text_data_to_binary(path_original_data, path_encoded_data)
    convert_binary_to_text_data(path_encoded_data, path_decoded_data,
                                dict_file_name_extension)
    check_text_equal(path_original_data, path_decoded_data)
    
    return None
    