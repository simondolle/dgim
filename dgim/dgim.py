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
        self.oldest_bucket_timestamp = -1  # No bucket so far

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
        if self.N == 0:
            return
        self.timestamp = (self.timestamp + 1) % (2 * self.N)
        #check if oldest bucket should be removed
        if self.oldest_bucket_timestamp >= 0 and self.is_bucket_too_old(self.oldest_bucket_timestamp):
            self.drop_oldest_bucket()
        if elt != 1:
            #nothing to do
            return

        reminder = self.timestamp
        if self.oldest_bucket_timestamp == -1:
            self.oldest_bucket_timestamp = self.timestamp
        for queue in self.queues:
            queue.appendleft(reminder)
            if len(queue) <= self.r:
                break
            last = queue.pop()
            second_last = queue.pop()
            # merge last two buckets.
            reminder = second_last
            if last == self.oldest_bucket_timestamp:
                self.oldest_bucket_timestamp = second_last

    def is_bucket_too_old(self, bucket_timestamp):
        """Check if a bucket is too old and should be dropped.
        ;param bucket_timestamp: the bucket timestamp
        :type bucket_timestamp: int
        :returns: bool
        """
        # the buckets are stored modulo 2 * N
        return (self.timestamp - bucket_timestamp) % (2 * self.N) >= self.N

    def drop_oldest_bucket(self):
        """Drop oldest bucket timestamp."""
        for queue in reversed(self.queues):
            if len(queue) > 0:
                queue.pop()
                break
        #update oldest bucket timestamp
        self.oldest_bucket_timestamp = -1
        for queue in reversed(self.queues):
            if len(queue) > 0:
                self.oldest_bucket_timestamp = queue[-1]
                break

    def get_count(self):
        """Returns an estimate of the number of ones in the sliding window.
        :returns: int
        """
        result = 0
        max_value = 0
        power_of_two = 1
        for queue in self.queues:
            queue_length = len(queue)
            if queue_length > 0:
                max_value = power_of_two
                result += queue_length * power_of_two
            power_of_two = power_of_two << 1
        result -= math.floor(max_value/2)
        return int(result)
