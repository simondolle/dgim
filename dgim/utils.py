import random


def generate_random_stream(length):
    """Generate a random stream of booleans.
    :param length: the stream length
    :type length: int
    :returns: iterator
    """
    for i in range(length):
        yield bool(random.randint(0, 1))
