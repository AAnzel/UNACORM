#include "xor_code/encode.hpp"
#include "xor_code/nucleotideUtils.hpp"
#include "xor_code/settings.hpp"
#include <iostream>

namespace xor_code {

    class Encoder {

    private:

        std::string key;
        types::bytes *inputBytes;

        std::vector<strand *> *strands = new std::vector<strand *>;

    public:

        Encoder(const std::string &key, types::bytes &bytes) {
            this->key = key;
            inputBytes = &bytes;
        }

        ~Encoder() {
            for (strand *s: *strands) {
                delete s;
            }
            delete strands;
        }

        void createPayloadStrands() {
            // create primers
            auto *primerBegin = getPrimer(key);
            auto *primerEnd = new types::nucleotides(NUCLEOTIDES_PER_PRIMER, 0);
            std::copy(primerBegin->begin(), primerBegin->end(), primerEnd->begin());
            invertNucleotides(*primerEnd);
            // start creating the strands
            auto length = getPayloadByteLength();
            uint64_t index = 0;
            int i = 0;
            while (i < inputBytes->size()) {
                // create and encode the payload
                types::bytes payload;
                for (int j = 0; j < length && i < inputBytes->size(); ++j) {
                    payload.push_back(inputBytes->at(i));
                    ++i;
                }
                auto *newStrand = new strand();
                convertBinaryToNucleotides(nuc_A, payload, length - payload.size(), newStrand->payload);
                // set all the other fields
                newStrand->isXor = false;
                newStrand->lowAddress = index++;
                newStrand->primerBegin = primerBegin;
                newStrand->primerEnd = primerEnd;
                strands->push_back(newStrand);
            }
        }

        void createXorStrands() {
            auto size = getXorSize();
            auto step = getXorStep();
            auto xorStrandsCount = getXorStrandsCount(strands->size());
            auto *curPayloads = new types::nucleotides*[size];; // space for the strands to be used to create a Xor strand

            for (uint64_t i = 0; i < xorStrandsCount; i++) {
                auto start = i * step; // inclusive
                auto end = start + size; // exclusive

                // create xor strand with address start
                auto *newStrand = new strand();
                newStrand->isXor = true;
                newStrand->lowAddress = start;
                newStrand->primerBegin = strands->at(start)->primerBegin;
                newStrand->primerEnd = strands->at(start)->primerEnd;

                // create xor payload
                uint64_t payloadIndex = 0;
                for (uint64_t strandIndex = start; strandIndex < end; strandIndex++) {
                    curPayloads[payloadIndex++] = &strands->at(strandIndex)->payload;
                }
                newStrand->payload = getXorPayload(curPayloads, size);

                strands->push_back(newStrand);
            }
            delete[] curPayloads;
        }

        std::vector<types::nucleotides> assembleStrands() {
            std::vector<types::nucleotides> output;
            for (strand *s: *strands) {
                types::nucleotides result;
                // add primerBegin
                result.insert(result.end(), s->primerBegin->begin(), s->primerBegin->end());
                // add S nucleotide for detecting if strand is inverted
                result.push_back(nuc_A);
                // add payload nucleotides
                for (uint8_t c: s->payload) {
                    result.push_back(c);
                }
                // add address
                types::bytes address;
                if (s->isXor) {
                    address.push_back(255);
                } else {
                    address.push_back(0);
                }
                for (int i = 0; i < 8; ++i) {
                    address.push_back(s->lowAddressArray[i]);
                }
                auto prevSize = result.size();
                convertBinaryToNucleotides(result.back(), address, 0, result);
                // pad address to always have a length of 9 * MAX_NUCLEOTIDES_PER_BYTE
                auto remaining = (9 * MAX_NUCLEOTIDES_PER_BYTE) - (result.size() - prevSize);
                uint8_t next = nuc_C;
                if (result.back() == nuc_C) {
                    next = nuc_T;
                }
                for (int i = 0; i < remaining; ++i) {
                    result.push_back(next);
                    if (next == nuc_C) {
                        next = nuc_T;
                    } else {
                        next = nuc_C;
                    }
                }
                // add parity nucleotide
                auto parityPointerBegin = result.end() - (9 * MAX_NUCLEOTIDES_PER_BYTE);
                result.push_back(getParityNucleotide(parityPointerBegin, result.end()));
                // add another S nucleotide
                result.push_back(nuc_A);
                // add inverted primerBegin
                result.insert(result.end(), s->primerEnd->begin(), s->primerEnd->end());
                output.push_back(result);
            }
            return output;
        }

    };

    std::vector<types::nucleotides> encode(const std::string &key, types::bytes &bytes) {
        auto encoder = Encoder(key, bytes);
        encoder.createPayloadStrands();
        encoder.createXorStrands();
        return encoder.assembleStrands();
    }

    std::vector<types::nucleotides> encode(const std::string &key, std::istream &input) {
        types::bytes bytes;
        while (!input.eof()) {
            auto cur = input.get();
            if (!input.eof()) {
                bytes.push_back(cur);
            }
        }
        return encode(key, bytes);
    }

    std::vector<types::nucleotides> encode(const std::string &filePath) {
        std::ifstream input(filePath, std::ios::binary);
        if (!input.is_open()) {
            std::cout << "Unable to open file!\n";
            return {};
        }
        std::string key = filePath.substr(filePath.find_last_of("/\\") + 1);
        auto strands = encode(key, input);
        input.close();
        return strands;
    }
}
