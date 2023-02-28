#include "xor_code/settings.hpp"

namespace xor_code {

    int maxStrandLength = 111; // in nucleotides
    int payloadByteLength = 5; // in bytes

    int xorSize = 3; // the amount of strands involved in each xor
    int xorStep = 3; // the difference between the indices of the starting strands for each xor

    int getMaxStrandLength() {
        return maxStrandLength;
    }

    void setMaxStrandLength(int length) {
        if (length >= MIN_STRAND_LENGTH) {
            maxStrandLength = length;
            payloadByteLength = (length - MIN_STRAND_LENGTH + MAX_NUCLEOTIDES_PER_BYTE) / MAX_NUCLEOTIDES_PER_BYTE;
        }
    }

    int getPayloadByteLength() {
        return payloadByteLength;
    }

    int getXorSize() {
        return xorSize;
    }

    void setXorSize(int size) {
        if (size >= MIN_XOR_SIZE) {
            xorSize = size;
        }
    }

    int getXorStep() {
        return xorStep;
    }

    void setXorStep(int step) {
        if (step >= MIN_XOR_STEP) {
            xorStep = step;
        }
    }

    uint64_t getXorStrandsCount(uint64_t strandsCount) {
        auto size = getXorSize();
        auto step = getXorStep();

        // number of strands with step size 1
        uint64_t xorStrandsCount = strandsCount - (size - 1);

        // number of strands with correct step size
        return (xorStrandsCount / step) + (xorStrandsCount % step == 0 ? 0 : 1);
    }

    uint64_t getSmallestContainingXorAddress(uint64_t payloadAddress) {
        auto size = getXorSize();
        auto step = getXorStep();

        if (payloadAddress < size) {
            return 0;
        }
        uint64_t result = payloadAddress + 1 - size;
        if (result % step != 0) {
            result += step - (result % step);
        }
        return result;
    }

}
