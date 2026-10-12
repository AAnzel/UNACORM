import os
import random
import shutil
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unified  # noqa: E402


def _installed():
    try:
        unified._vnxdna_executable()
        return True
    except RuntimeError:
        return False


pytestmark = pytest.mark.skipif(not _installed(), reason="VNX-DNA not installed")


def _bits(bytes_data):
    return np.unpackbits(np.frombuffer(bytes_data, dtype=np.uint8)).astype(bool)


def test_round_trip_from_file(tmp_path):
    bytes_data = bytes(random.Random(1).getrandbits(8) for _ in range(5000))
    path_file = tmp_path / "data.bin"
    path_file.write_bytes(bytes_data)
    list_strands = unified.encode(str(path_file))
    assert list_strands and all(set(s) <= set("ACGT") for s in list_strands)
    np.testing.assert_array_equal(unified.decode("", list_strands), _bits(bytes_data))


def test_round_trip_from_bool_array():
    bytes_data = b"UNACORM VNX-DNA round trip " * 50
    list_strands = unified.encode("", _bits(bytes_data))
    np.testing.assert_array_equal(unified.decode("", list_strands), _bits(bytes_data))


def test_round_trip_with_substitutions_and_shuffle():
    bytes_data = bytes(range(256)) * 20
    list_strands = unified.encode("", _bits(bytes_data))
    rng = random.Random(2)
    list_reads = []
    for string_strand in list_strands:
        list_bases = list(string_strand)
        int_pos = rng.randrange(len(list_bases))
        list_bases[int_pos] = "ACGT"[("ACGT".index(list_bases[int_pos]) + 1) % 4]
        list_reads.append("".join(list_bases))
    rng.shuffle(list_reads)
    np.testing.assert_array_equal(unified.decode("", list_reads), _bits(bytes_data))


def test_unrecoverable_input_returns_empty_array():
    rng = random.Random(3)
    list_reads = ["".join(rng.choice("ACGT") for _ in range(150)) for _ in range(50)]
    assert unified.decode("", list_reads).size == 0
    assert unified.decode("", []).size == 0
