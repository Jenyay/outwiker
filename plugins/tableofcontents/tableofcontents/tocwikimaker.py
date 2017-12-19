# -*- coding: UTF-8 -*-

from .tocwikigenerator import TOCWikiGenerator
from .contentsparser import ContentsParser


class TocWikiMaker (object):
    """
    Класс создает текст оглавления по тексту заметки
    """
    def __init__ (self, config):
        self._generator = TOCWikiGenerator (config)


    def make (self, text):
        items = ContentsParser().parse (text)
        return self._generator.make (items)
