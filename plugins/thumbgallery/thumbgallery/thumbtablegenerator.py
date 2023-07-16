# -*- coding: utf-8 -*-

from outwiker.api.core.attachment import Attachment
from outwiker.api.core.defines import PAGE_ATTACH_DIR

from .basethumbgenerator import BaseThumbGenerator


class ThumbTableGenerator(BaseThumbGenerator):
    """
    Создание списка превьюшек в виде таблицы
    """

    def __init__(self, items, thumbsize, parser, cols):
        """
        items - список кортежей, описывающие прикрепленные файлов,
            из которых надо сделать превьюшки (первый элемент),
            и комментарии к ним (второй элемент)
        thumbsize - размер превьюшек (по наибольшей стороне)
        parser - экземпляр википарсера (Parser)
        cols - количество столбцов таблицы
        """
        super().__init__(items, thumbsize, parser)
        self._cols = cols

        # Обертка для галереи в целом
        self._fullTemplate = '<table class="thumbgallery-table">{content}</table>'

        self._rowTemplate = '<tr class="thumbgallery-row">{row}</tr>'

        self._singleThumbTemplate = '<td class="thumbgallery-td"><div class="thumbgallery-table-item"><div class="thumbgallery-table-image">{thumbimage}</div><div class="thumbgallery-table-comment">{comment}</div></div></td>'

        self._style = """<!-- Begin thumbgallery styles -->
<style>
    table.thumbgallery-table {
        border: 1px solid #DDD;
        }

    div.thumbgallery-table-item{
		padding: 1em;
	}

	td.thumbgallery-td {
        border: 1px solid #DDD;
		text-align: center;
	}

    div.thumbgallery-table-image{
		text-align: center;
	}

	div.thumbgallery-table-comment{
		text-align: center;
		height: 100%;
	}
</style>
<!-- End thumbgallery styles -->"""

    def generate(self):
        """
        Возвращает строку, содержащую HTML-текст галереи
        """
        if self._style not in self._parser.head:
            self._parser.appendToHead(self._style)

        resultContent = self._generateRows(self._items)

        return self._fullTemplate.format(content=resultContent)

    def _generateItemText(self, item):
        """
        Возвращает оформленный элемент таблицы
        """
        image = (
            """<a href="{attachdir}/{imagename}"><img src="{thumbpath}"/></a>""".format(
                attachdir=PAGE_ATTACH_DIR,
                imagename=item[0].replace("\\", "/"),
                thumbpath=self._getThumbnail(self._parser.page, item[0]),
            )
        )

        return self._singleThumbTemplate.format(thumbimage=image, comment=item[1])

    def _generateRows(self, items):
        """
        Возвращает список строк, описывающих строки таблицы
        """
        itemsText = [self._generateItemText(item) for item in self._items]

        # Разрежем список на несколько списков, длиной self._cols
        splitItems = [
            itemsText[i : i + self._cols] for i in range(0, len(itemsText), self._cols)
        ]

        rows = [self._rowTemplate.format(row="".join(row)) for row in splitItems]
        return "".join(rows)
