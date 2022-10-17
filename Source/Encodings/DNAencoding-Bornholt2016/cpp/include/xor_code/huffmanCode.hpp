#ifndef XOR_CODE_HUFFMANCODE_H
#define XOR_CODE_HUFFMANCODE_H

#include <unordered_map>
#include <list>
#include <string>
#include <cstdint>

#include "settings.hpp"

namespace xor_code {

    struct TreeNode {

        /**
         * Fills the given map with the sequences leading to the leafs of this nodes subtree.
         * @param map The map that should be filled.
         * @param seq The sequence leading to the current tree node.
         */
        virtual void fillMap(std::unordered_map<uint8_t, types::ternaries> &map, types::ternaries &seq) = 0;

        /**
         * Decodes the given sequence of nucleotides into bytes and appends those bytes to 'out'.
         * @param itBegin A Random Access Iterator pointing at the start of the sequence (inclusive).
         * @param itEnd A Random Access Iterator pointing at the end of the sequence (exclusive).
         * @param out A sequence of bytes. The result of this function will be appended to the end of this sequence.
         */
        virtual void decode(types::iter &itBegin, types::iter &itEnd, types::bytes &out) const = 0;

    };

    struct Leaf : public TreeNode {

        uint8_t byte;

        explicit Leaf(uint8_t byte);

        void fillMap(std::unordered_map<uint8_t, types::ternaries> &map, types::ternaries &seq) override;

        void decode(types::iter &itBegin, types::iter &itEnd, types::bytes &out) const override;
    };

    struct ExtraLeaf : public TreeNode {

        types::ternaries extraSeq;

        void fillMap(std::unordered_map<uint8_t, types::ternaries> &map, types::ternaries &seq) override;

        void decode(types::iter &itBegin, types::iter &itEnd, types::bytes &out) const override;
    };

    struct Composite : public TreeNode {

        TreeNode *left, *middle, *right;

        Composite(TreeNode *left, TreeNode *middle, TreeNode *right);

        void fillMap(std::unordered_map<uint8_t, types::ternaries> &map, types::ternaries &seq) override;

        void decode(types::iter &itBegin, types::iter &itEnd, types::bytes &out) const override;
    };

    class HuffmanCode {

    private:
        static HuffmanCode *instance;
        TreeNode *root;
        std::unordered_map<uint8_t, types::ternaries> *map;
        ExtraLeaf *extraLeaf;

        HuffmanCode();

    public:

        HuffmanCode(HuffmanCode &other) = delete;

        void operator=(const HuffmanCode &other) = delete;

        /**
         * Returns the pointer to the single instance of this class.
         * @return A pointer to this class.
         */
        static HuffmanCode *getInstance();

        /**
         * Encodes the given byte as a sequence of ternary digits using a prefix encoding.
         * @param byte The byte that should be converted.
         * @return The calculated sequence of ternary digits.
         */
        const types::ternaries &encodeToTernaries(uint8_t byte);

        /**
         * Returns a sequence of ternary digits that will be decoded to nothing when given as input to decodeToByte().
         * @return The sequence of ternary digits.
         */
        const types::ternaries &getExtraTernaries();

        /**
         * Decodes the given sequence of nucleotides into bytes and appends those bytes to 'out'.
         * @param itBegin A Random Access Iterator pointing at the start of the sequence (inclusive).
         * @param itEnd A Random Access Iterator pointing at the end of the sequence (exclusive).
         * @param out A sequence of bytes. The result of this function will be appended to the end of this sequence.
         */
        void decodeToByte(types::iter &itBegin, types::iter &itEnd, types::bytes &out);

    };

}

#endif //XOR_CODE_HUFFMANCODE_H
