#ifndef XOR_CODE_NUCLEOTIDES_H
#define XOR_CODE_NUCLEOTIDES_H

#include <list>
#include <cstdint>
#include <string>
#include <memory>
#include "settings.hpp"

namespace xor_code {

    extern const uint8_t nuc_A;
    extern const uint8_t nuc_C;
    extern const uint8_t nuc_G;
    extern const uint8_t nuc_T;
    extern const uint8_t min_nuc;
    extern const uint8_t max_nuc;

    /**
     * Returns whether the given integer is a correct integer representation of a nucleotide.
     *
     * @param nucleotide the integer to be checked.
     * @return True if the given integer is one of 0, 1, 2, 3. False otherwise.
     */
    bool isNucleotide(uint8_t nucleotide);

    /**
     * Returns the char representation of the given nucleotide. The mapping works like this:
     * 0 -> 'A', 1 -> 'C', 2 -> 'G', 3 -> 'T'.
     * This is the exact inverse function to getIntegerNucleotide().
     *
     * @param nucleotide An integer representation of a nucleotide.
     * @return The matching char representation of the nucleotide.
     */
    char getCharNucleotide(uint8_t nucleotide);

    /**
     * Returns the integer representation of the given nucleotide. The mapping works like this:
     * 'A' -> 0, 'C' -> 1, 'G' -> 2, 'T' -> 3.
     * This is the exact inverse function to getCharNucleotide().
     *
     * @param nucleotide A char representation of a nucleotide.
     * @return The matching integer representation of the nucleotide.
     */
    uint8_t getIntegerNucleotide(char nucleotide);

    /**
     * Inverts every nucleotide in the given sequence according to the following pairs:
     * ('A', 'T'), ('C', 'G').
     * For example the sequence "ACTAG" would be turned into "TGATC".
     *
     * @param seq The sequence that should be inverted.
     */
    void invertNucleotides(types::nucleotides &seq);

    /**
     * Performs an xor operation on the given nucleotides.
     *
     * @param nucleotide1 An integer representation of the first nucleotide.
     * @param nucleotide2 An integer representation of the second nucleotide.
     * @return An integer representation of the nucleotide that is the result of the xor operation.
     */
    uint8_t getXorNucleotide(uint8_t nucleotide1, uint8_t nucleotide2);

    /**
     * Calculates a parity nucleotide for the sequence starting at 'itBegin' (inclusive) and ending at
     * 'itEnd' (exclusive).
     *
     * @param itBegin A Random Access Iterator pointing at the start of the sequence (inclusive).
     * @param itEnd A Random Access Iterator pointing at the end of the sequence (exclusive).
     * @return An integer representation of the calculated parity nucleotide.
     */
    uint8_t getParityNucleotide(types::iter itBegin, types::iter itEnd);

    /**
     * Calculates and returns the primerBegin associated with the given key. The returned primerBegin will always have a
     * length of 12 nucleotides.
     * IMPORTANT: It is possible that two different keys will be associated with the same primerBegin.
     *
     * @param key a normal string.
     * @return A pointer to the calculated primerBegin as a sequence of nucleotides.
     */
    types::nucleotides *getPrimer(const std::string &key);

    /**
     * Generates a random nucleotide sequence with the given length.
     * @param length The length of the resulting sequence.
     * @return The generated nucleotide sequence.
     */
    types::nucleotides generateRandomPayload(uint64_t length);

    /**
     * Calculates the sequence of nucleotides that is the result of doing an xor operation between all the given
     * payload strands. The length of the result will be the length of the longest given payload strand.
     * @param payloads An array of pointers pointing at a sequence of nucleotides.
     * @param size The size of the given array.
     * @return The calculated xor sequence.
     */
    types::nucleotides getXorPayload(types::nucleotides *payloads[], int size);

    /**
     * Encodes the given sequence of bytes into a sequence of nucleotides. The nucleotides are appended to the
     * end of 'out'.
     * The encoding works by first turning each byte into a sequence of 5 or 6 ternary digits using a prefix encoding.
     * Then each ternary digit is turned into a nucleotide based on a rotary encoding that makes sure that no
     * nucleotide appears twice in a row. For this the given nucleotide 'prev' is assumed to be the nucleotide that
     * appears immediately before the newly encoded sequence.
     * The parameter 'extraBytes' says how bytes worth of padding nucleotides should be added to the end of the
     * sequence. These extra bytes will be ignored when this same sequence of nucleotides is decoded to a sequence
     * of bytes using convertNucleotidesToBinary().
     * This is the exact inverse function to convertNucleotidesToBinary().
     *
     * @param prev An integer representation of a nucleotide.
     * @param buffer A sequence of bytes.
     * @param extraBytes An integer representing how many extra bytes should be added.
     * @param out A sequence of nucleotides. The result of this function will be appended to the end of this sequence.
     */
    void convertBinaryToNucleotides(uint8_t prev, types::bytes &buffer, uint8_t extraBytes, types::nucleotides &out);

    /**
     * Decodes the given sequence of nucleotides into a sequence of bytes. The bytes are appended to the
     * end of 'out'.
     * The decoding works by first turning each nucleotide into a ternary digit based on a rotating encoding. For this
     * the given nucleotide 'prev' is assumed to be the nucleotide that appears immediately before the given sequence.
     * Then every 5 or 6 ternary digits are turned into a byte using a prefix encoding.
     * The decoding will stop if the end of the given sequence of nucleotides is reached or when 'numOfBytes' many
     * bytes have been decoded.
     * This is the exact inverse function to convertBinaryToNucleotides().
     *
     * @param prev An integer representation of a nucleotide.
     * @param itBegin A Random Access Iterator pointing at the start of the sequence of nucleotides (inclusive).
     * @param itEnd A Random Access Iterator pointing at the end of the sequence of nucleotides (exclusive).
     * @param numOfBytes The maximum number of bytes that should be decoded.
     * @param out A sequence of bytes. The result of this function will be appended to the end of this sequence.
     */
    void convertNucleotidesToBinary(uint8_t prev, types::iter itBegin, types::iter itEnd, uint32_t numOfBytes,
                                    types::bytes &out);

}

#endif //XOR_CODE_NUCLEOTIDES_H
