# -*- coding: UTF-8 -*-
"""Classes for parsing data"""

from abc import ABCMeta, abstractmethod
import re


class BaseSource (object):
    __meta__ = ABCMeta


    def __init__ (self, colsep):
        self._colsep = colsep
        self._rowSeparator = r'[\r\n]+'


    @abstractmethod
    def getRowsIterator (self):
        """
        Return iterator for rows
        """
        pass


    def splitItems (self, line):
        """Return list of the row elements
        line - line (row) of the data
        sep - separator between items"""
        return line


class StringSource (BaseSource):
    """
    Get data from command context
    """
    def __init__ (self, text, colsep=r'\s+'):
        super (StringSource, self).__init__(colsep)
        self._text = text


    def getRowsIterator (self):
        """
        Return iterator for rows
        """
        colsCount = None
        start = 0
        finish = False

        regexp = re.compile (self._rowSeparator, re.I | re.M)

        if len (self._text.strip()) == 0:
            raise StopIteration

        while not finish:
            match = regexp.search (self._text, start)

            if match is None:
                line = self._text[start:].strip()
                finish = True
            else:
                line = self._text[start: match.start()].strip()
                start = match.end() + 1

            if len (line) == 0:
                break

            items = self.splitItems (line)

            yield items





class FileSource (BaseSource):
    """
    Get data from text file
    """
    def __init__ (self, filename, colsep=r'\s+'):
        super (FileSource, self).__init__(colsep)
        self._filename = filename


    def getRowsIterator (self):
        """
        Return iterator for rows
        """
        pass
