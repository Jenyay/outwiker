#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ThumbStreamGenerator (object):
    """
    Создание списка превьюшек в виде простой последовательсности (не в виде таблицы)
    """
    def __init__ (self, files, thumbsize, parser):
        """
        files - список прикрепленных файлов, из которых надо сделать превьюшки
        thumbsize - размер превьюшек (по наибольшей стороне)
        parser - экземпляр википарсера (Parser)
        """
        self._files = files
        self._thumbsize = thumbsize
        self._parser = parser


    def generate (self):
        """
        Возвращает строку, содержащую HTML-текст галереи
        """
        singleFileTemplate = u"%thumb maxsize={maxsize}%Attach:{fname}%%"
        wikitext = u" ".join ([singleFileTemplate.format (maxsize=self._thumbsize, fname=fname)
            for fname in self._files])

        return self._parser.parseWikiMarkup (wikitext)
