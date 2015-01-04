import math
from collections import deque

class Dgim(object):
    """An implementation of the DGIM algorithm.
    It estimates the number of "True" present the last N elements
    of a boolean stream.
    The datastructure it uses is very compact and
    has a memory complexity of O(log(N)^2).

    The algorithm is described in:
    Datar, Mayur, et al. "Maintaining stream statistics over sliding windows."
    SIAM Journal on Computing 31.6 (2002): 1794-1813.

    An explanation of the algorithm can also be found here:
    http://infolab.stanford.edu/~ullman/mmds/ch4.pdf
    """

    def __init__(self, N, error_rate=0.5):
        """Constructor
        :param N: size of the sliding window
        :type N: int
        :param error_rate: the maximum error made by the algorithm.
        The error rate is in ]0, 1]
        Let c be the true result and e the estimate returned by the dgim
        algorithm.
        abs(c-e) < error_rate * c
        :type error_rate: float
        """
        self.N = N

        if not (0 < error_rate <= 1):
            raise ValueError(
                    "Invalid value for error_rate: {}. Error rate should be in ]0, 1].".format(error_rate))

        self.error_rate = error_rate

        #the maximum number of buckets of the same size
        self.r = math.ceil(1/error_rate)
        self.r = max(self.r, 2)

        # the datastructure to store the buckets
        # it is an array of queues
        # queue[i] stores the timestamp of the bucket of size 2^i
        # in descending order
        # this structure makes it easy to :
        # - know how many bucket of the same size there is
        # - update a queue of bucket
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
        :param elt: the latest element of the stream
        :type elt: bool
        """
        if self.N == 0:
            return
        self.timestamp = (self.timestamp + 1) % (2 * self.N)
        #check if oldest bucket should be removed
        if self.oldest_bucket_timestamp >= 0 and self.is_bucket_too_old(self.oldest_bucket_timestamp):
            self.drop_oldest_bucket()
        if elt is not True:
            #nothing to do
            return

        carry_over = self.timestamp
        if self.oldest_bucket_timestamp == -1:
            self.oldest_bucket_timestamp = self.timestamp
        for queue in self.queues:
            queue.appendleft(carry_over)
            if len(queue) <= self.r:
                break
            last = queue.pop()
            second_last = queue.pop()
            # merge last two buckets.
            carry_over = second_last
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
        """Returns an estimate of the number of "True"
        in the last N elements of the stream.
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
