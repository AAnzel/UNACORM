#include "xor_code/decode.hpp"
#include "xor_code/encode.hpp"
#include "xor_code/settings.hpp"
#include "xor_code/nucleotideUtils.hpp"
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <algorithm>

namespace xor_code {

    class StrandDecoder {

    private:

        std::string key;
        std::vector<types::nucleotides> strands;

        std::vector<types::nucleotides *> cleanedStrands;
        std::vector<strand *> decodedPayloadStrands;
        std::vector<strand *> decodedXorStrands;

        // the highest index of the strands in the map
        uint64_t highestPayloadIndex = 0;
        std::unordered_map<uint64_t, std::vector<strand *>> payloadStrandMap;
        std::unordered_map<uint64_t, std::vector<strand *>> xorStrandMap;

        /**
         * Filters the strands in strands.
         * Checks if a strand is inverted.
         * Checks if a strand is reversed.
         * Checks that the primers are correct.
         * Removes primers from all correct strands and adds them to cleanedStrands.
         */
        void filterStrands() {
            // create primers
            auto primerBegin = *getPrimer(key);
            auto primerEnd = types::nucleotides(NUCLEOTIDES_PER_PRIMER, 0);
            std::copy(primerBegin.begin(), primerBegin.end(), primerEnd.begin());
            invertNucleotides(primerEnd);
            auto revPrimerBegin = types::nucleotides(NUCLEOTIDES_PER_PRIMER, 0);
            std::reverse_copy(primerBegin.begin(), primerBegin.end(), revPrimerBegin.begin());
            // start filtering the strands
            for (auto strand: strands) {
                // check if strand is inverted
                if (strand[primerBegin.size()] == nuc_T) {
                    invertNucleotides(strand);
                } else if (strand[primerBegin.size()] != nuc_A) {
                    continue;
                }
                // check if strand is reversed
                if (std::equal(revPrimerBegin.begin(), revPrimerBegin.end(), strand.end() - revPrimerBegin.size())) {
                    std::reverse(strand.begin(), strand.end());
                }
                // check if primers are correct
                bool correct = true;
                auto itStart = strand.begin();
                for (auto c: primerBegin) {
                    correct = c == *itStart;
                    ++itStart;
                }
                ++itStart;
                auto itEnd = strand.end();
                for (int i = primerEnd.size() - 1; i >= 0; --i) {
                    --itEnd;
                    correct = primerEnd[i] == *itEnd;
                }
                --itEnd;
                if (correct) {
                    // remove primers and 'A' nucleotides
                    auto *cleaned = new types::nucleotides(itStart, itEnd);
                    cleanedStrands.push_back(cleaned);
                }
            }
        }

        /**
         * Tries to decode the addresses of each strand in cleanedStrands.
         * Turns the strands where decoding is possible into the strand struct and adds them to either
         * decodedXorStrands or decodedPayloadStrands.
         */
        void decodeStrands() {
            int addressLengthBytes = 9;
            int addressLength = addressLengthBytes * MAX_NUCLEOTIDES_PER_BYTE + 1;
            for (auto *strand: cleanedStrands) {
                // itBegin now points to the char right before the address
                auto itBegin = strand->end() - addressLength - 1;
                auto *cur = new xor_code::strand;
                uint8_t prev = *itBegin;
                ++itBegin; // itBegin now points to the first char of the address
                // check parity nucleotide
                auto itEnd = strand->end() - 1;
                auto parity = getParityNucleotide(itBegin, itEnd);
                if (parity != strand->back()) {
                    continue;
                }
                types::bytes address;
                itBegin = strand->end() - addressLength;
                itEnd = strand->end() - 1;
                convertNucleotidesToBinary(prev, itBegin, itEnd, addressLengthBytes, address);
                if (address.size() != addressLengthBytes) {
                    continue;
                }
                // get xor byte from address
                uint8_t isXor = address.at(0);
                if (isXor != 0 && isXor != 255) {
                    continue;
                }
                cur->isXor = isXor == 255;
                // get lowAddress from address
                for (int i = 0; i < 8; ++i) {
                    cur->lowAddressArray[i] = address.at(i + 1);
                }
                // extract payload from strand
                cur->payload.assign(strand->begin(), strand->end() - addressLength);
                if (cur->isXor) {
                    decodedXorStrands.push_back(cur);
                } else {
                    decodedPayloadStrands.push_back(cur);
                }
            }
        }

