import threading
import time

class StoppableThread(threading.Thread):
    def __init__(self, target=None, args=(), kwargs=None):
        super(StoppableThread, self).__init__()
        self.stop_requested = False
        self.target = target
        self.args = args
        if kwargs is None:
            self.kwargs = {}
        else:
            self.kwargs = kwargs

    def run(self):
        while not self.stop_requested:
            if self.target:
                # Call the target function provided by the user
                self.target(*self.args, **self.kwargs)
            # Adjust the sleep as necessary based on your application's requirements
            time.sleep(1)

    def stop(self):
        self.stop_requested = True




