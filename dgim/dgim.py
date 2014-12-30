class Dgim(object):
    """An implementation of the DGIM algorithm.
    It estimates the number of 1s present in a sliding window of a stream
    while using few memory.

    The algorithm is described in:
    Datar, Mayur, et al. "Maintaining stream statistics over sliding windows."
    SIAM Journal on Computing 31.6 (2002): 1794-1813.

    An explanation of the algorithm can also be found here:
    http://infolab.stanford.edu/~ullman/mmds/ch4.pdf
    """

    def __init__(self, N):
        """Constructor
        :param N: size of the sliding window
        :type N: int
        """
        self.N = N

    def update(self, elt):
        """Update the stream with one element.
        The element can be either 0 or 1.
        :param elt: the latest element of the stream
        :type elt: int
        """
        pass

    def get_count(self):
        """Returns an estimate of the number of ones in the sliding window.
        :returns: int
        """
        pass


class Bucket(object):
    """A class to represent a bucket."""
    def __init__(self, most_recent_timestamp, one_count):
        """Constructor
        :param most_recent_timestamp: the timestamp of the most recent element
                                      that belongs to the bucket.
        :type most_recent_timestamp: int
        :param one_count: the count of ones in this bucket.
                          It must be a power of 2.
        """
        self.most_recent_timestamp = most_recent_timestamp
        self.one_count = one_count

    def merge(self, other_bucket):
        """Merge this bucket with an other bucket.
        :param other_bucket: the bucket that has to be merged with this one.
        :type other_bucket: Bucket
        """
        pass
