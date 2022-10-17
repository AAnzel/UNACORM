import numpy
import goldman
import random

# binary1 = numpy.load('La_Jeunesse.npy')
binary1 = numpy.load('Vue_de_la_Buena_Vista.npy')
# print(binary1)
dna_str = goldman.encode(binary1, "La_Jeunesse")
# print(dna_str)
random.shuffle(dna_str)
binary2 = goldman.decode(dna_str)
# print(binary2)
# print(len(binary1), len(binary2))
# print(len(binary1)==len(binary2))

print("------ERROR ANALYSIS:-------")

# exit()

count_errors = 0
count_position = 0

print("binary before encoding | binary after decoding | position")
while count_position < len(binary1):
    if binary1[count_position] != binary2[count_position]:
        print((binary1[count_position], binary2[count_position], count_position))
        count_errors = count_errors + 1
    count_position = count_position + 1
print("Total amount of wrong bits:")
print(str(count_errors) + "   (of " + str(len(binary1)) + " Bits)")
print("Second check, if both arrays are equal:")
print(numpy.array_equal(binary2, binary1))
