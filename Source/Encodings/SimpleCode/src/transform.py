import struct;
import random;
import numpy;

L = 19 # 2^19 = 524,288 = max number of oligos L=00010011
N = 12 # Length of segment in bytes (not including segment number)
t = {
    "0": "a", # lowercase a,c = zero bit.
    "1": "G",
    "a": "c",
    "G": "T",
    "c": "a",
    "T": "G",
}
# Initialize; keep homopolymer runs < 4
u1 = ""
u2 = ""
u3 = "" 
f="CTACACGACGCTCTTCCGATCT" # forward 'universal' sequencing & amplification
r="AGATCGGAAGAGCGGTTCAGCA" # reverse 22-mer primer
n=0
Max_Length = (2**N)*L*8
#converts the adress of a block of information into pb
def int2bp(param):
    global u1
    global u2
    global u3
    b = '{0:032b}'.format(param)
    p = ""
    for i in range(31, 32-L-1, -1):
        x =  b[i]
        u = t[x]
        if random.randint(0,1):   
            u = t[u]
        if u == u1 and u == u2 and u == u3:
            u = t[u]
        u1 = u2 
        u2 = u3 
        u3 = u # Shift previous base string
        p = p+u
    return p

def byt2bp(param): # convert rightmost 8 bits (MSB first byte) to 8 bp
    global u1
    global u2
    global u3
    b = '{0:032b}'.format(param)
    p = ""
    for i in range(24, 32, 1):
        x = b[i]
        u = t[x]
        if random.randint(0,1):
            u = t[u]
        if u == u1 and u == u2 and u == u3:
            u = t[u]
        u1 = u2 
        u2 = u3 
        u3 = u # Shift previous base string
        p = p+u
    return p

def bits2byte(param):
    value = 0
    for i in range(len(param)):
        if param[i]:
            value |= 1 << i
    # print(value)
    return value


def encode(string_file_name, numpy_boolean_array):
    output_text = []
    output_string = f+int2bp(0)
    n = 0
    if (len(numpy_boolean_array) > Max_Length):
        print('the input data exceeds the maximum length the algorithm can encode')
        print('will truncate to the maximum length in order to continue with the encoding')
        numpy_boolean_array = numpy_boolean_array[0: Max_Length-1]
    for i in range(0, len(numpy_boolean_array), 8):
        chunk = numpy_boolean_array[i:i+8]
        bytedata = bits2byte(chunk)
        output_string += byt2bp(bytedata)
        n+=1
        if n % N == 0:
            #we put this in a file, the address
            output_string += r
            output_text.append(output_string)
            output_string = f+int2bp(n//N)
            #print(n//N)
    for k in range(n%N, N):
        output_string += byt2bp(random.randint(0,255))
        # pad last data line to keep all oligos same size.
    output_string += r
    output_text.append(output_string)
    return output_text
       
def testbit2byte(string_file_name):
    inarray = numpy.load(string_file_name)
    firstbyte = []
    firstbyte = inarray[8:16]
    print(firstbyte)
    result = bits2byte(firstbyte)
    print(result)
    print(byt2bp(result))

#encode('', "Ulysses.npy")
#testbit2byte("Ulysses.npy")
# print(len(int2bp(5)))

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
    return result_array
    
def compare_input_with_output(input, output):
    input_array = numpy.load(input)
    output_array = numpy.load(output) 
    print(len(input_array), len(output_array))
    minl = min(len(input_array), Max_Length - 1)
    l = numpy.array_equal(input_array[:minl], output_array[:minl])
    print(input_array[16:24], output_array[16:24], l)

# output = encode('', "The_Picture_of_Dorian_Gray.npy")    
# decode('', output)
# compare_input_with_output("The_Picture_of_Dorian_Gray.npy", "decode.npy")
