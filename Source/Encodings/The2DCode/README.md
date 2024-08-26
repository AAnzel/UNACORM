# ReedSolomonDNA En-/Decoder
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#generalized-solomon">Generalized Reed Solomon Code</a>
      <ul>
          <li><a href="#documentation">Documentation</a></li>
          <li><a href="#usage">Usage</a></li>
          <li><a href="#dependencies">Dependencies</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started-with-the-modul">Getting Started with the modul</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
	<li><a href="#usage-of-the-api">Usage of the API</a></li>
	<li><a href="#documentation-of-module">Documentation of module</a></li>
	<li><a href="#license">License</a></li>
	<li><a href="#contacts">Contacts</a></li>
	<li><a href="#acknowledgments">Acknowledgments</a></li>
      </ul>
    </li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This module is a python implementation for encoding and decoding information using Reed Solomon self-correcting codes.

In particular, this module is a research work on behalf of the Philipps University Marburg (DE), input formats as well as output formats were given in this framework.
Basic implementations have been programmed based on the paper ```'Robust Chemical Preservation of Digital Information on DNA in Silica with Error Correcting Codes'```. 
An aid for the transformation of data into different number systems and internal formats was the repository via ```'dna_data_storage'``` by Reinhard Heckel (link can be found in Acknowledgments).
A special kind of Reed Solomon Code is used to encode or decode data. This special implementation called Generalized Reed Solomon is according to the paper ```'A Class of Generalized RS-Codes with Faster
Encoding and Decoding Algorithms'``` by Amin Shokrollahi.



<!-- GENERALIZED SOLOMON -->
## Generalized Reed Solomon Code
This special code can be sped up by a factor of p, since the code can be parallelized over p components. Additionally it allows to construct codes of arbitrary length as long as n%p == 0 is fulfilled and a primitive root of unity p can be found in the corresponding field over which the code is constructed. Whereas the standard Reed Solomon code imposes n= q^m -1. The code can be constructed over all Galois Fields.

## Documentation
n = k + r <br/>
k = message symbols sent <br/>
r = number of parity symbols <br/>
p = speed up factor <br/>

Currently the code can also handle codes where n %p != 0 however only if r is still divisble by p.
### Class Generalized_Reed_Solomon
```
class Generalized_Reed_Solomon(
field_size:int, #q characterisitc of the field
message_length:int, # n
payload_length:int, # k
symbol_size:int, #m exponent of field. Order of field is q^m
p_factor:int, #p speedup factor
irr_poly=None:array, # optional in case that the galois libary has not a precomputed irreducible polynominal
multi_processing = False, #optional when True certain parts of the code will be parallelized this is however currently only efficent when operating with long messages
debug=False # can be set to true in order to have the steps printed to the console
)
```
### Generalized_Reed_Solomon.encode()
```
Generalized_Reed_Solomon.encode(self,array)
# Takes as an argument a list and appends parity symbols to it
```
### Generalized_Reed_Solomon.decode()
```
Generalized_Reed_Solomon.decode(self, recieved_msg)
# Takes as an argument a list of a encoded message. Detects and corrects errors and then returns the k info symbols
```
### Generalized_Reed_Solomon.convert_to_symbol_array()
```
Generalized_Reed_Solomon.convert_to_symbol_array(self,array)
# Takes as an argument a list values and converts them to galois elements. If the degree of field > 1, the list will be´a list of list
# where each list represents the coefficents of a Galois element of the corresponding Field
```

### Generalized_Reed_Solomon.symbol_array_to_array()
```
Generalized_Reed_Solomon.symbol_array_to_array(self,array)
# Takes a list of ints as an argument. Performs the reverse of convert_to_symbol_array(). Transforms each Galois field element in the list
# into its coefficent representation.
```
## Usage
```
import generalizedReedSolomon
import numpy as np

org_info = [30, 20, 20, 9, 25, 1, 7, 2, 0, 18, 17, 22, 11,0,0]
org_compare = np.copy(org_info)
test_normal_rs = generalizedReedSolomon.Generalized_Reed_Solomon(field_size=31,
                                                                 message_length=27,
                                                                 payload_length=15,
                                                                 symbol_size=1,
                                                                 p_factor=3)
# encode message
normal_msg = test_normal_rs.encode(org_info)
#corrupt encode message
normal_msg[6] = 10
normal_msg[9] = 12
normal_msg[10] = 0
normal_msg[16] = 4
normal_msg[23] = 10

#fix encoded message
dec_test_normal = test_normal_rs.decode(normal_msg)
print("dec",dec_test_normal)
print("org",org_info)
print("equal",org_info == dec_test_normal)

#dec [30, 20, 20, 9, 25, 1, 7, 2, 0, 18, 17, 22, 11, 0, 0]
#org [30, 20, 20, 9, 25, 1, 7, 2, 0, 18, 17, 22, 11, 0, 0]
#equal True
```
```
 info_symbols = [
        [20,5],
        [35,10],
        [5,10],
        [35,20],
        [35,10],
        [3,10],
        [35,10],
        [35,2],
        [5,10],
        [35,10]
    ]
test_normal_rs =reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                                 message_length=14,
                                                                 payload_length=10,
                                                                 symbol_size=2,
                                                                 p_factor=2,
                                                                debug=True)
#convert to galois elements
symbols = test_normal_rs.convert_to_symbol_array(info_symbols)
print("symbols",symbols)
symbols_encoded = test_normal_rs.encode(symbols)
symbols_encoded[0] =1
#convert Galois Elements back to coefficent representation
symbols_decoded = test_normal_rs.decode(symbols_encoded)
conv_back = test_normal_rs.symbol_array_to_array(symbols_decoded)
    
print(conv_back)
print(info_symbols == conv_back)
#symbols [945, 1655, 245, 1665, 1655, 151, 1655, 1647, 245, 1655]
#[[20, 5], [35, 10], [5, 10], [35, 20], [35, 10], [3, 10], [35, 10], [35, 2], [5, 10], [35, 10]]
#True
```
## Dependencies
galois == 0.0.28 <br/>
numpy == 1.19.5

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED WITH THE MODUL -->
## Getting Started with the Modul

