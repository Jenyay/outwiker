# -*- coding: utf-8 -*-

import sys
import logging
import time


class LogRedirector(object):
    def __init__(self, filename, level):
        self._terminal = sys.stdout
        self._fname = filename
        self._level = level

    def init(self):
        sys.stdout = self
        sys.stderr = self

        self._firstWrite = True

        self._runTime = time.strftime(u'%Y-%m-%d %H:%M:%S')

        logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                            level=self._level)

    def write(self, message):
        self._terminal.write(message)
        if isinstance(message, unicode):
            message = message.decode('utf8')
        with open(self._fname, "a") as fp:
            if self._firstWrite:
                fp.write(u'\n\n{} - START\n'.format(self._runTime))
                self._firstWrite = False
            fp.write(message)
