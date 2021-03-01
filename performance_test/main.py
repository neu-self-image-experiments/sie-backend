import thread

from concurrent.futures import ThreadPoolExecutor

SLEEP_TIME = 2


def main(num_thread):

    with ThreadPoolExecutor(max_workers=num_thread) as executor:
        for i in range(num_thread):
            t = thread(i, SLEEP_TIME)
            executor.submit(t.run)