        /**
         * tries to find the highest payload address and make sure that there is no gap of missing
         * strands that is too high.
         * Removes all strands that have an address that is too high.
         * Puts the remaining strands into payloadStrandMap and xorStrandMap.
         */
        void filterStrandsBasedOnAddress() {
            // sort decodedPayloadStrands in ascending order by their lowAddress
            std::sort(decodedPayloadStrands.begin(), decodedPayloadStrands.end(), [](strand *s1, strand *s2) -> bool {
                return s1->lowAddress < s2->lowAddress;
            });
            // find the highest payload index
            auto prevIndex = decodedPayloadStrands.back()->lowAddress;
            int inARow = 0;
            for (auto i = decodedPayloadStrands.size(); i > 0 && inARow < MIN_BIGGER_PAYLOADS_AMOUNT; --i) {
                auto i1 = i - 1;
                auto *curStrand = decodedPayloadStrands[i1];
                if (curStrand->lowAddress + MAX_PAYLOAD_INDEX_GAP < prevIndex) {
                    inARow = 1; // already counting curStrand
                    // remove and delete strands with higher index than curStrand
                    for (auto j = decodedPayloadStrands.size() - 1; j > i1; --j) {
                        delete decodedPayloadStrands[j];
                    }
                    decodedPayloadStrands.resize(i);
                } else {
                    ++inARow;
                }
                prevIndex = curStrand->lowAddress;
            }
            highestPayloadIndex = decodedPayloadStrands.back()->lowAddress;
            // sort decodedXorStrands in ascending order by their lowAddress
            std::sort(decodedXorStrands.begin(), decodedXorStrands.end(), [](strand *s1, strand *s2) -> bool {
                return s1->lowAddress < s2->lowAddress;
            });
            // remove and delete xor strands with index that is too high
            // otherwise add them to xorStrandMap
            while (!decodedXorStrands.empty()) {
                auto *s = decodedXorStrands.back();
                if (s->lowAddress > highestPayloadIndex + MAX_PAYLOAD_INDEX_GAP) {
                    delete s;
                } else {
                    if (!xorStrandMap.contains(s->lowAddress)) {
                        xorStrandMap[s->lowAddress] = std::vector<strand *>();
                    }
                    xorStrandMap[s->lowAddress].push_back(s);
                }
                decodedXorStrands.pop_back();
            }
            // put remaining strands into data structures for next step
            for (auto *s: decodedPayloadStrands) {
                // [] implicitly adds new vector
                payloadStrandMap[s->lowAddress].push_back(s);
            }
        }

        /**
         * Sorts the strands in payloadStrandMap by their frequency and removes any duplicates.
         */
        void sortMapEntriesAndEliminateDuplicates() {
            struct PointedVectorEq {
                bool operator()(strand const *l, strand const *r) const {
                    return l->payload == r->payload;
                }
            };
            struct PointedVectorHash {
                size_t operator()(strand const *s) const {
                    // https://stackoverflow.com/questions/20511347/a-good-hash-function-for-a-vector
                    auto vec = s->payload;
                    std::size_t seed = vec.size();
                    for (auto x: vec) {
                        x = ((x >> 16) ^ x) * 0x45d9f3b;
                        x = ((x >> 16) ^ x) * 0x45d9f3b;
                        x = (x >> 16) ^ x;
                        seed ^= x + 0x9e3779b9 + (seed << 6) + (seed >> 2);
                    }
                    return seed;
                }
            };
            // put all strands with the current key into a set and a multiset
            // two strands are only equal if their payloads are equal
            auto multiSet = std::unordered_multiset<strand *, PointedVectorHash, PointedVectorEq>();
            auto set = std::unordered_set<strand *, PointedVectorHash, PointedVectorEq>();
            for (auto &entry: payloadStrandMap) {
                multiSet.insert(entry.second.begin(), entry.second.end());
                set.insert(entry.second.begin(), entry.second.end());
                // insert all unique strands into the vector
                entry.second.clear();
                entry.second.insert(entry.second.begin(), set.begin(), set.end());
                // sort vector in descending order based on how often each strand appears in the multiset
                std::sort(entry.second.begin(), entry.second.end(), [&multiSet](const auto &lhs, const auto &rhs) {
                    return multiSet.count(lhs) > multiSet.count(rhs);
                });
                multiSet.clear();
                set.clear();
            }
            for (auto &entry: xorStrandMap) {
                multiSet.insert(entry.second.begin(), entry.second.end());
                set.insert(entry.second.begin(), entry.second.end());
                // insert all unique strands into the vector
                entry.second.clear();
                entry.second.insert(entry.second.begin(), set.begin(), set.end());
                // sort vector in descending order based on how often each strand appears in the multiset
                std::sort(entry.second.begin(), entry.second.end(), [&multiSet](const auto &lhs, const auto &rhs) {
                    return multiSet.count(lhs) > multiSet.count(rhs);
                });
                multiSet.clear();
                set.clear();
            }
        }

