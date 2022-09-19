#include "xor_code/nucleotideUtils.hpp"
#include "xor_code/huffmanCode.hpp"
#include "xor_code/settings.hpp"

#include <cstdint>
#include <random>

namespace xor_code {

    const uint8_t nuc_A = 0;
    const uint8_t nuc_C = 1;
    const uint8_t nuc_G = 2;
    const uint8_t nuc_T = 3;
    const uint8_t min_nuc = nuc_A;
    const uint8_t max_nuc = nuc_T;

    const char charRepresentations[] = {'A', 'C', 'G', 'T'};
    const int primes[NUCLEOTIDES_PER_PRIMER] = {2, 3, 5, 7, 11, 13,
                                                17, 19, 23, 29, 31, 37};
    const std::hash<std::string> hasher;

    bool isNucleotide(uint8_t nucleotide) {
        return nucleotide <= 3;
    }

    char getCharNucleotide(uint8_t nucleotide) {
        return charRepresentations[nucleotide % 4];
    }

    uint8_t getIntegerNucleotide(char nucleotide) {
        switch (nucleotide) {
            case 'A':
                return nuc_A;
            case 'C':
                return nuc_C;
            case 'G':
                return nuc_G;
            case 'T':
                return nuc_T;
            default:
                return nuc_A;
        }
    }

    void invertNucleotides(types::nucleotides &seq) {
        uint8_t mask = 3; // preserve only the 2 lowest bits
        for (uint8_t &nucleotide: seq) {
            nucleotide = ~nucleotide & mask;
        }
    }

    uint8_t getXorNucleotide(uint8_t nucleotide1, uint8_t nucleotide2) {
        return nucleotide1 ^ nucleotide2;
    }

    uint8_t getParityNucleotide(types::iter itBegin, types::iter itEnd) {
        uint8_t sum = 0;
        while (itBegin < itEnd) {
            sum = (sum + *itBegin) % 4;
            ++itBegin;
        }
        return sum % 4;
    }

    types::nucleotides *getPrimer(const std::string &key) {
        auto hash = hasher(key);
        auto *primer = new types::nucleotides(NUCLEOTIDES_PER_PRIMER);
        for (int i = 0; i < NUCLEOTIDES_PER_PRIMER; ++i) {
            primer->at(i) = (hash / primes[i]) % max_nuc;
        }
        return primer;
    }

    types::nucleotides generateRandomPayload(uint64_t length) {
        // initialize RNG (Random Nucleotide Generator)
        std::random_device rd;
        std::mt19937 rng(rd()); // https://www.pcg-random.org
        std::uniform_int_distribution<int> dist(min_nuc, max_nuc);

        auto randomPayload = types::nucleotides(length, nuc_A);

        for (uint8_t &nuc: randomPayload) {
            nuc = dist(rng);
        }
        return randomPayload;
    }

    types::nucleotides getXorPayload(types::nucleotides *payloads[], int size) {
        // find maximum length of the payloads
        uint64_t maxLength = 0;
        for (int i = 0; i < size; ++i) {
            if (payloads[i]->size() > maxLength) {
                maxLength = payloads[i]->size();
            }
        }
        // do xor one by one
        auto xorPayload = types::nucleotides(maxLength, nuc_A);
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < payloads[i]->size(); ++j) {
                xorPayload[j] = getXorNucleotide(xorPayload[j], payloads[i]->at(j));
            }
        }
        return xorPayload;
    }

    void convertBinaryToNucleotides(uint8_t prev, types::bytes &buffer, uint8_t extraBytes, types::nucleotides &out) {
        auto curPrev = prev;
        auto *encoder = HuffmanCode::getInstance();
        for (uint8_t byte: buffer) {
            // encode byte as base 3
            for (uint8_t c: encoder->encodeToTernaries(byte)) {
                // convert base 3 digit c into nucleotide
                uint8_t prevIndex = curPrev + 1;
                prevIndex += c;
                prevIndex %= 4;
                curPrev = prevIndex;
                out.push_back(curPrev);
            }
        }
        // add nucleotides for the extra bytes to out
        for (int i = 0; i < extraBytes; ++i) {
            // encode byte as base 3
            for (uint8_t c: encoder->getExtraTernaries()) {
                // convert base 3 digit c into nucleotide
                uint8_t prevIndex = curPrev + 1;
                prevIndex += c;
                prevIndex %= 4;
                curPrev = prevIndex;
                out.push_back(curPrev);
            }
        }
    }

    void convertNucleotidesToBinary(uint8_t prev, types::iter itBegin, types::iter itEnd, uint32_t numOfBytes,
                                    types::bytes &out) {
        // decode to base 3
        types::ternaries base3;
        auto curPrev = prev;
        while (itBegin != itEnd) {
            uint8_t t = *itBegin;
            uint8_t prevIndex = curPrev;
            uint8_t curIndex = t;
            if (curIndex <= prevIndex) {
                curIndex += 4;
            }
            base3.push_back(curIndex - (prevIndex + 1));
            curPrev = t;
            ++itBegin;
        }
        // decode to binary
        auto *decoder = HuffmanCode::getInstance();
        int bytesRead = 0;
        auto itBeginBase3 = base3.begin();
        auto itEndBase3 = base3.end();
        while (itBeginBase3 != itEndBase3 && bytesRead < numOfBytes) {
            decoder->decodeToByte(itBeginBase3, itEndBase3, out);
            ++bytesRead;
        }
    }
}
