#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ThumbStreamGenerator (object):
    """
    Создание списка превьюшек в виде простой последовательсности (не в виде таблицы)
    """
    def __init__ (self, items, thumbsize, parser):
        """
        items - список кортежей, описывающие прикрепленные файлов, из которых надо сделать превьюшки (первый элемент), и комментарии к ним (второй элемент)
        thumbsize - размер превьюшек (по наибольшей стороне)
        parser - экземпляр википарсера (Parser)
        """
        self._items = items
        self._thumbsize = thumbsize
        self._parser = parser

        self._singleThumbTemplate = u'<div class="thumblist-thumb"><div class="thumblist-image">%thumb maxsize={maxsize}%Attach:{fname}%%</div></div>'

        self._style ="""
<style>
    div.thumblist {
        }
</style>
<style>
    div.thumblist-thumb {
        display: inline;
        }
</style>
<style>
    div.thumblist-image {
        display: inline;
        }
</style>
<style>
    div.thumblist-image img{
		padding: 0.3em 0.3em 0.5em 0.5em;
        }
</style>"""


    def generate (self):
        """
        Возвращает строку, содержащую HTML-текст галереи
        """

        wikitext = u"".join ([self._singleThumbTemplate.format (maxsize=self._thumbsize, 
            fname=item[0])
                for item in self._items])

        if self._style not in self._parser.head:
            self._parser.appendToHead (self._style)

        return self._parser.parseWikiMarkup (wikitext)
