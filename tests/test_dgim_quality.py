import unittest
import itertools
from dgim.dgim import Dgim
from dgim.utils import generate_random_stream


class ExactAlgorithm(object):
    """Exact algorithm to count the number of "True"
    in the last N elements of a boolean stream."""
    def __init__(self, N):
        """Constructor
        :param N: size of the sliding window
        :type N: int
        """
        self.N = N
        self.sliding_window = []

    def update(self, elt):
        """Update the stream with one element.
        :param elt: the latest element of the stream
        :type elt: bool
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

    def check_quality_settings(self, N, r, stream):
        """Compare the result "e" returned by dgim with the exact result
        "c" on a stream which elements are 0 or 1.
        The test fails if the dgim result "e" is not in the expected bounds.
        0.5 * c <= e <= 1.5 * c

        :param N: sliding window length
        :type N: int
        :param r: the maximum number of buckets of the same size
        :type r: int
        :param stream: the stream to use. It should contains only 0 or 1 as elements.
        :type stream: iterator
        """
        dgim = Dgim(N, r)
        exact_algorithm = ExactAlgorithm(N)
        for elt in stream:
            dgim.update(elt)
            exact_algorithm.update(elt)

            exact_result = exact_algorithm.get_count()
            error = abs(dgim.get_count() - exact_result)
            self.assertTrue(error <= dgim.error_rate * exact_result)

    def test_nominal_case(self):
        stream = generate_random_stream(length=10000)
        self.check_quality_settings(N=100, r=2, stream=stream)

    def test_large_N(self):
        stream = generate_random_stream(length=2000)
        self.check_quality_settings(N=10000, r=2, stream=stream)

    def test_short_stream(self):
        # stream is shorter than N
        stream = generate_random_stream(length=100)
        self.check_quality_settings(N=1000, r=2, stream=stream)

    def test_N_is_one(self):
        stream = generate_random_stream(length=10)
        self.check_quality_settings(N=1, r=2, stream=stream)

    def test_N_is_two(self):
        stream = generate_random_stream(length=100)
        self.check_quality_settings(N=2, r=2, stream=stream)

    def test_low_error_rate_case(self):
        stream = generate_random_stream(length=1000)
        self.check_quality_settings(N=100, r=100, stream=stream)

    def test_only_true_case(self):
        stream = itertools.repeat(True, 10000)
        self.check_quality_settings(N=100, r=2, stream=stream)
