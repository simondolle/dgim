import time
import math
import matplotlib.pyplot as plt

from dgim.dgim import Dgim
from dgim.utils import generate_random_stream

def measure_update_time(N, iterations):
    dgim = Dgim(N)
    # initialization
    for elt in generate_random_stream(N):
        dgim.update(elt)
    time_start = time.time()
    bucket_count = 0
    for elt in generate_random_stream(iterations):
        dgim.update(elt)
        bucket_count += len(dgim.buckets)
    time_stop = time.time()
    return time_stop - time_start, bucket_count/float(iterations)

def run_update_benchmark():
    times = []
    bucket_counts = []
    for i in range(24):
        time, bucket_count = measure_update_time(2 ** i, iterations=100000)
        print 2 ** i, time
        times.append((2 ** i, time))
        bucket_counts.append(bucket_count)
    plt.plot([n for n, time in times], [time for n, time in times])
    #plt.plot(bucket_counts, [time for n, time in times])
    plt.show()

if __name__ == "__main__":
    run_update_benchmark()
