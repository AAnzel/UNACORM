import numpy as np
import xor_code_python as xor


def test_max_strand_length():
    xor.set_max_strand_length(120)
    assert xor.get_max_strand_length() == 120
    xor.set_max_strand_length(111)
    assert xor.get_max_strand_length() == 111


def test_payload_byte_length():
    xor.set_max_strand_length(120)
    assert xor.get_payload_byte_length() == 6
    xor.set_max_strand_length(111)
    assert xor.get_payload_byte_length() == 5


def test_xor_size():
    xor.set_xor_size(7)
    assert xor.get_xor_size() == 7
    xor.set_xor_size(11)
    assert xor.get_xor_size() == 11


def test_xor_step():
    xor.set_xor_step(5)
    assert xor.get_xor_step() == 5
    xor.set_xor_step(3)
    assert xor.get_xor_step() == 3


def test_encode_decode():
    original = np.array([i >= 0.5 for i in np.random.rand(1_000_000)])
    encoded = xor.encode('test', original)
    decoded = xor.decode('test', encoded)
    assert (original == decoded).all()
