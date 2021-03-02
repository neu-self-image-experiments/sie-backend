import thread
import queue

from concurrent.futures import ThreadPoolExecutor

SLEEP_TIME = 2
FILE_DIR = "./test_data/"


def performance_test(num_thread):
    # To record the start and end times for each thread
    start_queue = queue.Queue()
    end_queue = queue.Queue()

    with ThreadPoolExecutor(max_workers=num_thread) as executor:

        for i in range(num_thread):
            t = thread(i, SLEEP_TIME, start_queue, end_queue)
            executor.submit(t.run, (FILE_DIR, str(i) + ".jpg"))

    min_start_time = start_queue.get()
    max_end_time = end_queue.get()

    while start_queue.empty() is False:
        min_start_time = min(min_start_time, start_queue.get())
    
    while end_queue.empty() is False:
        max_end_time = max(max_end_time, end_queue.get())
    
    print("The resulting throughput of the program is {}".format(float((max_end_time - min_start_time) / num_thread)))
