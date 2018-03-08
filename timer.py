from threading import Thread, Event
import time


class StoppableThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.stop_event = Event()

    def stop(self):
        if self.isAlive():
            # set event to signal thread to terminate
            self.stop_event.set()
            # block calling thread until thread really has terminated
            self.join()


class IntervalTimer(StoppableThread):

    def __init__(self, interval, worker_func):
        StoppableThread.__init__(self)
        self.Interval = interval
        self._worker_func = worker_func

    def run(self):
        while not self.stop_event.is_set():
            self._worker_func()
            time.sleep(self.Interval)
