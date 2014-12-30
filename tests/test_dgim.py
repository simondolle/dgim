import unittest

from dgim.dgim import Dgim, Bucket

class TestDgim(unittest.TestCase):
    def test_get_count(self):
        """Example from chapter 4 of "Mining of Massing Datasets"""
        dgim = Dgim(10)
        stream = iter([
            1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0
            ])
        for elt in stream:
            dgim.update(elt)
        self.assertEquals(6, dgim.get_count())

    def test_get_count_without_update(self):
        crt_timestamp = 65
        #hand built dgim
        buckets = [
            Bucket(crt_timestamp - 1, 1),
            Bucket(crt_timestamp - 2, 1),
            Bucket(crt_timestamp - 4, 2),
            Bucket(crt_timestamp - 8, 4),
            Bucket(crt_timestamp - 13, 8),
            Bucket(crt_timestamp - 21, 8)
        ]
        dgim = Dgim(10)
        dgim.timestamp = crt_timestamp
        dgim.buckets = buckets

        self.assertEquals(6, dgim.get_count())

    def test_count_empty_stream(self):
        dgim = Dgim(10)
        self.assertEqual(0, dgim.get_count())
