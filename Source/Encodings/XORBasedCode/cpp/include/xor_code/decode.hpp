#ifndef XOR_CODE_DECODE_H
#define XOR_CODE_DECODE_H

#include "settings.hpp"

#include <cstdint>
#include <vector>
#include <list>
#include <string>

namespace xor_code {

    /**
     * Decodes the given nucleotide strands, filtered by the given key, into binary data.
     *
     * @param key The string identifying the relevant strands.
     * @param strands The strands to be decoded.
     * @return The decoded data as a vector of bytes.
     */
    types::bytes decode(std::string key, std::vector<types::nucleotides> &strands);

}

#endif //XOR_CODE_DECODE_H
