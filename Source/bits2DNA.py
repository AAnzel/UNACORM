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
print(len(int2bp(5)))