        /**
         * Deletes all strands in the payloadStrandMap entry of strandIndex except for keepStrand.
         */
        void deleteOtherStrands(strand *keepStrand, uint64_t strandIndex) {
            for (auto *otherStrand: payloadStrandMap[strandIndex]) {
                if (otherStrand != keepStrand) {
                    delete otherStrand;
                }
            }
            payloadStrandMap[strandIndex].clear();
            payloadStrandMap[strandIndex].push_back(keepStrand);
        }

        /**
         * Fills incorrectStrands with all strand indices that are not currently in correctStrands.
         */
        void determineIncorrectAndMissingStrands(std::unordered_set<uint64_t> &correctStrands,
                                                 std::queue<uint64_t> &incorrectStrands) const {
            for (uint64_t strandIndex = 0; strandIndex < highestPayloadIndex; strandIndex++) {
                if (!correctStrands.contains(strandIndex)) {
                    incorrectStrands.push(strandIndex);
                }
            }
        }

        /**
         * Checks if correctStrands contains all necessary strands to restore a strand that is part of an
         * xor that goes from the start index to the end index.
         */
        bool canBeRestored(uint64_t start, uint64_t end, std::unordered_set<uint64_t> &correctStrands) {
            // no strand can be restored without the xor strand
            if (!xorStrandMap.contains(start)) {
                return false;
            }

            uint32_t missingStrandsCount = 0;
            for (auto j = start; j < end; j++) {
                if (!correctStrands.contains(j)) {

                    // only one strand can be restored using the xor strand
                    if (missingStrandsCount == 1) {
                        return false;
                    }

                    missingStrandsCount++;
                }
            }

            return true;
        }

        /**
         * Restores the strand with index restoreIndex using all strands from the start index to the end index.
         */
        void restoreStrand(uint64_t start, uint64_t end, uint64_t restoreIndex) {
            auto size = getXorSize();
            auto *xorStrand = xorStrandMap[start].front();


            auto *curPayloads = new types::nucleotides*[size];
            curPayloads[0] = &(xorStrand->payload);
            int i = 1;
            for (auto strandIndex = start; strandIndex < end; ++strandIndex) {
                if (strandIndex == restoreIndex) continue;
                curPayloads[i] = &(payloadStrandMap[strandIndex].front()->payload);
                i++;
            }
            auto restoredPayload = getXorPayload(curPayloads, size);

            delete[] curPayloads;

            auto *restoredStrand = new strand();
            restoredStrand->payload = restoredPayload;
            restoredStrand->isXor = false;
            restoredStrand->lowAddress = restoreIndex;
            restoredStrand->primerBegin = xorStrand->primerBegin;
            restoredStrand->primerEnd = xorStrand->primerEnd;
            payloadStrandMap[restoreIndex].push_back(restoredStrand);

            // remove all incorrect strands from the payloadStrandMap
            deleteOtherStrands(restoredStrand, restoreIndex);
        }

        /**
         * Goes through all strands in incorrectStrands and restores them using the xor strands if possible.
         */
        void restoreIncorrectAndMissingStrands(std::unordered_set<uint64_t> &correctStrands,
                                               std::queue<uint64_t> &incorrectStrands,
                                               uint64_t xorStrandsCount) {
            auto size = getXorSize();
            auto step = getXorStep();

            uint64_t lastCount = 0;
            while (lastCount != incorrectStrands.size()) { // repeat until no incorrect strand can be restored/exists
                lastCount = incorrectStrands.size();

                // go through all strands in the queue exactly once
                for (uint64_t lookedAt = 0; lookedAt < incorrectStrands.size(); lookedAt++) {
                    auto restoreIndex = incorrectStrands.front();
                    incorrectStrands.pop();

                    if (correctStrands.contains(restoreIndex)) {
                        continue;
                    }

                    // restore strand if possible
                    bool isRestored = false;
                    auto smallestXorIndex = getSmallestContainingXorAddress(restoreIndex);
                    for (auto start = smallestXorIndex; start <= restoreIndex; start += step) {
                        auto end = start + size; // exclusive

                        if (canBeRestored(start, end, correctStrands)) {
                            // found fitting xor batch
                            restoreStrand(start, end, restoreIndex);
                            correctStrands.insert(restoreIndex);
                            isRestored = true;
                            break;
                        }
                    }
                    if (isRestored) {
                        // check all possibilities for all xor strands, this strand is involved with
                        std::queue<uint64_t> checkNext;
                        for (auto start2 = smallestXorIndex; start2 <= restoreIndex; start2 += step) {
                            checkNext.push(start2);
                        }
                        while (!checkNext.empty()) {
                            auto curXor = checkNext.front();
                            checkNext.pop();
                            checkAllPossibilities(curXor, correctStrands, checkNext);
                        }
                        break;
                    } else {
                        incorrectStrands.push(restoreIndex);
                    }
                }
            }
        }

