# DNAencoding-Goldman2013
encode binary data (0, 1) to DNA (A, T, C, G) and decode vice versa - an implementation of Goldman et al. (2013)

### How to Setup
Download or clown this repository. Make sure you have installed python3. Make sure you have also installed the python modules numpy, csv and optional random if you also want to run testcode2.py. Test-data need to be binary data in .npy-format. Make sure that the data folder with the huff3.dict file has on your computer the same relative path to Goldman.py as it is the case in this repository and specified in line 38 of Goldman.py.

### About goldman.py
Goldman.py provides two main methods: encode(binary, file_name) encodes an arbitrary binary string (binary) with a file name (string, file_name) in DNA form as described by Goldman et al. (2013) and therefore returns a string of [A, T, C, G]. decode(dnastr) decodes an DNA string as it would be produced by encode(binary, file_name) back to its binary representation as it is left to the reader as an "exercise" by Goldman et al. (2013).

### About testcode2.py
testcode2.py is used to test Goldman.py. Specify in line 6 the path to your test data and give it in line 8 a suitable name. Also make sure that you test-data is binary data stored as .npy-file. Otherwise, you have to make some adjustments of you own.

### Important Notice
The program Goldman.py will crash if you call the decode function on data which contains sequences of nucleotides in which a nucleotides successor is itself. 

## a thousand thanks to ...	
Allan Costa as the majority of this code is built on his repository you can find on github at https://github.com/allanino/DNA/blob/master/dna.

