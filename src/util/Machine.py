#!/usr/bin/env python3

import time
import threading


class Machine(object):
    def __init__(self, executor = None):
        self._started = False
        self._thread = None
        self._lock = threading.Lock()
        self._executor = executor

    def is_started(self):
        with self._lock:
            return self._started

    def start(self, duration):
        with self._lock:
            self._started = True
        self._thread = threading.Thread(target=Machine.run, args=(self, duration))
        self._thread.start()

    def run(self, duration):
        begin_time = time.time()
        while self.is_started() and time.time() - begin_time <= duration:
            local_time = time.localtime()
            self._executor(local_time)
            time.sleep(1)


    def stop(self):
        with self._lock:
            self._started = False
        self._thread.join()

if __name__ == '__main__':
    machine = Machine(lambda local_time : print("Laundry service at {}".format(time.strftime("%H:%M:%S", local_time))))
    machine.start(5)
    time.sleep(3)
    machine.stop()