        /**
         * Chooses for each strand in incorrectStrands the first strand in payloadStrandMap and deletes all the others.
         * Then adds that strand to correctStrands. If a strand has no entries in payloadStrandMap it is kept
         * in incorrectStrands.
         */
        void chooseFromAvailableStrands(std::unordered_set<uint64_t> &correctStrands,
                                        std::queue<uint64_t> &incorrectStrands) {
            // go through all strands in the queue exactly once
            auto incorrectCount = incorrectStrands.size(); // can't inline as size changes
            for (uint64_t lookedAt = 0; lookedAt < incorrectCount; lookedAt++) {
                auto restoreIndex = incorrectStrands.front();
                incorrectStrands.pop();

                if (payloadStrandMap[restoreIndex].empty()) {
                    incorrectStrands.push(restoreIndex);
                    continue;
                }

                auto *chosenStrand = payloadStrandMap[restoreIndex].front();

                // remove all incorrect strands from the payloadStrandMap
                deleteOtherStrands(chosenStrand, restoreIndex);
                correctStrands.insert(restoreIndex);
            }
        }

        /**
         * Generates a random payload for all remaining strands in incorrectStrands and adds them to correctStrands.
         */
        void generateRandomStrands(std::unordered_set<uint64_t> &correctStrands,
                                   std::queue<uint64_t> &incorrectStrands) {
            if (incorrectStrands.empty()) {
                return;
            }

            // go through all strands in the queue exactly once
            while (!incorrectStrands.empty()) {
                auto restoreIndex = incorrectStrands.front();
                incorrectStrands.pop();

                auto *restoredStrand = new strand();
                restoredStrand->payload = generateRandomPayload(getMaxStrandLength());
                restoredStrand->isXor = false;
                restoredStrand->lowAddress = restoreIndex;
                restoredStrand->primerBegin = nullptr;
                restoredStrand->primerEnd = nullptr;
                payloadStrandMap[restoreIndex].push_back(restoredStrand);

                correctStrands.insert(restoreIndex);
            }
        }

        /**
         * Goes through all combinations of strands that are covered by the given xorIndex and checks if they form the
         * correct xor strand.
         */
        void checkAllPossibilities(uint64_t xorIndex, std::unordered_set<uint64_t> &correctStrands,
                                   std::queue<uint64_t> &checkNext) {
            auto size = getXorSize();
            auto step = getXorStep();
            if (!xorStrandMap.contains(xorIndex) || xorStrandMap[xorIndex].empty() ||
                xorIndex + size - 1 > highestPayloadIndex) {
                return;
            }
            auto payloadIterators = std::vector<std::vector<strand *>::iterator>();
            payloadIterators.resize(size);
            auto *curPayloads = new types::nucleotides*[size];
            for (auto *curXorStrand: xorStrandMap[xorIndex]) {
                // initialize iterators for every payload index
                for (int i = 0; i < size; ++i) {
                    if (!payloadStrandMap[xorIndex + i].empty()) {
                        payloadIterators[i] = payloadStrandMap[xorIndex + i].begin();
                    } else {
                        return;
                    }
                }
                // iterate over all combinations of payloads and check if they create the correct xor payload
                int nextIncrease = size - 1;
                while (nextIncrease >= 0) {
                    // check current payloads
                    for (int i = 0; i < size; ++i) {
                        curPayloads[i] = &((*payloadIterators[i])->payload);
                    }
                    auto newXorPayload = getXorPayload(curPayloads, size);
                    if (newXorPayload.size() == curXorStrand->payload.size()
                        && std::equal(newXorPayload.begin(), newXorPayload.end(), curXorStrand->payload.begin())) {
                        // the calculated xor payload is correct
                        // add current strands to correct strands
                        for (int i = 0; i < size; ++i) {
                            auto *curStrand = *payloadIterators[i];
                            if (!correctStrands.contains(curStrand->lowAddress)) {
                                correctStrands.insert(curStrand->lowAddress);

                                // remove all incorrect strands from the payloadStrandMap
                                deleteOtherStrands(curStrand, xorIndex + i);

                                // recursively call this function for all other xorStrands that involve this strand
                                auto smallestXorIndex = getSmallestContainingXorAddress(curStrand->lowAddress);
                                for (auto j = smallestXorIndex; j <= curStrand->lowAddress; j += step) {
                                    if (j >= 0 && j + size > curStrand->lowAddress && j != xorIndex) {
                                        checkNext.push(j);
                                        break;
                                    }
                                }
                            }
                        }
                        // delete all xorStrands with xorIndex
                        for (auto *xorToDelete: xorStrandMap[xorIndex]) {
                            delete xorToDelete;
                        }
                        xorStrandMap[xorIndex].clear();
                        delete[] curPayloads;
                        return;
                    }

                    // update iterators so that they point to the next combination of payloads
                    while (nextIncrease >= 0) {
                        payloadIterators[nextIncrease]++;
                        if (payloadIterators[nextIncrease] == payloadStrandMap[xorIndex + nextIncrease].end()) {
                            payloadIterators[nextIncrease] = payloadStrandMap[size + nextIncrease].begin();
                            nextIncrease--;
                        } else {
                            nextIncrease = size - 1;
                            break;
                        }
                    }
                }
            }
            delete[] curPayloads;
        }