### Prerequisites

To use the libary Python 3.8.8 or higher must be installed. Installation as follows in Python 3:

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/raeudigerRaeffi/reedSolomonDNA
   ```
2. Install needed packages
   ```sh
   pip install galois
   pip install numpy
   ```
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE OF THE API -->
## Usage of the API

To load the module the folder ```'reedSolomonDNA'``` must be in your project folder.
```
YOUR_PROJECT
  |- reedSolomonDNA
  |- your_main.py
  .
  .
```


The following explains how to use the API. First you have to import the module:
   ```python
   # Recommended import of the reedSolomonDNA module
   import reedSolomonDNA as dna

   # Creating an API object
   api = dna.encoder.api()
   ```
### Test
To test if all necessary libraries are installed and the module is imported correctly, run the unity test as follows:
   ```python
   api.utility_test()
   ```
The test itself loads a test file from the ```'test/data'``` folder and encodes it first, then shuffles the output DNA strand to simulate errors and decodes it again. At the end, errors are displayed between the test file and the decoded message.

During the test, the progress is displayed on the console. This process may take some time!

### Encode
To encode a file yourself you must provide an input that is either a string with a file path representing a numpy boolean array or pass the loaded numpy boolean array of the text to be translated directly. As a return a list with the strings of the DNA strings is returned:
   ```python
   # api.encode(file_path, boolean_numpy_array)
   
   # Encode method through a file path
   list_dna_str = api.encode('reedSolomonDNA/test/data/La_Jeunesse.npy', '')
    
   # Load or create a numpy boolean array and call the encode method 
   input_data = np.load('reedSolomonDNA/test/data/La_Jeunesse.npy')
   list_dna_str = api.encode('', input_data)
   ```
Test calls using test data available in the module.

### Decode
Decode runs similar to the encode method. A boolean numpy array is returned:
   ```python
   # api.decode(file_path, list_of_dna_strings)
   
   # Decode method through a file path
   np_array = api.decode('reedSolomonDNA/test/data/encoded_data.txt', '')
    

   # Load or create a list of DNA strings and call the decode method
   input_data = []
   with open('reedSolomonDNA/test/data/encoded_data.txt', 'r') as data:
        input_data = data.readlines()
   np_array = api.decode('', input_data)
   ```
Test calls using test data available in the module.

<!-- DOCUMENTATION OF MODULE -->
## Documentation of module

### Input format
Any text file can be encoded or decoded by the module. A file that is to be encoded must be transformed into a boolean array.
To transform it, format the text by splitting the string in pairs and create a boolean array in numpy that represents the character pairs as a byte boolean vector.
   ```python
   # Split text into a list of string pairs of ASCII characters
   'The text must be divided into pairs.' --> ['Th','e ','te','xt', ... ,' i','nt','o ','pa','ir','s.']
   
   # Transform all pairs into a numpy array of one byte boolean vectors
   ['Th','e ','te','xt', ... ,' i','nt','o ','pa','ir','s.'] --> [ [TRUE,FALSE,TRUE,TRUE,TRUE,FALSE,FALSE,TRUE]
								  		... ]
   ```

### Output format
After encoding, a list of DNA strands is returned that must be dealt with.
   ```python
   # Returned format
   [ [GGTGGTAGAGCACGCACGCTCAAGACGGGAGTC ... CACTTATACGCTAAAGATACGTACGACAGATCGCGAGGAT]
     [CTGGTCTCATCAACAGCGCCGTGTGGAAGTGGG ... CATTGTTGCTACAGAAAGTAGAGAAGCTATCCTATCTGGA]
                                        ... ]
   ```
The decode method returns a numpy boolean array.
   ```python
   [ [TRUE,FALSE,TRUE,TRUE,TRUE,FALSE,FALSE,TRUE]
     [FALSE,FALSE,FALSE,TRUE,FALSE,TRUE,TRUE,TRUE]
			... ]
   ```

### Encode
The encode method takes a string with the file path or a numpy boolean array.
   ```python
   def encode(self, string_file_name:str, numpy_boolean_array):
   ```

The input is checked and depending on whether a relative file path was specified or a numpy boolean array was passed, either the encode process is continued or the file is read and its data loaded into the appropriate format. In case of any errors or wrong formats an error is output.

After the input is checked, the generalized Reed Solomon code is initialized (as can be seen in the Generalized Reed Solomon Code documentation). 
The passed boolean array is transformed to a list of ASCII pairs.
   ```python
   def bools_to_int(bits):
    value = 0
    for i, bit in enumerate(bits):
        value |= bit << (len(bits) - i - 1)
    return value

   ```
This is made possible by a list comprehension and bitwise shift.
This list of ASCII pairs, represented as integers, is mapped to a Galoise Field with values 0 to 46.
This is achieved by a transformation of the number format.

To encode the information the input must be transformed to an array that represents the encode block with the length 713x39. *Only this array is encoded*.

A list of values is given back, these are mapped by the codon wheel to a sequence of three nucleotides.
   ```python
   # Part of the Codon Wheel class
   # Pair to number dicionary for mapping nucleotides to a GF(47) value.
   self.pair_to_number = {'ATC': 22,
                               'ATA': 15,
                               'ATG': 9,
                               'ACT': 31,
                               'ACA': 25,
                               'ACG': 2,
                               'AAT': 42,
                               'AAC': 24,
                               'AAG': 12,
                               'AGT': 16,
                               'AGC': 5,
                               'AGA': 1,
                               'GTC': 27,
                               'GTA': 18,
                               'GTG': 33,
                               'GCT': 10,
                               'GCA': 4,
                               'GCG': 26,
                               'GAT': 30,
                               'GAC': 20,
                               'GAG': 46,
                               'GGT': 0,
                               'GGC': 29,
                               'GGA': 39,
                               'TTC': 14,
                               'TTA': 8,
                               'TTG': 34,
                               'TCT': 13,
                               'TCA': 23,
                               'TCG': 36,
                               'TAT': 37,
                               'TAC': 21,
                               'TAG': 44,
                               'TGT': 45,
                               'TGC': 6,
                               'TGA': 38,
                               'CTC': 19,
                               'CTA': 11,
                               'CTG': 17,
                               'CCT': 43,
                               'CCA': 41,
                               'CCG': 7,
                               'CAT': 40,
                               'CAC': 35,
                               'CAG': '*',
                               'CGT': 3,
                               'CGC': 28,
                               'CGA': 32}
	# Number to pair dicionary for mapping GF(47) values to nucleotides.
        self.number_to_pair = {v: k for k, v in    self.pair_to_number.items()}
   ```
   A list of nucleotide sequences is returned to the API.

### Decode
The decoding function runs recursively with respect to the encoding function.

Instead of a boolean array we work with a list containing the sequences of the nucleotides. The input is checked first and the generalized Reed Solomon code is initialized.

To encode the nucleotide sequences an aaray with the blocks of length 713x39 must be created again. This is made possible by simple modulo operations that ask if a block length has been reached and the next one can be filled with information.

Since we cannot take the nucleotide sequences for encoding, we first map all sequences via the codon wheel into a GF(47) value.
The transformed sequences are then decoded as a block.
The encoded information is again taken from a block to a list of Galoise Field values of the form 47^3.

To get a readable form all Galoise field triplets are transformed to ASCII pairs. This is done again by converting the number system. To get the desired output again the list with ASCII pairs is transferred into a boolean array and will be returned to the API.
   
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Raffael Schön - raffaelschon@rocketmail.com

Samuel Becker - becker-samu@gmx.de

Felix Klein - f.m.klein@online.de 

Project Link: [https://github.com/raeudigerRaeffi/reedSolomonDNA](https://github.com/raeudigerRaeffi/reedSolomonDNA)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Reinhard Heckel - https://github.com/reinhardh

Robert N. Grass, Reinhard Heckel, Michela Puddu, Daniela Paunescu, and Wendelin J. Stark
 - Robust Chemical Preservation of Digital Information on DNA in Silica with Error-Correcting Codes 
 - https://www.researchgate.net/publication/272029638_Robust_Chemical_Preservation_of_Digital_Information_on_DNA_in_Silica_with_Error-Correcting_Codes

Amin Shokrollahi 
 - A Class of Generalized RS-Codes with Faster Encoding and Decoding Algorithms
 - https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.306.4767&rep=rep1&type=pdf

<p align="right">(<a href="#readme-top">back to top</a>)</p>
