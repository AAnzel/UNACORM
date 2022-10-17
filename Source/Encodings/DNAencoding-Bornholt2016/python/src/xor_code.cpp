#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "xor_code/encode.hpp"
#include "xor_code/decode.hpp"
#include "xor_code/settings.hpp"

namespace py = pybind11;
using namespace pybind11::literals;

namespace xor_code {
    std::vector<std::string> encode_helper(const std::string &filename, const py::array_t<bool> &data) {
        // convert bit array to byte vector
        types::bytes bytes;

        uint8_t byte;
        for (size_t i = 0; i < data.size(); ++i) {
            byte = (byte << 1) ^ data.at(i);

            if (i % 8 == 7) {
                bytes.push_back(byte);
            }
        }

        // if the last byte isn't complete, don't forget it
        if (data.size() % 8 != 0) {
            byte = byte << data.size() % 8;
            bytes.push_back(byte);
        }


        // encode data
        auto strands = encode(filename, bytes);


        // convert vector of nucleotides to vector of strings
        std::vector<std::string> result;

        for (const auto &strand: strands) {
            std::string s;
            for (uint8_t nucleotide: strand) {
                s.push_back(getCharNucleotide(nucleotide));
            }
            result.push_back(s);
        }

        return result;
    }

    py::array_t<bool> decode_helper(const std::string &filename, const std::vector<std::string> &strands) {
        // convert vector of strings to vector of nucleotides
        std::vector<types::nucleotides> nucleotides;

        for (const auto &strand: strands) {
            types::nucleotides n;
            for (char nucleotide: strand) {
                n.push_back(getIntegerNucleotide(nucleotide));
            }
            nucleotides.push_back(n);
        }


        // decode data
        auto bytes = decode(filename, nucleotides);


        // convert byte vector to bit array
        std::vector<bool> result;

        for (uint8_t byte: bytes) {
            for (int8_t shift = 7; shift >= 0; --shift) {
                result.push_back((byte >> shift & 0x1) == 0x1);
            }
        }

        return py::cast(result);
    }


    PYBIND11_MODULE(xor_code_python, m) {
        m.doc() = R"pbdoc(
            Python bindings for the implementation of the xor based DNA Encoding created by Bornholt et al..
            )pbdoc";


        m.def("encode", &encode_helper, R"pbdoc(
            Encodes the given data into strands of nucleotides.
            )pbdoc", "filename"_a, "data"_a);

        m.def("decode", &decode_helper, R"pbdoc(
            Decodes the given nucleotide strands, filtered by the given key (filename), into binary data.
            )pbdoc", "filename"_a, "strands"_a);


        m.def("get_max_strand_length", &getMaxStrandLength, R"pbdoc(
            Returns the maximum length of a strand measured in nucleotides.
            )pbdoc");

        m.def("set_max_strand_length", &setMaxStrandLength, R"pbdoc(
            Sets the maximum length of a strand measured in nucleotides to the given parameter.
            )pbdoc", "length"_a);


        m.def("get_payload_byte_length", &getPayloadByteLength, R"pbdoc(
            Returns the amount of bytes a single payload contains.
            )pbdoc");


        m.def("get_xor_size", &getXorSize, R"pbdoc(
            Returns the amount of strands that that are used to create a single xor strand.
            )pbdoc");

        m.def("set_xor_size", &setXorSize, R"pbdoc(
            Sets the amount of strands that that are used to create a single xor strand to the given parameter.
            )pbdoc", "size"_a);


        m.def("get_xor_step", &getXorStep, R"pbdoc(
            Returns the step size for the creation of the xor strands.
            If the strand with index i is the first strand used to create a xor strand then the first strand for the next xor strand will have index i + step size.
            )pbdoc");

        m.def("set_xor_step", &setXorStep, R"pbdoc(
            Sets the step size for the creation of the xor strands to the given parameter.
            If the strand with index i is the first strand used to create a xor strand then the first strand for the next xor strand will have index i + step size.
            )pbdoc", "step"_a);
    }
}