        /**
         * Validates existing strands and attempts to correct possible mutations as well as restore lost strands
         * 1. Check all possibilities when searching for correct strands.
         * 2. Recreate missing strands.
         *  2.1 If a missing strand has been recreated and the xors overlap check all possibilities for the other
         *      xors involving this strand again.
         * 3. If a strand cant be recreated but a strand with that address is available then just use that strands
         *    payload
         * 4. If even that fails just choose random bytes.
         */
        void checkAndRestore() {
            auto step = getXorStep();
            auto xorStrandsCount = getXorStrandsCount(highestPayloadIndex + 1);
            if (xorStrandMap.size() > xorStrandsCount) {
                xorStrandsCount = xorStrandMap.size();
            }

            std::unordered_set<uint64_t> correctStrands{};

            // first check for correct strands
            std::queue<uint64_t> checkNext;
            for (uint64_t xorIndex = 0; xorIndex < xorStrandsCount * step; xorIndex += step) {
                checkNext.push(xorIndex);
            }
            while (!checkNext.empty()) {
                auto curXor = checkNext.front();
                checkNext.pop();
                checkAllPossibilities(curXor, correctStrands, checkNext);
            }

            // find incorrect/missing strands
            std::queue<uint64_t> incorrectStrands{};
            determineIncorrectAndMissingStrands(correctStrands, incorrectStrands);

            // restore incorrect/missing strands using correct strands and xor strands (not correct if the xor strands have problems)
            restoreIncorrectAndMissingStrands(correctStrands, incorrectStrands, xorStrandsCount);

            // choose available strand (probably not correct)
            chooseFromAvailableStrands(correctStrands, incorrectStrands);

            // restore incorrect/missing strands using correct strands, available strands and xor strands (not correct if the available or the xor strands have problems)
            restoreIncorrectAndMissingStrands(correctStrands, incorrectStrands, xorStrandsCount);

            // generate random strand (most likely not correct)
            generateRandomStrands(correctStrands, incorrectStrands);
        }

        /**
         * Converts the payloads to binary and stores the resulting bytes in a vector.
         */
        types::bytes assemble() {
            types::bytes result;

            for (int i = 0; i <= highestPayloadIndex; ++i) {
                // decode and append payload
                auto payload = payloadStrandMap[i].front()->payload;
                convertNucleotidesToBinary(nuc_A, payload.begin(), payload.end(), getPayloadByteLength(), result);
            }
            return result;
        }

    public:

        StrandDecoder(std::string &key, std::vector<types::nucleotides> &strands) {
            this->key = key;
            this->strands = strands;
        }

        ~StrandDecoder() {
            for (auto *strand: cleanedStrands) {
                delete strand;
            }
        }

        types::bytes decode() {
            filterStrands();
            decodeStrands();
            filterStrandsBasedOnAddress();
            sortMapEntriesAndEliminateDuplicates();
            checkAndRestore();
            return assemble();
        }

    };

    types::bytes decode(std::string key, std::vector<types::nucleotides> &strands) {
        auto decoder = StrandDecoder(key, strands);
        return decoder.decode();
    }
}
