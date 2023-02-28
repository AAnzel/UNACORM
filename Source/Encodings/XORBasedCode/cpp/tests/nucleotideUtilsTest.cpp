#include "gtest/gtest.h"
#include "xor_code/nucleotideUtils.hpp"

using namespace xor_code;

TEST(NucleotideUtilsTest, Nucleotides) {
    ASSERT_EQ(0, nuc_A);
    ASSERT_EQ(1, nuc_C);
    ASSERT_EQ(2, nuc_G);
    ASSERT_EQ(3, nuc_T);
    ASSERT_EQ(nuc_A, min_nuc);
    ASSERT_EQ(nuc_T, max_nuc);
}

TEST(NucleotideUtilsTest, IsNucleotide) {
    ASSERT_EQ(true, isNucleotide(nuc_A));
    ASSERT_EQ(true, isNucleotide(nuc_C));
    ASSERT_EQ(true, isNucleotide(nuc_G));
    ASSERT_EQ(true, isNucleotide(nuc_T));

    ASSERT_EQ(false, isNucleotide(255));
    ASSERT_EQ(false, isNucleotide(4));
    ASSERT_EQ(false, isNucleotide(10));
    ASSERT_EQ(false, isNucleotide(27));
    ASSERT_EQ(false, isNucleotide(100));
    ASSERT_EQ(false, isNucleotide(111));
    ASSERT_EQ(false, isNucleotide(125));
    ASSERT_EQ(false, isNucleotide(200));
}

TEST(NucleotideUtilsTest, GetCharNucleotide) {
    ASSERT_EQ('A', getCharNucleotide(nuc_A));
    ASSERT_EQ('C', getCharNucleotide(nuc_C));
    ASSERT_EQ('G', getCharNucleotide(nuc_G));
    ASSERT_EQ('T', getCharNucleotide(nuc_T));

    ASSERT_EQ('T', getCharNucleotide(255));
    ASSERT_EQ('A', getCharNucleotide(4));
    ASSERT_EQ('G', getCharNucleotide(10));
    ASSERT_EQ('T', getCharNucleotide(27));
    ASSERT_EQ('A', getCharNucleotide(100));
    ASSERT_EQ('T', getCharNucleotide(111));
    ASSERT_EQ('C', getCharNucleotide(125));
    ASSERT_EQ('A', getCharNucleotide(200));
}

TEST(NucleotideUtilsTest, GetIntegerNucleotide) {
    ASSERT_EQ(nuc_A, getIntegerNucleotide('A'));
    ASSERT_EQ(nuc_C, getIntegerNucleotide('C'));
    ASSERT_EQ(nuc_G, getIntegerNucleotide('G'));
    ASSERT_EQ(nuc_T, getIntegerNucleotide('T'));


    ASSERT_EQ(nuc_A, getIntegerNucleotide('B'));
    ASSERT_EQ(nuc_A, getIntegerNucleotide('D'));
    ASSERT_EQ(nuc_A, getIntegerNucleotide('J'));
    ASSERT_EQ(nuc_A, getIntegerNucleotide('Z'));
}

TEST(NucleotideUtilsTest, InvertNucleotides) {
    types::nucleotides strand1{nuc_A, nuc_C, nuc_G, nuc_T};
    types::nucleotides inverted1{nuc_T, nuc_G, nuc_C, nuc_A};
    ASSERT_NE(inverted1, strand1);
    invertNucleotides(strand1);
    ASSERT_EQ(inverted1, strand1);

    types::nucleotides strand2{nuc_A, nuc_A, nuc_T, nuc_C, nuc_G, nuc_T, nuc_G};
    types::nucleotides inverted2{nuc_T, nuc_T, nuc_A, nuc_G, nuc_C, nuc_A, nuc_C};
    ASSERT_NE(inverted2, strand2);
    invertNucleotides(strand2);
    ASSERT_EQ(inverted2, strand2);
}

TEST(NucleotideUtilsTest, GetXorNucleotide) {
    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_A, nuc_A));
    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_A, nuc_C));
    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_A, nuc_G));
    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_A, nuc_T));

    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_A, nuc_A));
    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_C, nuc_A));
    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_G, nuc_A));
    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_T, nuc_A));


    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_C, nuc_A));
    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_C, nuc_C));
    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_C, nuc_G));
    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_C, nuc_T));

    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_A, nuc_C));
    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_C, nuc_C));
    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_G, nuc_C));
    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_T, nuc_C));


    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_G, nuc_A));
    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_G, nuc_C));
    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_G, nuc_G));
    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_G, nuc_T));

    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_A, nuc_G));
    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_C, nuc_G));
    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_G, nuc_G));
    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_T, nuc_G));


    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_T, nuc_A));
    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_T, nuc_C));
    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_T, nuc_G));
    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_T, nuc_T));

    ASSERT_EQ(nuc_T, getXorNucleotide(nuc_A, nuc_T));
    ASSERT_EQ(nuc_G, getXorNucleotide(nuc_C, nuc_T));
    ASSERT_EQ(nuc_C, getXorNucleotide(nuc_G, nuc_T));
    ASSERT_EQ(nuc_A, getXorNucleotide(nuc_T, nuc_T));
}


TEST(NucleotideUtilsTest, GetParityNucleotide) {
    types::nucleotides strand{nuc_C, nuc_A, nuc_G, nuc_T, nuc_A, nuc_C};

    auto begin1 = strand.begin();
    auto end1 = strand.end();
    ASSERT_EQ(3, getParityNucleotide(begin1, end1));

    auto begin2 = strand.begin() + 1;
    ASSERT_EQ(2, getParityNucleotide(begin2, end1));

    auto end2 = strand.end() - 1;
    ASSERT_EQ(2, getParityNucleotide(begin1, end2));

    ASSERT_EQ(1, getParityNucleotide(begin2, end2));
}
