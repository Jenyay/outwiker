# -*- coding: UTF-8 -*-

import time


class Timer (object):
    def __init__ (self):
        self.start()


    def start (self):
        self._start = time.clock()


    def getTimeInterval (self):
        return time.clock() - self._start
