"""
This programme largely builds on the work of Allan Costa as it is found at his github repository
(https://github.com/allanino/DNA/blob/master/dna/dna.py)
This programme implements to main methods:
 - encode(binary, file_name): encode an arbitrary binary string with a file name in DNA form as
                            described by Goldman et al. (2013).
 - decode(dnastr): decode an DNA string as it would be produced by encode(binary, file_name) back
                            to its binary representation as it is left to the reader as an "exercise"
                            by Goldman et al. (2013).
"""


# imports

import csv
from random import randint

# Huffman code dictionary
code = {}

# Dictionary with files 2-trits
files_trits = {}


# Note. There will be the problem that if trough mutation/errors/... a nucleotide is followed
# by te same one, this programme will crash. But this is the algorithm the authors describe.


def encode(binary, file_name):
    """ This function encodes binary data [0, 1] to DNA [A, T, C, G] following the algorithm
    described in supplementary material 2 of Goldman et al. (2013).

    :param binary: numpy array of [0, 1]
    :param file_name: string
    :return: string [A, T, C, G]
    """
    # populate the Huffman code dictionary
    read_huff("data/huff3.dict")
    # print("s0 (binary):" + str(len(binary)))
    s1 = S0_to_S1(binary, file_name)
    # print("s1:" + str(len(s1)))
    s4 = S1_to_S4(s1)
    # print("s4:" + str(len(s4)))
    s5 = S4_to_S5(s4)
    # print("s5:" + str(len(s5)))
    F = S5_to_Fi(s5)
    Findex = Fi_to_Findex(F, file_name)
    return Findex


def decode(dnastr):
    """ This function decodes data encoded in DNA [A, T, C, G] back to its binary form [0, 1].
    Note. If the DNA-data is compromised in a way that the a nucleotide is followed by itself,
    it is possible that the programme will crash due to the nature of the implemented algorithm.

    :param dnastr: string [A, T, C, G]
    :return: array [O, 1]
    """
    # populate the Huffman code dictionary
    read_huff("data/huff3.dict")
    # This also sorts the overlapping nucleotide strings w
    # which is essential for real world applications
    Fi = Findex_to_Fi(dnastr)
    # s5 = Fi_to_S5(Fi)
    # use Fi_to_S5(Fi), if you do not want to use the majority vote
    s5 = majority_vote(Fi)
    # print("s5:" + str(len(s5)))
    s4 = S5_to_S4(s5)
    # print("s4:" + str(len(s4)))
    s0 = S4_to_S0(s4)
    # print(s0)

    s00 = []
    for bit in s0:
        if bit == "0":
            s00.append(False)
        else:
            s00.append(True)

    return s00


# functions used to encode binary data into dna (A, C, T, G) / called by encode(binary, file_name)


def S0_to_S1(binary, file_name):
    """ convert binary to trinary using the revised huffman code published by Goldman et al. (2013).

    :param binary: numpy array of [0, 1]
    :param file_name: string
    :return: array of [0, 1, 2]
    """
    # Update 2-trits file dictionary (for later use: if more than one file)
    trit = base10_to_base3(len(files_trits))
    trit = '0' * (2 - len(trit)) + trit
    files_trits[file_name] = trit
    # Concatenate byte by byte to s1 (after Huffman codification)
    # This part is altered by me to suite the specifications of the project
    s1 = ""
    i = 0
    while i + 8 <= len(binary):  # ... because 8 bits are one byte ;-)
        byte_str = ""
        for bit_char in list(map(int, binary[i:i + 8])):
            byte_str = byte_str + str(bit_char)
        byte_num = int(byte_str, base=2)
        s1 = s1 + code[str(byte_num)]
        i = i + 8

    return s1


def S1_to_S4(s1):
    """
    :param s1: array of [0, 1, 2]
    :return: s4 is s1 with appended information about the length of s1
    """
    # Compute s2
    n = len(s1)
    s2 = base10_to_base3(n)
    s2 = '0' * (20 - len(s2)) + s2

    # Compute s3
    s3 = '0' * (-(n + len(s2) % 25) % 25)

    # Compute s4
    s4 = s1 + s3 + s2
    return s4


