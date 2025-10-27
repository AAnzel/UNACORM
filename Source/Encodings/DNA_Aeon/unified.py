import json
import os
import subprocess

import numpy as np

path_working_dir = os.path.dirname(os.path.realpath(__file__))
conf_file_path = os.path.join(path_working_dir, "config.json")


def encode(string_file_name, numpy_boolen_array=None):
    if numpy_boolen_array:
        raise IOError(
            "Numpy boolean array input is not supported, please use a filepath to the target."
        )
    if not os.path.exists(string_file_name):
        raise IOError("Input file does not exists")

    with open(conf_file_path, "r") as conf_file:
        cfile = json.load(conf_file)
        cfile["encode"]["input"] = string_file_name
        conf_file.seek(0)
    with open(conf_file_path, "w") as conf_file:
        json.dump(cfile, conf_file, indent=4)

    subprocess.call([
        "python",
        os.path.join(path_working_dir, "encode.py"),
        "-c",
        conf_file_path,
    ])

    sequences = []
    with open(
        os.path.join(path_working_dir, "data", "encoded.fasta"), "r"
    ) as file:
        sequence = ""
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if sequence != "":
                    sequences.append(sequence)
                    sequence = ""
            else:
                sequence += line
        if sequence != "":
            sequences.append(sequence)

    return sequences


def decode(string_file_name=None, list_of_dna_strings=None):
    if list_of_dna_strings:
        with open(
            os.path.join(path_working_dir, "data", "to_be_decoded.fasta"), "w"
        ) as file:
            for i, sequence in enumerate(list_of_dna_strings):
                header = ">{}\n".format(i + 1)
                file.write(header)
                file.write(sequence + "\n")
    with open(conf_file_path, "r") as conf_file:
        # DNA-Aeon decodes the file with the original filename, have to extract it before being able to read in the decoded data.
        cfile = json.load(conf_file)
        input_file_name = cfile["encode"]["input"].split("/")[-1]
        if list_of_dna_strings:
            cfile["decode"]["input"] = (
                "Encodings/DNA_Aeon/data/to_be_decoded.fasta"
            )
        # elif string_file_name:
        #    cfile["decode"]["input"] = string_file_name
        else:
            raise IOError
        conf_file.seek(0)
    with open(conf_file_path, "w") as conf_file:
        json.dump(cfile, conf_file, indent=4)

    subprocess.call([
        "python",
        os.path.join(path_working_dir, "decode.py"),
        "-c",
        conf_file_path,
    ])

    with open(
        os.path.join(path_working_dir, "data", "results", input_file_name), "rb"
    ) as f:
        data = np.fromfile(f, dtype=np.uint8)
    bits = np.unpackbits(data).astype(bool)
    return bits
