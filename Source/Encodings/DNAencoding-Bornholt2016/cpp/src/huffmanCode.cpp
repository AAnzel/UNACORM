#include <cstdint>
#include <queue>
#include <unordered_map>
#include <list>
#include "xor_code/huffmanCode.hpp"

namespace xor_code {

    Leaf::Leaf(uint8_t byte) {
        this->byte = byte;
    }

    void Leaf::fillMap(std::unordered_map<uint8_t, types::ternaries> &map, types::ternaries &seq) {
        map[byte] = seq;
    }

    void Leaf::decode(types::iter &itBegin, types::iter &itEnd, types::bytes &out) const {
        out.push_back(byte);
    }

    void ExtraLeaf::fillMap(std::unordered_map<uint8_t, types::ternaries> &map, types::ternaries &seq) {
        extraSeq = seq;
    }

    void ExtraLeaf::decode(types::iter &itBegin, types::iter &itEnd, types::bytes &out) const {
        // don't do anything
    }

    Composite::Composite(TreeNode *left, TreeNode *middle, TreeNode *right) {
        this->left = left;
        this->middle = middle;
        this->right = right;
    }

    void Composite::fillMap(std::unordered_map<uint8_t, types::ternaries> &map, types::ternaries &seq) {
        seq.push_back(0);
        left->fillMap(map, seq);
        seq.back() = 1;
        middle->fillMap(map, seq);
        seq.back() = 2;
        right->fillMap(map, seq);
        seq.pop_back();
    }

    void Composite::decode(types::iter &itBegin, types::iter &itEnd, types::bytes &out) const {
        if (itBegin != itEnd) {
            switch (*itBegin) {
                case 0:
                    ++itBegin;
                    return left->decode(itBegin, itEnd, out);
                case 1:
                    ++itBegin;
                    return middle->decode(itBegin, itEnd, out);
                case 2:
                    ++itBegin;
                    return right->decode(itBegin, itEnd, out);
                default:
                    ++itBegin;
                    return left->decode(itBegin, itEnd, out);
            }
        }
    }

    HuffmanCode *HuffmanCode::instance = nullptr;

    HuffmanCode *HuffmanCode::getInstance() {
        if (instance == nullptr) {
            instance = new HuffmanCode();
        }
        return instance;
    }

    HuffmanCode::HuffmanCode() {
        std::queue<TreeNode *> q;
        // create a node for each possible byte
        uint8_t byte = 0;
        for (int i = 0; i < 256; ++i) {
            q.push(new Leaf(byte));
            ++byte;
        }
        // add an extra node so that every node later on will have exactly three children
        extraLeaf = new ExtraLeaf();
        q.push(extraLeaf);
        while (q.size() > 1) {
            auto *n1 = q.front();
            q.pop();
            auto *n2 = q.front();
            q.pop();
            auto *n3 = q.front();
            q.pop();
            q.push(new Composite(n1, n2, n3));
        }
        root = q.front();
        types::ternaries curSeq;
        map = new std::unordered_map<uint8_t, types::ternaries>;
        root->fillMap(*map, curSeq);
    }

    const types::ternaries &HuffmanCode::encodeToTernaries(uint8_t byte) {
        return (*map)[byte];
    }

    const types::ternaries &HuffmanCode::getExtraTernaries() {
        return extraLeaf->extraSeq;
    }

    void HuffmanCode::decodeToByte(types::iter &itBegin, types::iter &itEnd, types::bytes &out) {
        root->decode(itBegin, itEnd, out);
    }
}
