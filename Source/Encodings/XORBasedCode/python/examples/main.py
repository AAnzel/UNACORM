import numpy as np
import xor_code_python as xor


def get_bit(data, num):
    byte = int(num // 8)
    shift = int(num % 8)
    return (data[byte] >> shift) & 0x1 == 0x1


def file_to_boolean_array(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    return np.array([get_bit(data, i) for i in range(len(data) * 8)])


file = 'test.txt'

T = file_to_boolean_array('./python/examples/data/' + file)

print('Setting max strand length to 120...')
xor.set_max_strand_length(120)
print('Max strand length: ' + str(xor.get_max_strand_length()))

xor.set_xor_step(2)
xor.set_xor_size(3)

E = xor.encode(file, T)
D = xor.decode(file, E)
print('Correctly decoded: ' + str((T == D).all()))
