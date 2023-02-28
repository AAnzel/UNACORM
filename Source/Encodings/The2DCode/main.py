# Import
import numpy as np
import time
import random
import galois as gl
from pyrsistent import field
import utils.NumberSystemConversion as nsc
import utils.dna_wheel as dna_wheel
import reedSolomon

def load_dataset(filepath='data/the_federal_charter_of_1291.txt'):
    '''
    Load the dataset as string
    Parameters
    ----------
    filepath : string
    Returns
    -------
    data_string : string
    '''
    with open(filepath) as file:
        data_string = file.read()
    return data_string


if __name__ == '__main__':
    '''
    Main function
    '''

   
    """
    org_info = np.random.randint(2000, size=594).tolist()
    org_compare = np.copy(org_info)
    irr_poly_47 = [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1, 32]
    test_normal_rs =reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                                 message_length=713,
                                                                 payload_length=594,
                                                                 symbol_size=30,
                                                                 p_factor=7,
                                                                irr_poly=irr_poly_47,
                                                                debug=False)
    
    normal_msg = test_normal_rs.encode(org_info)
    normal_msg[1] = 10
    normal_msg[9] = 12
    normal_msg[10] = 0
  
    #normal_msg =  [0,0] +normal_msg[0:13]+ normal_msg[15:len(normal_msg)]
    dec_test_normal = test_normal_rs.decode(normal_msg)
    print("dec",dec_test_normal)
    print("org",org_info)
    print(dec_test_normal == org_info)
    """
    start = time.process_time()
    info = [0, 28, 29, 10, 28, 2, 7, 10, 18, 31, 24, 3, 12, 35, 10, 23, 10, 12, 13, 40, 8, 10, 43, 21, 40, 21, 15, 44, 37, 3, 3, 33, 7]

    inner_encoder = reedSolomon.Generalized_Reed_Solomon(field_size=47,
                                                         message_length=39,
                                                         payload_length=33,
                                                         symbol_size=1,
                                                         p_factor=2)

    print(len(info))
    encoded = inner_encoder.encode(info)
    encoded[0] = 2
    encoded[1] = 2
    decoded = inner_encoder.decode(encoded)
    print(decoded)
    print(info == decoded)
    print(time.process_time() - start)
    
    print(str(time.perf_counter()/1000)+' s')


    # n = k +r  k = information r = parity bits
    # n / p -> k /p und r/p
    # p = 23 713 
    # k % p != 0 r %p = 0
    # wähle p so dass r /p   n = 713,k = 594,r=119 und p = 17

    #veränderung von p führt zu fehler -> 
    ##veränderung von field size führt zu fehler
