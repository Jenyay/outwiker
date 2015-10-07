# -*- coding: utf-8 -*-

import sys
import logging
import time
import codecs


class LogRedirector(object):
    def __init__(self, filename):
        self._terminal = sys.stdout
        self._fname = filename


    def init (self):
        sys.stdout = self
        sys.stderr = self

        self._firstWrite = True

        self._runTime = time.strftime (u'%Y-%m-%d %H:%M:%S')
        logging.basicConfig (format = '%(asctime)s - %(levelname)s - %(message)s',
                             level = logging.WARNING)


    def write(self, message):
        self._terminal.write(message)
        with codecs.open (self._fname, "a", "utf-8") as fp:
            if self._firstWrite:
                fp.write(u'\n\n{} - START\n'.format (self._runTime))
                self._firstWrite = False
            fp.write(message)
