class NumberSystemConversion():
    '''
    Following code can be used as unit test:

    errors = 0
    for x in range(0, 256):
        for y in range(0, 256):
            test_set = [x, y]
            converted_test_set = nsc.char2pfe(test_set)
            reverted_test_set = nsc.pfe2char(converted_test_set)
            for i, ele in enumerate(test_set):
                if(reverted_test_set[i] != ele):
                    print("Error!", test_set,
                          converted_test_set, reverted_test_set)
                    errors += 1
                    break

    print(errors)
    '''
    # C++ implementierung
    def tobase(nu, base, size):
        nn = []
        for x in range(size):
            nn.append(0)
        if(nu == 0):
            return nn

        div = nu
        i = 0
        while(div != 0 and i < size):
            nn[i] = int(div % base)
            div = int(div / base)
            i += 1

        return nn

    def frombase(nn, base):
        nu = 0
        basepow = 1
        for n in nn:
            nu += (n * basepow)
            basepow *= base

        return nu

    def char2pfe(data_char):
        output = []

        if((len(data_char) % 2) != 0):
            data_char.append(10)  # append \n

        for i in range(0, len(data_char), 2):
            indec = NumberSystemConversion.frombase(data_char[i:i+2], 256)
            tmpvec = NumberSystemConversion.tobase(indec, 47, 3)
            output.extend(tmpvec)

        return output

    def pfe2char(data_char):
        output = []

        if((len(data_char) % 3) != 0):
            return output

        for i in range(0, len(data_char), 3):
            indec = NumberSystemConversion.frombase(data_char[i:i+3], 47)
            tmpvec = NumberSystemConversion.tobase(indec, 256, 2)
            output.extend(tmpvec)

        return output

    # Raffaels implementierung
    def convert_between_bases(num_arr, origin_base, target_base, target_degree):
        def to_base_10(num_arr, origin_base):
            num = 0
            for index, element in enumerate(num_arr[::-1]):
                if element >= origin_base:
                    raise ValueError("Val cant be higher than base")
                num = num + (element * origin_base*index)
            return num

        def from_10_to_base(num, target_base):
            digits = []
            if num == 0:
                return [0]
            while num:
                digits.append(int(num % target_base))
                num //= target_base
            return digits[::-1]

        new_base_rep = from_10_to_base(
            to_base_10(num_arr, origin_base), target_base)
        if len(new_base_rep) < target_degree:
            return (target_degree - len(new_base_rep))[0] + new_base_rep
        return new_base_rep
