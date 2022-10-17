import struct;
import random;
import numpy
from bits2DNA import Max_Length, encode;

L = 19
N = 12
t = {
    "0": "a",
    "1": "G",
    "a": "c",
    "G": "T",
    "c": "a",
    "T": "G",
}
u1 = ""
u2 = ""
u3 = "" 
f="CTACACGACGCTCTTCCGATCT"
r="AGATCGGAAGAGCGGTTCAGCA"
n=0

#converts DNA strings to int
def bp2int(param):
    value = 0
    for i in range(len(param)):
        char = param[i]
        if char == "G" or char == "T":
            value |= 1 << i
    return value
#converts DNA strings to byte
def bp2byt(param):
    value = 0
    for i in range(len(param)):
        char = param[i]
        if char == "G" or char == "T":
            value |= 1 << len(param) -i-1
            # value |= 1 << i
    return value
#converts DNA strings to boolean 
def bp2bool(byte, result_array):
    for k in range(len(byte)-1, -1, -1):
        char = byte[k]
        if char == "G" or char == "T":
            result_array.append(True)
        else:
            result_array.append(False)

def get_address(oligo):
    data1 = oligo[len(f): -len(r)]
    address = data1[0:L-1]
    return bp2int(address)

def verify_segments_order(input_list):
    input_list.sort(key = get_address)
    for i in range(len(input_list)):
        if get_address(input_list[i]) != i:
            print('oligo at position')


def decode(string_file_name, input_list):
    result_array = []
    for data in input_list:
        if data.startswith(f) and data.endswith(r):
            data1 = data[len(f): -len(r)]
            #address = data1[0:L-1]
            bytes = data1[L:]
            for n in range(0,96,8):
                chunk = bytes[n : n+8]
                # Convert all characters in the data chunk to bool values
                bp2bool(chunk, result_array)
        else:
            print('Malformed data found', data[:60])
    numpy.save("decode.npy", result_array)
    
def compare_input_with_output(input, output):
    input_array = numpy.load(input)
    output_array = numpy.load(output) 
    print(len(input_array), len(output_array))
    minl = min(len(input_array), Max_Length - 1)
    l = numpy.array_equal(input_array[:minl], output_array[:minl])
    print(input_array[16:24], output_array[16:24], l)

output = encode('', "The_Picture_of_Dorian_Gray.npy")    
decode('', output)
compare_input_with_output("The_Picture_of_Dorian_Gray.npy", "decode.npy")