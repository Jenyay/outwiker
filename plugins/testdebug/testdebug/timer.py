# -*- coding: UTF-8 -*-

import time


class Timer (object):
    def __init__ (self):
        self.start()


    def start (self):
        self._start = time.perf_counter()


    def getTimeInterval (self):
        return time.perf_counter() - self._start
