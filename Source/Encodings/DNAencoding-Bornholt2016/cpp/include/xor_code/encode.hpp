#ifndef XOR_CODE_ENCODE_H
#define XOR_CODE_ENCODE_H

#include "settings.hpp"
#include "nucleotideUtils.hpp"

#include <cstdint>
#include <memory>
#include <string>
#include <fstream>
#include <vector>
#include <list>
#include <array>

namespace xor_code {

    struct strand {
        types::nucleotides payload;
        union {
            uint64_t lowAddress;
            std::array<uint8_t, 8> lowAddressArray;
        };
        bool isXor;
        types::nucleotides *primerBegin;
        types::nucleotides *primerEnd;
    };

    /**
     * Encodes the given data into strands of nucleotides.
     *
     * @param key The string identifying the given data.
     * @param bytes The binary data to be encoded.
     * @return The encoded nucleotide strands.
     */
    std::vector<types::nucleotides> encode(const std::string &key, types::bytes &bytes);

    /**
     * Encodes the given data into strands of nucleotides.
     *
     * @param key The string identifying the given data.
     * @param input The binary stream to be encoded.
     * @return The encoded nucleotide strands.
     */
    std::vector<types::nucleotides> encode(const std::string &key, std::istream &input);

    /**
     * Encodes the given data into strands of nucleotides.
     *
     * @param filePath The file to be read and encoded.
     * @return The encoded nucleotide strands.
     */
    std::vector<types::nucleotides> encode(const std::string &filePath);

}

#endif //XOR_CODE_ENCODE_H