def S4_to_S5(s4):
    """ convert trinary [0, 1, 2] to DNA [A, T, C, G] as it was described by Goldman et al. (2013).

    :param s4: array of [0, 1, 2]
    :return: string of [A, T, C, G]
    """
    # Create table
    dna_table = {
        'A': ['C', 'G', 'T'],
        'C': ['G', 'T', 'A'],
        'G': ['T', 'A', 'C'],
        'T': ['A', 'C', 'G']
    }

    s5 = ''
    s5 = s5 + dna_table['A'][int(s4[0])]
    # print(s4)
    for c in s4[1:]:
        # print(s5[-1],int(c))
        s5 = s5 + dna_table[s5[-1]][int(c)]

    return s5


def S5_to_Fi(s5):
    """ split s5 in overlapping arrays of length 100 with an offset of 25 and create the reverse complement
    of every odd segment.

    :param s5: string of [A, T, C, G]
    :return: array of DNA segments (strings) [[A, T, C, G],...,[A, T, C, G]]
    """
    n = len(s5)
    F = []
    for i in range(0, int(n / 25 - 3)):
        # Reverse if odd
        if i % 2 == 1:
            F.append(reverse_complement(s5[25 * i:25 * i + 100]))
        else:
            F.append(s5[25 * i:25 * i + 100])
    return F


def Fi_to_Findex(F, input_file):
    """ append to every nucleotide segment in F information about its position in F (order) and about the
    input_file. Also append information about the start and final end of each nucleotide segment.
    Explanation. Information about the position in F is needed because practical DNA synthesis and sequencing
    may change the order of the nucleotide strings in F.
    Explanation. Information about the input_file allows the mixing of DNA of different experiments/ files
    which might be favourable for a more cost efficient DNA synthesizing / sequencing process and therefore
    might facilitate real world applications of this algorithm.

    :param F: array of DNA segments (strings) [[A, T, C, G],...,[A, T, C, G]]
    :param input_file: str, some name for the data to be encoded
    :return: array of DNA segments (strings) [[A, T, C, G],...,[A, T, C, G]]
    """
    # Indexed segments
    Findex = []

    # File ID
    ID = files_trits[input_file]

    # Create table
    dna_table = {
        'A': ['C', 'G', 'T'],
        'C': ['G', 'T', 'A'],
        'G': ['T', 'A', 'C'],
        'T': ['A', 'C', 'G']
    }

    # For each segment compute the IX
    for i in range(0, len(F)):
        i3 = base10_to_base3(i)
        i3 = '0' * (12 - len(i3)) + i3
        P = (int(ID[1 - 1]) + int(i3[1 - 1]) + int(i3[3 - 1]) +
             int(i3[5 - 1]) + int(i3[7 - 1]) + int(i3[9 - 1]) + int(i3[11 - 1])) % 3
        IX = ID + i3 + str(P)

        ix = ''
        ix = ix + dna_table[F[i][-1]][int(IX[0])]
        for c in IX[1:]:
            ix = ix + dna_table[ix[-1]][int(c)]

        if F[i][0] == 'A':
            F[i] = 'T' + F[i]
        elif F[i][0] == 'T':
            F[i] = 'A' + F[i]
        else:
            if randint(0, 1) == 0:
                F[i] = 'A' + F[i]
            else:
                F[i] = 'T' + F[i]

        if ix[-1] == 'C':
            ix = ix + 'G'
        elif ix[-1] == 'G':
            ix = ix + 'C'
        else:
            if randint(0, 1) == 0:
                ix = ix + 'G'
            else:
                ix = ix + 'C'

        Findex.append(F[i] + ix)

    return Findex


# functions used to decode data stored in dna back to its binary format / called by decode(dnastr)


