import threading

'''
    This is the counter
'''

class counter():
    def __init__(self, count):
        self.count = 0
        self.lock = threading.Lock()

    def dec():
        with self.lock:
            count -= 1
    
    def getCount():
        return self.count