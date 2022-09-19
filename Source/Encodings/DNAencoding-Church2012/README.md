# DNA-Encoding
based on "Next-Generation Digital Information Storage in DNA" paper
# How to install and use
clone the project to have it locally on the machine
change directory to src and run DNA2Bits.py 

# Project Description
this project uses the algorithm provided in the "Next-Generation Digital Information Storage in DNA" paper in order to encode binary data into DNA segments. the decoding process is d
 
    # enocde
    this function takes a string file name(unused) and a numpy array of boolean values as parameters, 
    for every 8 bits, we call bits2byte function that returns a byte, which then gets fed to the byte2pb function, the latter returns DNA segments.
    We assign 19 bits to the address of a segment
    A segment is 12 bytes long, the maximum amount of “oligos” is set to 2^19.
    The creation of DNA is as follows
    an oligo starts with a primer f ( forward universal sequencing and amplification primer), we then write the address of the segment, then the encoded segment ( which is 12 bytes long),then a primer r( a reverse 22-mer primer ) at the end.
    We check if the last segment is 12 bytes long, if not, we add padding ( random data at the end of the  segment) to keep all oligos the same size.

    # decode
    this function takes a string file name(unused) and a list of DNA segments as parameters.
    For every DNA string, we check if it has the start and ending primer, we then extract the encoded data. In a loop we convert the 12 bytes of data of the oligo into boolean values.

    # verify_segments_order
    this function takes the DNA segments list as parameter, it then sorts them using the address of each segment.Once the segments are sorted, it checks if the address of every segment matches its position, if not, then we can safely assume that certain segments got lost during the syntheszing and/or sequencing step

    # int2bp
    this function converts the adress of a block of information into bp
    