def Findex_to_Fi(Findex):
    """
    :param Findex: array of DNA segments (strings) [[A, T, C, G],...,[A, T, C, G]]
    :return: sorted array of DNA segments (strings) [[A, T, C, G],...,[A, T, C, G]] with each segment
    removed of its reading direction and indexing information; and reversed complemented if odd.
    """
    # Create inverse table
    dna_inv_table = {
        'A': {'T': '0', 'G': '1', 'C': '2'},
        'C': {'A': '0', 'T': '1', 'G': '2'},
        'G': {'C': '0', 'A': '1', 'T': '2'},
        'T': {'G': '0', 'C': '1', 'A': '2'}
    }

    F = [''] * len(Findex)

    for Fi in Findex:

        # Check if reverse complemented
        if Fi[0] != 'T' and Fi[0] != 'A':
            Fi = reverse_complement(Fi)

        # Remove prepended A/T and appended C/G
        Fi = Fi[1:116]  # Prior lenght of Fi is 117

        # Extract ix (last 15) n DNA format
        ix = Fi[-15:]
        Fi = Fi[:-15]

        # Convert ix to trits (IX)
        lastFi = Fi[-1]
        IX = dna_inv_table[ix[0]][lastFi]
        for i in range(1, 15):
            IX = IX + dna_inv_table[ix[i]][ix[i - 1]]

        # Extract ID
        ID = IX[:2]

        # Extract i3 and i
        i3 = IX[2:len(IX) - 1]
        i = int(base3_to_base10(i3))

        # Checksum error
        P = int(IX[-1])
        Pexpected = (int(ID[1 - 1]) + int(i3[1 - 1]) + int(i3[3 - 1]) +
                     int(i3[5 - 1]) + int(i3[7 - 1]) + int(i3[9 - 1]) + int(i3[11 - 1])) % 3
        if P != Pexpected:
            print("Corrupted segment:\nID = %s\ni = %d" % (ID, i))
        else:
            # Save Fi
            if i % 2 == 1:
                F[i] = reverse_complement(Fi)
            else:
                F[i] = Fi
    return F


def Fi_to_S5(Fi):
    """ In real applications we should check if the overlapping. That why this function is not called by
    the decode function :-)

    :param Fi: array of DNA segments (strings) [[A, T, C, G],...,[A, T, C, G]]
    :return: String of [A, T, C, G]
    """

    s5 = Fi[0][0:75]
    # print(len(Fi))
    # print(Fi)
    for f in Fi:
        s5 = s5 + f[-25:]
    return s5


def majority_vote(seqs):
    """ This function performs a majority vote in the sense that of each corresponding nucleotide that is
    chosen, which occurs most often.

    :param seqs: array of DNA segments (strings) [[A, T, C, G],...,[A, T, C, G]]
    :return: String of [A, T, C, G]
    """
    dna_str = ""
    s_in_seq = 0
    pos_in_s = 0
    leng_dna = 0

    while s_in_seq < len(seqs):
        nucs_temp = []

        nucs_temp.append(seqs[s_in_seq][pos_in_s])
        if s_in_seq + 1 < len(seqs) and pos_in_s - 25 >= 0:
            nucs_temp.append(seqs[s_in_seq + 1][pos_in_s - 25])
        else:
            nucs_temp.append(nucs_temp[0])
        if s_in_seq + 2 < len(seqs) and pos_in_s - 50 >= 0:
            nucs_temp.append(seqs[s_in_seq + 2][pos_in_s - 50])
        else:
            nucs_temp.append(nucs_temp[0])
        if s_in_seq + 3 < len(seqs) and pos_in_s - 75 >= 0:
            nucs_temp.append(seqs[s_in_seq + 3][pos_in_s - 75])
        else:
            nucs_temp.append(nucs_temp[0])

        count_nucs = [0, 0, 0, 0]  # [A, T, C, G]
        for nuc in nucs_temp:
            if nuc == 'A':
                count_nucs[0] += 1
                if count_nucs[0] >= 2:
                    dna_str += "A"
                    leng_dna += 1
                    break
            elif nuc == 'T':
                count_nucs[1] += 1
                if count_nucs[1] >= 2:
                    dna_str += "T"
                    leng_dna += 1
                    break
            elif nuc == 'C':
                count_nucs[2] += 1
                if count_nucs[2] >= 2:
                    dna_str += "C"
                    leng_dna += 1
                    break
            else:
                count_nucs[3] += 1
                if count_nucs[3] >= 2:
                    dna_str += "G"
                    leng_dna += 1
                    break

        # if no nulceotide is at least doubled append "A" - alternatively to preserve the data length
        if count_nucs.__eq__([1, 1, 1, 1]):
            dna_str += "A"
            leng_dna += 1

        pos_in_s = pos_in_s + 1
        if pos_in_s >= 100:
            pos_in_s = 75
            s_in_seq = s_in_seq + 1

    # print(leng)
    # print(len(dna_str))

    return dna_str


