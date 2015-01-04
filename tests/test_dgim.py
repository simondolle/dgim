import unittest
import itertools
from collections import deque
from dgim import Dgim


class TestDgim(unittest.TestCase):
    def test_get_count(self):
        dgim = Dgim(12)
        stream = iter([
            False, False, True, False, True, True, True, False, True,
            True, False, False, True, False, True, True, False
        ])
        for elt in stream:
            dgim.update(elt)
        self.assertEquals(7, dgim.get_count())

    def test_get_count_without_update(self):
        """Example from chapter 4 of "Mining of Massing Datasets"""
        crt_timestamp = 65
        # hand built dgim
        queues = [
            deque([crt_timestamp - 1, crt_timestamp - 2]),
            deque([crt_timestamp - 4]),
            deque([crt_timestamp - 8]),
            deque()
        ]

        dgim = Dgim(10)
        dgim.timestamp = crt_timestamp
        dgim.queues = queues
        self.assertEquals(6, dgim.get_count())

    def test_count_empty_stream(self):
        dgim = Dgim(10)
        self.assertEqual(0, dgim.get_count())

    def test_N_is_null(self):
        dgim = Dgim(0)
        stream = iter([True, False, False, True])
        for elt in stream:
            dgim.update(elt)
        self.assertEquals(0, dgim.get_count())

    def test_N_is_one(self):
        dgim = Dgim(1)
        dgim.update(True)
        self.assertEqual(1, dgim.get_count())
        dgim.update(False)
        self.assertEqual(0, dgim.get_count())

    def test_N_is_two(self):
        dgim = Dgim(2)
        dgim.update(True)
        self.assertEqual(1, dgim.get_count())
        dgim.update(True)
        self.assertEqual(2, dgim.get_count())
        dgim.update(True)
        self.assertEqual(2, dgim.get_count())

    def test_bucket_drop(self):
        crt_timestamp = 65
        # hand built dgim
        queues = [
            deque([crt_timestamp - 1, crt_timestamp - 2]),
            deque([crt_timestamp - 4]),
            deque()
        ]
        dgim = Dgim(6)
        dgim.timestamp = crt_timestamp
        dgim.queues = queues
        dgim.oldest_bucket_timestamp = crt_timestamp - 4
        self.assertEquals(3, dgim.nb_buckets)
        dgim.update(0)
        self.assertEquals(3, dgim.nb_buckets)
        dgim.update(0)
        self.assertEquals(2, dgim.nb_buckets)

    def test_only_zeros(self):
        dgim = Dgim(10)
        for elt in itertools.repeat(False, 1000):
            dgim.update(elt)
            self.assertEqual(0, dgim.get_count())

    def test_r_computation(self):
        dgim = Dgim(10, 0.5)
        self.assertEqual(2, dgim.r)

        dgim = Dgim(10, 0.1)
        self.assertEqual(10, dgim.r)

    def test_invalid_error_rates(self):
        self.assertRaises(ValueError, Dgim, 10, 0)
        self.assertRaises(ValueError, Dgim, 10, -0.1)
        self.assertRaises(ValueError, Dgim, 10, 1.1)

    def test_is_bucket_too_old(self):
        dgim = Dgim(10)
        dgim.timestamp = 15
        self.assertFalse(dgim.is_bucket_too_old(6))
        self.assertTrue(dgim.is_bucket_too_old(5))
        self.assertTrue(dgim.is_bucket_too_old(16))

        dgim.timestamp = 5
        self.assertFalse(dgim.is_bucket_too_old(16))
        self.assertTrue(dgim.is_bucket_too_old(15))
