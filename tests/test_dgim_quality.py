import unittest
import itertools
from collections import deque

from dgim import Dgim
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
        self.sliding_window = deque()

    def update(self, elt):
        """Update the stream with one element.
        :param elt: the latest element of the stream
        :type elt: bool
        """
        self.sliding_window.append(elt)
        if len(self.sliding_window) > self.N:
            self.sliding_window.popleft()

    def get_count(self):
        """Returns an estimate of the number of "True"
        in the last N elements of the stream.
        :returns: int
        """
        return sum(self.sliding_window)


class TestDgimQuality(unittest.TestCase):

    def check_quality_settings(self, dgim, stream):
        """Compare the result "e" returned by dgim with the exact result
        "c" on a stream which elements are 0 or 1.
        The test fails if the dgim result "e" is not in the expected bounds.
        0.5 * c <= e <= 1.5 * c

        :param dgim: the Dgim instance to test
        :type dgim: Dgim
        :param stream: the stream to use. It should contains only 0 or 1 as elements.
        :type stream: iterator
        """
        exact_algorithm = ExactAlgorithm(dgim.N)
        for elt in stream:
            dgim.update(elt)
            exact_algorithm.update(elt)

            exact_result = exact_algorithm.get_count()
            error = abs(dgim.get_count() - exact_result)
            self.assertTrue(error <= dgim.error_rate * exact_result)

    def test_nominal_case(self):
        dgim = Dgim(N=100, error_rate=0.5)
        stream = generate_random_stream(length=10000)
        self.check_quality_settings(dgim=dgim, stream=stream)

    def test_large_N(self):
        dgim = Dgim(N=10000, error_rate=0.5)
        stream = generate_random_stream(length=2000)
        self.check_quality_settings(dgim=dgim, stream=stream)

    def test_short_stream(self):
        dgim = Dgim(N=1000, error_rate=0.5)
        # stream is shorter than N
        stream = generate_random_stream(length=100)
        self.check_quality_settings(dgim=dgim, stream=stream)

    def test_N_is_one(self):
        dgim = Dgim(N=1, error_rate=0.5)
        stream = generate_random_stream(length=10)
        self.check_quality_settings(dgim=dgim, stream=stream)

    def test_N_is_two(self):
        dgim = Dgim(N=2, error_rate=0.5)
        stream = generate_random_stream(length=100)
        self.check_quality_settings(dgim=dgim, stream=stream)

    def test_low_error_rate_case(self):
        dgim = Dgim(N=100, error_rate=0.01)
        stream = generate_random_stream(length=1000)
        self.check_quality_settings(dgim=dgim, stream=stream)

    def test_only_true_case(self):
        dgim = Dgim(N=100, error_rate=0.5)
        stream = itertools.repeat(True, 10000)
        self.check_quality_settings(dgim=dgim, stream=stream)
