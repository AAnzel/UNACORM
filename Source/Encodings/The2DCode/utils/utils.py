import numpy as np


def bools_to_int(bits):
    ''' Transform boolean to integer
        copied from "https://stackoverflow.com/questions/68423946/python-making-and-int-from-8-boolean-byte-values-and-vice-versa"
    '''
    value = 0
    for i, bit in enumerate(bits):
        value |= bit << (len(bits) - i - 1)
    return value


def int_to_bools(value):
    ''' Transform integer to boolean
        copied from "https://stackoverflow.com/questions/68423946/python-making-and-int-from-8-boolean-byte-values-and-vice-versa"
    '''
    bits = [False, False, False, False, False, False, False, False]
    for i in range(8):
        if(value != 0):
            bits[7 - i] = ((value % 2) >= 1)
            value = value / 2
        else:
            break

    return bits


def tobase(nu, base, size):
    ''' A C++ to Python implementation of base numbersystem transformations
        
        Author:     Reinhard Heckel
        Repository: https://github.com/reinhardh/dna_data_storage
    '''
    nn = []
    for x in range(size):
        nn.append(0)
    if(nu == 0):
        return nn

    div = nu
    i = 0
    while(div != 0 and i < size):
        nn[i] = int(div % base)
        div = int(div / base)
        i += 1

    return nn

def frombase(nn, base):
    ''' A C++ to Python implementation of base numbersystem transformations
        
        Author:     Reinhard Heckel
        Repository: https://github.com/reinhardh/dna_data_storage
    '''
    nu = 0
    basepow = 1
    for n in nn:
        nu += (n * basepow)
        basepow *= base

    return nu


def char2pfe(data_char):
    ''' A C++ to Python implementation of base numbersystem transformations
        Characters to galoise value of 47^3
        
        Author:     Reinhard Heckel
        Repository: https://github.com/reinhardh/dna_data_storage
    '''
    output = []

    if((len(data_char) % 2) != 0):
        data_char.append(10)  # append \n

    for i in range(0, len(data_char), 2):
        indec = frombase(data_char[i:i+2], 256)
        tmpvec = tobase(indec, 47, 3)
        output.extend(tmpvec)

    return output


def pfe2char(data_char):
    ''' A C++ to Python implementation of base numbersystem transformations
        Galoise field value of 47^3 to characters 
        
        Author:     Reinhard Heckel
        Repository: https://github.com/reinhardh/dna_data_storage
    '''
    output = []

    if((len(data_char) % 3) != 0):
        return output

    for i in range(0, len(data_char), 3):
        indec = frombase(data_char[i:i+3], 47)
        tmpvec = tobase(indec, 256, 2)
        output.extend(tmpvec)

    return output


def encode_input(string_file_name:str, numpy_boolean_array):
    if isinstance(numpy_boolean_array, np.ndarray):
        return numpy_boolean_array
    elif string_file_name != '':
        try:
            return np.load(string_file_name)
        except Exception as error:
            print('The given file link is compromised or not exsiting!\n'
                  +str(error))
    else:
        print('No file path available or no boolean array available!')
        
        
def decode_input(string_file_name:str, list_of_dna_strings:list):
    if list_of_dna_strings:
        return list_of_dna_strings
    elif string_file_name != '':
        try:
            with open(string_file_name, 'r') as file:
                return file.readlines()
        except Exception as error:
            print('The given file link is compromised or not exsiting!\n'
                  +str(error))   
    else:
        print('No file path available or no boolean array available!')