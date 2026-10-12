"""UNACORM wrapper for the VNX-DNA codec.

VNX-DNA is installed in its own Python environment (it needs reedsolo>=1.7, while
the platform pins reedsolo==0.3 for another codec), so this wrapper calls its
command-line interface in a subprocess. The executable is taken from the
VNXDNA_BIN environment variable, then /opt/vnxdna/bin/vnx-dna (the Docker
image), then `vnx-dna` on PATH.

encode: file bits -> VNX-DNA container -> list of DNA strands.
decode: list of (possibly noisy) reads -> original file bits. VNX-DNA publishes
output only after the SHA-256 of the whole file verifies, so a failed decode
returns an empty array instead of wrong data.
"""

import os
import shutil
import subprocess
import tempfile

import numpy as np

# Store profile and single-read decoder settings used for the benchmark.
_STORE_ARGS = ["--profile", "archival"]
_RECOVER_ARGS = [
    "--burst-repair", "16",
    "--experimental-indel-repair",
    "--max-indel", "2",
]
_TIMEOUT_SECONDS = 3600


def _vnxdna_executable():
    for candidate in (
        os.environ.get("VNXDNA_BIN"),
        os.path.join(os.sep, "opt", "vnxdna", "bin", "vnx-dna"),
        shutil.which("vnx-dna"),
    ):
        if candidate and os.path.isfile(candidate):
            return candidate
    raise RuntimeError(
        "VNX-DNA is not installed: set VNXDNA_BIN to the vnx-dna executable"
    )


def _run(list_args):
    completed = subprocess.run(
        [_vnxdna_executable()] + list_args,
        capture_output=True,
        text=True,
        timeout=_TIMEOUT_SECONDS,
    )
    return completed.returncode, completed.stderr


def _read_fasta(path_fasta):
    list_sequences = []
    list_current = []
    with open(path_fasta, "r") as file:
        for string_line in file:
            string_line = string_line.strip()
            if not string_line:
                continue
            if string_line.startswith(">"):
                if list_current:
                    list_sequences.append("".join(list_current))
                    list_current = []
            else:
                list_current.append(string_line)
    if list_current:
        list_sequences.append("".join(list_current))
    return list_sequences


def encode(string_file_name, numpy_boolean_array=None):
    """Encode a file (or a NumPy boolean bit array) into DNA strands."""
    with tempfile.TemporaryDirectory(prefix="vnxdna_") as path_tmp:
        if numpy_boolean_array is not None and len(numpy_boolean_array) > 0:
            path_input = os.path.join(path_tmp, "input.bin")
            with open(path_input, "wb") as file:
                file.write(
                    np.packbits(np.asarray(numpy_boolean_array, dtype=bool))
                    .tobytes()
                )
        elif string_file_name and os.path.isfile(string_file_name):
            path_input = string_file_name
        else:
            raise IOError("Input file does not exist")

        path_container = os.path.join(path_tmp, "archive.vxdna")
        path_strands = os.path.join(path_tmp, "strands.fasta")
        int_code, string_err = _run(
            ["store", path_input, "-o", path_container, "--no-name"]
            + _STORE_ARGS
        )
        if int_code != 0:
            raise RuntimeError("VNX-DNA store failed: " + string_err)
        int_code, string_err = _run(
            ["encode", path_container, "-o", path_strands, "--no-index"]
        )
        if int_code != 0:
            raise RuntimeError("VNX-DNA encode failed: " + string_err)
        return _read_fasta(path_strands)


def decode(string_file_name=None, list_of_dna_strings=None):
    """Decode DNA reads back into the original bits (empty array on failure)."""
    if not list_of_dna_strings:
        return np.array([], dtype=bool)
    with tempfile.TemporaryDirectory(prefix="vnxdna_") as path_tmp:
        path_reads = os.path.join(path_tmp, "reads.fasta")
        path_output = os.path.join(path_tmp, "recovered.bin")
        with open(path_reads, "w") as file:
            for int_i, string_read in enumerate(list_of_dna_strings):
                file.write(">" + str(int_i) + "\n" + string_read.strip() + "\n")
        int_code, _ = _run(
            ["recover", path_reads, "-o", path_output] + _RECOVER_ARGS
        )
        if int_code != 0 or not os.path.isfile(path_output):
            return np.array([], dtype=bool)
        with open(path_output, "rb") as file:
            bytes_data = file.read()
    return np.unpackbits(np.frombuffer(bytes_data, dtype=np.uint8)).astype(bool)
