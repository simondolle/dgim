import itertools

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
        self.buckets = []
        self.timestamp = 0

    def update(self, elt):
        """Update the stream with one element.
        The element can be either 0 or 1.
        :param elt: the latest element of the stream
        :type elt: int
        """
        #check if oldest bucket should be removed
        if (len(self.buckets) > 0 and
                self.buckets[-1].most_recent_timestamp < self.timestamp - self.N):
            self.buckets = self.buckets[:-2]
        if elt != 1:
            self.timestamp += 1
            return
        reminder = Bucket(self.timestamp, 1)
        new_buckets = []
        for k, crt_buckets in itertools.groupby(self.buckets, key=lambda x: x.one_count):
            if reminder is not None:
                crt_buckets = [reminder] + list(crt_buckets)
            else:
                crt_buckets = list(crt_buckets)
            if len(crt_buckets) <= 2:
                reminder = None
                new_buckets.extend(crt_buckets)
            elif len(crt_buckets) == 3:
                new_buckets.append(crt_buckets[0])
                crt_buckets[1].merge(crt_buckets[2])
                reminder = crt_buckets[1]
            else:
                raise ValueError("Too many elements")
        if reminder is not None:
            new_buckets.append(reminder)
        self.buckets = new_buckets
        self.timestamp += 1

    def get_count(self):
        """Returns an estimate of the number of ones in the sliding window.
        :returns: int
        """
        #find the all the buckets which most recent timestamp is ok
        buckets = []
        for bucket in self.buckets:
            if bucket.most_recent_timestamp < self.timestamp - self.N:
                break
            buckets.append(bucket)
        if len(buckets) == 0:
            return 0
        result = 0
        last_bucket = buckets[-1]
        for bucket in buckets[0:-1]:
            result += bucket.one_count
        result += (last_bucket.one_count)/2
        return result

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
        self.most_recent_timestamp = max(
                self.most_recent_timestamp,
                other_bucket.most_recent_timestamp)
        self.one_count += other_bucket.one_count

    def __repr__(self):
        return "Bucket {}: {}".format(self.most_recent_timestamp, self.one_count)
