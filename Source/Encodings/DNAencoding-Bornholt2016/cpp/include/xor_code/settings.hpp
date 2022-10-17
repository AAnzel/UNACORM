#ifndef XOR_CODE_SETTINGS_H
#define XOR_CODE_SETTINGS_H

#include <cstdint>
#include <vector>

namespace xor_code {

    namespace types {

        /**
         * A Random Access Iterator for a vector containing uint8_t values.
         */
        typedef std::vector<uint8_t>::iterator iter;
        /**
         * A vector containing bytes.
         */
        typedef std::vector<uint8_t> bytes;
        /**
         * A vector containing ternary digits.
         * Possible values: 0, 1, 2.
         */
        typedef std::vector<uint8_t> ternaries;
        /**
         * A vector containing integer representations of nucleotides.
         * Possible values: 0, 1, 2, 3.
         */
        typedef std::vector<uint8_t> nucleotides;

    }

    const int NUCLEOTIDES_PER_PRIMER = 12;

    const int MAX_NUCLEOTIDES_PER_BYTE = 6;

    // 9 * MAX_NUCLEOTIDES_PER_BYTE for address + 1 for parity nucleotide + 2 for S Nucleotides
    // + 24 for Primers + MAX_NUCLEOTIDES_PER_BYTE for at least one byte in payload
    const int MIN_STRAND_LENGTH = 27 + (10 * MAX_NUCLEOTIDES_PER_BYTE);

    const int MAX_PAYLOAD_INDEX_GAP = 10;
    const int MIN_BIGGER_PAYLOADS_AMOUNT = 10;

    const int MIN_XOR_SIZE = 2;
    const int MIN_XOR_STEP = 1;

    /**
     * Returns the maximum length of a strand measured in nucleotides.
     */
    int getMaxStrandLength();

    /**
     * Sets the maximum length of a strand measured in nucleotides to the given parameter.
     * @param length The new maximum length measured in nucleotides.
     */
    void setMaxStrandLength(int length);

    /**
     * Returns the amount of bytes a single payload contains.
     */
    int getPayloadByteLength();

    /**
     * Returns the amount of strands that that are used to create a single xor strand.
     */
    int getXorSize();

    /**
     * Sets the amount of strands that that are used to create a single xor strand to the given parameter.
     * @param size The new amount of strands.
     */
    void setXorSize(int size);

    /**
     * Returns the step size for the creation of the xor strands.
     * If the strand with index i is the first strand used to create a xor strand then the first strand for the next
     * xor strand will have index i + step size.
     */
    int getXorStep();

    /**
     * Sets the step size for the creation of the xor strands to the given parameter.
     * If the strand with index i is the first strand used to create a xor strand then the first strand for the next
     * xor strand will have index i + step size.
     * @param step The new step size.
     */
    void setXorStep(int step);

    /**
     * Calculates the amount of xor strands that will be created for a given amount of payload strands based on the
     * current size and step values.
     * @param strandsCount The amount of payload strands.
     * @return The calculated amount of xor strands.
     */
    uint64_t getXorStrandsCount(uint64_t strandsCount);

    /**
     * Calculates the address of the smallest xor strand that contains the given payloadAddress.
     * @param payloadAddress The address of the payload strand.
     * @return The calculated address.
     */
    uint64_t getSmallestContainingXorAddress(uint64_t payloadAddress);

}

#endif //XOR_CODE_SETTINGS_H
