import threading

"""
This is the counter
"""


class counter:
    def __init__(self, count):
        self.count = 0
        self.lock = threading.Lock()

    def dec(self):
        with self.lock:
            self.count -= 1

    def getCount(self):
        return self.count
