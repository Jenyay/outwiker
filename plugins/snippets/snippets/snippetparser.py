# -*- coding: UTF-8 -*-

from outwiker.utilites.textfile import readTextFile


class SnippetParser(object):
    def __init__(self, fname):
        self._fname = fname
        self._content = readTextFile(fname)

    def process(self, **kwargs):
        result = self._content
        if result.endswith(u'\n'):
            result = result[:-1]

        return result
