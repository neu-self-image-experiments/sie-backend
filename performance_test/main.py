import thread
import queue

from concurrent.futures import ThreadPoolExecutor

SLEEP_TIME = 2


def performance_test(num_thread):
    # To record the start and end times for each thread
    start_queue = queue.Queue()
    end_queue = queue.Queue()

    with ThreadPoolExecutor(max_workers=num_thread) as executor:

        for i in range(num_thread):
            t = thread(i, SLEEP_TIME, start_queue, end_queue)
            executor.submit(t.run)

    # TODO iterate over two queues and find the smallest
    # start time and largest end time, to calculate the
    # throughput
