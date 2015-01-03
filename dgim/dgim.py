import math
from collections import deque

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

    def __init__(self, N, r=2):
        """Constructor
        :param N: size of the sliding window
        :type N: int
        :param r: the maximum number of buckets of the same size
        :type r: int
        """
        self.N = N
        if r < 2:
            raise ValueError("'r' should be higher or equal to 2. Got {}.".format(r))
        self.r = r
        self.queues = []
        if N == 0:
            max_index = -1
        else:
            max_index = int(math.ceil(math.log(N)/math.log(2)))

        for i in range(max_index + 1):
            self.queues.append(deque())

        self.timestamp = 0

    @property
    def error_rate(self):
        """Return the maximum error rate made by the algorithm.
        Let c be the true result and e the estimate returned by the dgim
        algorithm.
        abs(c-e) < error_rate * c
        :returns: float
        """
        return 1/float(self.r)

    @property
    def nb_buckets(self):
        """Returns the number of buckets.
        :returns: int
        """
        result = 0
        for queue in self.queues:
            result += len(queue)
        return result

    def update(self, elt):
        """Update the stream with one element.
        The element can be either 0 or 1.
        :param elt: the latest element of the stream
        :type elt: int
        """
        self.timestamp += 1
        #check if oldest bucket should be removed
        if self.is_oldest_bucket_too_old():
            self.drop_oldest_bucket()
        if elt != 1:
            return
        reminder = self.timestamp
        for queue in self.queues:
            queue.appendleft(reminder)
            if len(queue) <= self.r:
                break
            last = queue.pop()
            last_previous = queue.pop()
            reminder = max(last, last_previous)

    def is_oldest_bucket_too_old(self):
        """Check if the latest bucket is too old and should be dropped.
        :returns: bool
        """
        oldest_bucket_timestamp = self.get_oldest_bucket_timestamp()
        return (oldest_bucket_timestamp >= 0 and
                oldest_bucket_timestamp <= self.timestamp - self.N)

    def drop_oldest_bucket(self):
        """Drop oldest bucket timestamp."""
        for queue in reversed(self.queues):
            if len(queue) > 0:
                queue.pop()
                break

    def get_oldest_bucket_timestamp(self):
        """Return the timestamp of the oldest bucket.
        If there is no bucket, returns -1
        :returns: int
        """
        for queue in reversed(self.queues):
            if len(queue) > 0:
                return queue[-1]
        return -1

    def get_count(self):
        """Returns an estimate of the number of ones in the sliding window.
        :returns: int
        """
        #find the all the buckets which most recent timestamp is ok
        result = 0
        max_index = 0
        for index, queue in enumerate(self.queues):
            result += len(queue) * int(2 ** index)
            if len(queue) > 0:
                max_index = index
        result -= math.floor((2 ** max_index)/2)
        return int(result)
