# Import libaries
import numpy as np
import random
from .utils import *
from .reedSolomon import *


class api():
    def __init__(self):
        self.string_file_name = ''
        self.numpy_boolean_array = ''
        self.list_of_dna_strings = ''

    # DNA Encoding function
    def encode(self, string_file_name: str, numpy_boolean_array):
        ''' Top level encode function.
            Take a numpy array of booleans and transform them to a list of ASCII
            pairs (two letters of a text file). The ASCII pairs are mapped to three 
            values of the galoise field of size 47. 
            The original message is aranged in blocks of 594*39 elemnts. In an outer
            encoding step Reed-Solomon codes are employed to each block. 
            Each Column are transformed into three nucleotides by utilizing a 
            DNA codon wheel.

        Args:
            string_file_name (string): 
            numpy_Boolean_array (numpy array): 

        Return:
            list_of_dna_strings (list): list of three nucleotides 

        '''
        # Read input
        numpy_boolean_array = utils.encode_input(
            string_file_name, numpy_boolean_array)

        list_of_dna_strings = []

        # Initialize reedSolomon codes
        inner_encoder = generalizedreedsolo.Generalized_Reed_Solomon(field_size=47,
                                                                     message_length=39,
                                                                     payload_length=33,
                                                                     symbol_size=1,
                                                                     p_factor=2)
        irr_poly_47 = [1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                       0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 32]
        outer_encoder = generalizedreedsolo.Generalized_Reed_Solomon(field_size=47,
                                                                     message_length=713,
                                                                     payload_length=594,
                                                                     symbol_size=30,
                                                                     p_factor=7,
                                                                     irr_poly=irr_poly_47)
        reedWorker = parallelReed.parallelReed(inner_encoder, outer_encoder)

        # Transform boolean array list to a list of ASCII pairs
        ascii_pairs, ascii_pairs_pointer = [], 0
        byte = [False, False, False, False, False, False, False, False]
        byte_pointer = 0
        for bit in numpy_boolean_array:
            byte[byte_pointer] = bit
            if(byte_pointer == 7):
                ascii_pairs.append(utils.bools_to_int(byte))
                ascii_pairs_pointer += 1
                byte_pointer = 0
            else:
                byte_pointer += 1
        if(byte_pointer != 0):
            while(byte_pointer < 8):
                byte[byte_pointer] = False
                byte_pointer += 1
            ascii_pairs.append(utils.utils.bools_to_int(byte))

        # Map list of ASCII pairs represented as integers to a galoise field
        # value of 0 to 46
        base_list = utils.char2pfe(ascii_pairs)

        # Create array of the block with length 713*39
        dataList = []
        dataList.append(np.zeros((713, 39), dtype=int))

        block = 0
        x = 119
        y = 2
        for d in base_list:
            if(y < 32):
                y += 1
            elif(x < 712):
                y = 3
                x += 1
            else:
                x = 119
                y = 3
                dataList.append(np.zeros((713, 39), dtype=int))
                block += 1

            (dataList[block])[x][y] = d

        # Encode array
        reedWorker.startRsCode(dataList, 0)

        # Map encoded array to three nucleotides by utilizing the DNA codon wheel
        for block in dataList:
            for x in range(0, 713):
                row = ""
                for y in range(0, 39):
                    row += dnaWheel.dnaWheel().number_to_pair[block[x][y]]
                list_of_dna_strings.append(row)

        return list_of_dna_strings

    # DNA Decoding function
    def decode(self, string_file_name: str, list_of_dna_strings):
        ''' Top level decode function.
            Input sequence is transformed to values of galoise field of size 47.
            First inner incoding, sort sequences by means of index, followed by
            outer-decoding.

        Args:
            string_file_name (string): 
            numpy_Boolean_array (numpy array): 

        Return:
            numpy_boolean_array (numpy array): boolean array of decoded message

        '''
        # Read input
        list_of_dna_strings = utils.decode_input(
            string_file_name, list_of_dna_strings)
        numpy_boolean_array = []

        # Initialize reedSolomon codes
        inner_encoder = generalizedreedsolo.Generalized_Reed_Solomon(field_size=47,
                                                                     message_length=39,
                                                                     payload_length=33,
                                                                     symbol_size=1,
                                                                     p_factor=2)
        irr_poly_47 = [1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
                       0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 32]
        outer_encoder = generalizedreedsolo.Generalized_Reed_Solomon(field_size=47,
                                                                     message_length=713,
                                                                     payload_length=594,
                                                                     symbol_size=30,
                                                                     p_factor=7,
                                                                     irr_poly=irr_poly_47)
        reedWorker = parallelReed.parallelReed(inner_encoder, outer_encoder)

        # Transform list of three nucleotides to array for the blocks
        dataList = []
        block = 0
        for i, row in enumerate(list_of_dna_strings):
            if(i % 713 == 0):
                dataList.append(np.zeros((713, 39), dtype=int))
                if(i > 0):
                    block += 1
            pair = ''
            index = 0
            pos = 0
            for base in row:
                pair += base
                index += 1
                if(index > 2):
                    (dataList[block])[i %
                                      713][pos] = dnaWheel.dnaWheel().pair_to_number[pair]
                    pair = ''
                    index = 0
                    pos += 1

        # Decode array
        reedWorker.startRsCode(dataList, 1)

        # Transform decoded array to a list of galoise field values 47^3
        output = []
        for block in dataList:
            for x in range(119, 713):
                for y in range(3, 33):
                    output.append(block[x][y])

        # Remove 0es we used as padding in the last block
        lastValidNumber = len(output) - 1
        for i in range(lastValidNumber, 0, -3):
            if(output[i] != 0 or output[i-1] != 0 or output[i-2] != 0):
                lastValidNumber = i
                break
        output = output[:(lastValidNumber+1)]

        # Map the galoise field triplets to pairs of ASCII characters
        # 47**3 (List) -> 256**2 (List)
        converted_output = utils.pfe2char(output)

        # Remove '\n' we sometimes add to get an even amount of bytes
        if(converted_output[-1] == 10):
            converted_output = converted_output[:-1]

        # Transform list of ASCII pairs to numpy boolean array
        # 256**2 (List) -> Boolean (Array[n:1])
        numpy_boolean_array = np.empty(
            [int(len(converted_output)*8), ], dtype=bool)
        arr_out_pointer = 0
        for number in converted_output:
            for bool_val in utils.int_to_bools(number):
                numpy_boolean_array[arr_out_pointer] = bool_val
                arr_out_pointer += 1

        return numpy_boolean_array[0:arr_out_pointer]

    # Function Test - DNA Encoding/Decoding with Generalized Reed Solomon Code

    def utility_test(self):
        print('\n'+'Load test file..')
        test_data = np.load('reedSolomonDNA/test/data/La_Jeunesse.npy')
        org_data = np.copy(test_data)
        print('Test file loaded!'+'\n'*2)

        print('Encode test data..')
        encoded_data = self.encode('', test_data)
        print('Test data encoded!'+'\n'*2)

        print('Decode encoded test data..')
        random.shuffle(encoded_data)
        decoded_data = self.decode('', encoded_data)
        dec = np.copy(decoded_data)
        print('Test data decoded!'+'\n'*2)

        print('Error check..')
        print('Length of the original data: (byte) '+str(len(org_data)))
        print('Length of the decoded data: (byte) '+str(len(dec)))
        print('Original data shape: '+str(org_data.shape))
        print('Decoded data shape: '+str(dec.shape))
        print('Boolean Array check: ' +
              str(np.all(np.array(org_data) == np.array(dec))))