def S5_to_S4(s5):
    """ convert DNA [A, T, C, G] to trinary [0, 1, 2]. Note. This function will course a programme crash if
    due to mutation etc. a nucleotide is followed by itself.

    :param s5: String of [A, T, C, G]
    :return: Array of [0, 1, 2]
    """
    # Create inverse table
    dna_inv_table = {
        'A': {'T': '0', 'G': '1', 'C': '2'},
        'C': {'A': '0', 'T': '1', 'G': '2'},
        'G': {'C': '0', 'A': '1', 'T': '2'},
        'T': {'G': '0', 'C': '1', 'A': '2'}
    }

    s4 = ''
    for i in range(len(s5) - 1, 0, -1):
        s4 = dna_inv_table[s5[i]][s5[i - 1]] + s4
    s4 = dna_inv_table[s5[0]]['A'] + s4

    return s4


def S4_to_S0(s4):
    """ detach information about the data length and convert trinary to binary.

    :param s4: Array of [0, 1, 2]
    :return: Array of [0, 1]
    """
    # s2 is the last 20 trits
    s2 = s4[-20:]

    # n = len(s1) is s2 converted to base 10
    n = base3_to_base10(s2)

    # s1 is the first n trits
    s1 = s4[:int(n)]
    # print("s1:" + str(len(s1)))

    # Time to convert s1 from trits to bytes in s0
    inverted_code = dict([v, k] for k, v in code.items())
    s0 = ''
    i = 0
    while i != n:
        if s1[i:i + 5] in inverted_code.keys():
            # s0 = s0 + bin(int(inverted_code[s1[i:i + 5]])).replace("0b", "") # s0 = s0 + ''.join('%02x' % int(inverted_code[s1[i:i + 5]]))
            add = bin(int(inverted_code[s1[i:i + 5]]))[2:]  # same output
            while len(add) < 8:
                add = "0" + add  # It seems, that leading zeroes go missing ... I prepend them here
            s0 = s0 + add
            i = i + 5
        else:
            # s0 = s0 + bin(int(inverted_code[s1[i:i + 6]])).replace("0b", "") # s0 = s0 + ''.join('%02x' % int(inverted_code[s1[i:i + 6]]))
            add = bin(int(inverted_code[s1[i:i + 6]]))[2:]  # same output
            while len(add) < 8:
                add = "0" + add  # It seems, that leading zeroes go missing ... I prepend them here
            s0 = s0 + add
            i = i + 6

    return s0


# some functions that are called as helper functions above


def read_huff(file):
    """
    :param file: path to huffman dictionary as it comes with this programme
    :return: non. this method fills the programme variable huff_dict
    """
    huff_dict = open(file, "r")
    csv_reader = csv.reader(huff_dict, delimiter=',')
    for row in csv_reader:
        code[row[0]] = row[1]


def base10_to_base3(n):
    """
    :param n: int (base 10)
    :return: str (base 3 representation of int)
    """
    if n == 0:
        return '0'
    # This is a different algorithm from the one implemented by "Allanino", as the latter was flawed.
    nums = []
    while n:
        n, r = divmod(n, 3)
        nums.append(str(r))
    return ''.join(reversed(nums))


def base3_to_base10(n):
    """
    :param n: str (base 3 representation of int)
    :return: int (base 10)
    """
    # The method function base3_to_base10(n) as it war written by Allario
    # seemed to be faulty so I implemented a new one
    power = len(n) - 1
    decim = 0
    for char in n:
        decim = decim + int(char) * pow(3, power)
        power = power - 1
    return decim


def binary_to_hexa(n):
    """
    :param n: str [0, 1]
    :return: hexadecimal representation of n
    """
    # convert binary to int
    num = int(n, 2)
    # convert int to hexadecimal
    hex_num = hex(num)
    return hex_num


def reverse_complement(s):
    """ build the reverse complement of s that is: read from back to start and A is T and C is G and vice versa.

    :param s: str [A, T, C, G]
    :return:  str [A, T, C, G]
    """
    reverse = ''

    complement_dict = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

    for c in s:
        reverse = complement_dict[c] + reverse

    return reverse
