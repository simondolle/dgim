import unittest
import random
from dgim.dgim import Dgim

class ExactAlgorithm(object):
    """Exact algorithm to count the number of ones
    in the last N elements of a stream."""
    def __init__(self, N):
        """Constructor
        :param N: size of the sliding window
        :type N: int
        """
        self.N = N
        self.sliding_window = []

    def update(self, elt):
        """Update the stream with one element.
        The element can be either 0 or 1.
        :param elt: the latest element of the stream
        :type elt: int
        """
        self.sliding_window.append(elt)
        if len(self.sliding_window) > self.N:
            self.sliding_window.pop(0)

    def get_count(self):
        """Returns an estimate of the number of ones in the sliding window.
        :returns: int
        """
        return sum(self.sliding_window)


class TestDgimQuality(unittest.TestCase):

    def generate_random_stream(self, length):
        """Generate a random stream of zeros and ones.
        :param length: the stream length
        :type length: int
        :returns: iterator
        """
        for i in range(length):
            yield random.randint(0, 1)

    def check_quality_settings(self, N, stream_length):
        """Compare the result "e" returned by dgim with the exact result
        "c" on a random stream.
        The test fails if the dgim result "e" is not in the expected bounds.
        0.5 * c <= e <= 1.5 * c

        :param N: sliding window length
        :type N: int
        :param stream_length: the length of the random stream
        :type stream_length: int
        """
        dgim = Dgim(N)
        exact_algorithm = ExactAlgorithm(N)
        for elt in self.generate_random_stream(stream_length):
            dgim.update(elt)
            exact_algorithm.update(elt)

            exact_result = exact_algorithm.get_count()
            error = abs(dgim.get_count() - exact_result)
            self.assertTrue(float(error) <= 0.5 * exact_result)

    def test_nominal_case(self):
        self.check_quality_settings(N=100, stream_length=1000)

    def test_large_N(self):
        self.check_quality_settings(N=10000, stream_length=20000)

    def test_short_stream(self):
        # stream is shorter than N
        self.check_quality_settings(N=1000, stream_length=100)

    def test_N_is_one(self):
        self.check_quality_settings(N=1, stream_length=10)

    def test_N_is_two(self):
        self.check_quality_settings(N=2, stream_length=100)
