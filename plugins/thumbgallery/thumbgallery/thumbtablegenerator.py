#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ThumbTableGenerator (object):
    """
    Создание списка превьюшек в виде таблицы
    """
    def __init__ (self, items, thumbsize, parser, cols):
        """
        items - список кортежей, описывающие прикрепленные файлов, из которых надо сделать превьюшки (первый элемент), и комментарии к ним (второй элемент)
        thumbsize - размер превьюшек (по наибольшей стороне)
        parser - экземпляр википарсера (Parser)
        cols - количество столбцов таблицы
        """
        self._items = items
        self._thumbsize = thumbsize
        self._parser = parser
        self._cols = cols

        # Обертка для галереи в целом
        self._fullTemplate = u'<table class="thumblist-table">{content}</table>'

        self._rowTemplate = u'<tr class="thumblist-row">{row}</tr>'

        self._singleThumbTemplate = u'<td class="thumblist-td"><div class="thumblist-table-item"><div class="thumblist-table-image">{thumbimage}</div><div class="thumblist-table-comment">{comment}</div></div></td>'

        self._style ="""<!-- Begin Thumblist styles -->
<style>
    table.thumblist-table {
        border: 1px solid #DDD;
        }

    div.thumblist-table-item{
		padding: 1em;
	}

	td.thumblist-td {
        border: 1px solid #DDD;
		text-align: center;
	}

    div.thumblist-table-image{
		text-align: center;
	}

	div.thumblist-table-comment{
		text-align: center;
		height: 100%;
	}
</style>
<!-- End Thumblist styles -->"""


    def generate (self):
        """
        Возвращает строку, содержащую HTML-текст галереи
        """
        if self._style not in self._parser.head:
            self._parser.appendToHead (self._style)

        rows = self._generateRows (self._items)

        resultContent = self._parser.parseWikiMarkup (rows)
        return self._fullTemplate.format (content = resultContent)

    
    def _generateItemText (self, item):
        """
        Возвращает оформленный элемент таблицы
        """
        image = u"%thumb maxsize={maxsize}%Attach:{fname}%%".format (maxsize=self._thumbsize, fname=item[0])

        return self._singleThumbTemplate.format (thumbimage=image, comment=item[1])


    def _generateRows (self, items):
        """
        Возвращает список строк, описывающих строки таблицы
        """
        itemsText = [self._generateItemText (item) for item in self._items]

        # Разрежем список на несколько списков, длиной self._cols
        splitItems = [itemsText[i: i + self._cols] for i in range(0, len(itemsText), self._cols)]

        rows = [self._rowTemplate.format (row = u"".join (row)) for row in splitItems]
        return u"".join (rows)
