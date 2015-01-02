import random


def generate_random_stream(length):
    """Generate a random stream of zeros and ones.
    :param length: the stream length
    :type length: int
    :returns: iterator
    """
    for i in range(length):
        yield random.randint(0, 1)
