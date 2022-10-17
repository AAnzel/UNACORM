#include <iostream>
#include <filesystem>
#include "xor_code/encode.hpp"
#include "xor_code/decode.hpp"
#include "xor_code/settings.hpp"

bool doConsoleOutput = false;
std::string inputDirectory = "../../cpp/examples/data/";
std::string fileName = "example.jpg";
bool doFileOutput = true;
std::string outputDirectory = inputDirectory + "out/";

int main() {
    using namespace xor_code;

    setXorStep(2);
    setXorSize(3);

    std::cout << "Working directory: " << std::filesystem::current_path() << "\n";

    auto start = std::chrono::high_resolution_clock::now();

    auto strands = encode(inputDirectory + fileName);

    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "Time for encoding: " << duration.count() << '\n';

    if (doConsoleOutput) {
        std::cout << "Strands: " << strands.size() << "\n";
        for (const auto &assembled: strands) {
            for (uint8_t nucleotide: assembled) {
                std::cout << getCharNucleotide(nucleotide);
            }
            std::cout << " (" << assembled.size() << ')' << '\n';
        }
    }

    auto filteredStrands = std::vector<types::nucleotides>();
    for (int i = 0; i < strands.size(); ++i) {
        if ((i % 3 != 0 && i % 5 != 0) || i > strands.size() / 2) {
            filteredStrands.push_back(strands[i]);
        }
    }

    start = std::chrono::high_resolution_clock::now();

    auto original = decode(fileName, filteredStrands);

    end = std::chrono::high_resolution_clock::now();
    duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    std::cout << "Time for decoding: " << duration.count() << '\n';

    if (doFileOutput) {
        std::filesystem::create_directories(outputDirectory);
        auto out = std::ofstream(outputDirectory + fileName, std::ios::binary);
        for (uint8_t character: original) {
            out << character;
        }
        out.close();
    }

    if (doConsoleOutput) {
        std::cout << "Original File: \n";
        for (uint8_t character: original) {
            std::cout << character;
        }
        std::cout << "\n";
    }

    std::cout << "Done" << '\n';
}
