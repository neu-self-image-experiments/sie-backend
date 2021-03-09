import sys
import time
import os

from concurrent.futures import ThreadPoolExecutor
from PipelineRunnable import PipelineRunnable

SLEEP_TIME = 2
FILE_DIR = './test_data/'
"""
Defualt dirctory to store images, please make sure it
is ignored
"""


def performance_test(num_thread, file_dir, threshold):
    """
    The function does performance test on the pipeline with multithread.
    It also computes the throughput of the pipeline.
    Args:
        num_thread: The number of threads to execute.
        file_dir: The directory contians images.
        threshold: A threshold to determine whether image processing is finished.
    Returns:
        None;
    """
    # To record the start and end times for each thread
    min_start_time = time.time()
    max_end_time = time.time()
    futures = []

    if not os.path.isdir(file_dir):
        file_dir = FILE_DIR

    with ThreadPoolExecutor(max_workers=num_thread) as executor:

        for i in range(num_thread):
            pipeline_runnable = PipelineRunnable(i + 1, SLEEP_TIME, threshold)
            file_name = f"0000{i + 1}" if i < 9 else f"000{i + 1}"
            futures.append(
                executor.submit(pipeline_runnable.run, file_dir, f"{file_name}.jpg")
            )

    for future in futures:
        min_start_time = min(min_start_time, future.result()[0])
        max_end_time = max(max_end_time, future.result()[1])

    print(
        "The resulting throughput of the program is {}".format(
            float((max_end_time - min_start_time) / num_thread)
        )
    )


if __name__ == "__main__":

    num_thread = int(sys.argv[1])
    file_dir = sys.argv[2]
    threshold = int(sys.argv[3])
    performance_test(num_thread, file_dir, threshold)
