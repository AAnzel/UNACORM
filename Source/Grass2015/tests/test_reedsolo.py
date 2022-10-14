import unittest
import reedSolomon
from reedSolomon import Generalized_Reed_Solomon, Galois_Helper
import galois as gl

import numpy as np


class ReedSoloTest(unittest.TestCase):

    # Test case in which both k and r are divisble by a parameter p
    def test_k_and_r_divisble_by_p_base_two(self):
        print("test_k_and_r_divisble_by_p_base_two")
        # TODO check Reed_Solomon(2,12,6,6,7) index out of error shouldnt happen
        test_normal_rs = Generalized_Reed_Solomon(2, 12, 6, 8, 3)
        normal_msg = test_normal_rs.encode([5, 6, 4, 10, 3, 5])
        normal_msg_org = np.copy(normal_msg)
        normal_msg[2] = 11
        normal_msg[1] = 11
        dec_test_normal = test_normal_rs.decode(normal_msg)
        self.assertTrue([5, 6, 4, 10, 3, 5] == dec_test_normal)

    # Test case in which k is not divisble by p but r is
    def test_k_not_divisble_by_p_base_two(self):
        print("test_k_not_divisble_by_p_base_two")
        inner_encoder = reedSolomon.Generalized_Reed_Solomon(
            2, 11, 5, 8, 3)  # n 12 k 5 c 2 r 7 d 1 -> 5 + 9 - (3 -1)
        # 3- 2 = 1   12 -3- 2 = 7 3-1 = 2
        msg = inner_encoder.encode([5, 6, 0, 0, 3])
        msg_org = np.copy(msg)
        msg[3] = 11
        msg[2] = 11
        dec_msg = inner_encoder.decode(msg)
        self.assertTrue([5, 6, 0, 0, 3] == dec_msg)

    # Test case in which both k and r are divisble by a parameter p
    def test_k_and_r_divisble_by_p_base_five(self):
        print("test_k_and_r_divisble_by_p_base_five")
        org_info = [5, 6, 4, 10, 3, 5, 7, 4, 5]
        org_compare = np.copy(org_info)
        test_normal_rs = Generalized_Reed_Solomon(7, 15, 9, 4, 3)
        normal_msg = test_normal_rs.encode(org_info)
        normal_msg[2] = 11
        dec_test_normal = test_normal_rs.decode(normal_msg)
        print("dec", dec_test_normal)
        self.assertTrue((org_compare == dec_test_normal).all())

    # Test case in which both k and r are divisble by a parameter p
    def test_k_and_not_divisble_by_p_base_seven(self):
        print("test_k_and_r_divisble_by_p_base_five")
        org_info = [5, 6, 4, 10, 3, 5, 7, 4, 5]
        org_compare = np.copy(org_info)
        test_normal_rs = Generalized_Reed_Solomon(7, 15, 9, 4, 6)
        normal_msg = test_normal_rs.encode(org_info)
        normal_msg[2] = 11
        normal_msg[1] = 11
        dec_test_normal = test_normal_rs.decode(normal_msg)
        print("dec", dec_test_normal)
        self.assertTrue([5, 6, 4, 10, 3, 5, 7, 4, 5] == dec_test_normal)

    def test_k_and_r_not_divisible_by_p(self):
        print("test_k_and_r_not_divisible_by_p")
        org_info = [30, 20, 20, 9, 25, 1, 7, 2, 0, 18, 17, 22, 11]
        org_compare = np.copy(org_info)
        test_normal_rs = Generalized_Reed_Solomon(31, 24, 13, 2, 3)
        normal_msg = test_normal_rs.encode(org_info)
        normal_msg[2] = 11
        dec_test_normal = test_normal_rs.decode(normal_msg)
        print("dec", dec_test_normal)
        self.assertTrue((org_compare == dec_test_normal).all())


if __name__ == '__main__':
    unittest.main()
