# -*- coding: utf-8 -*-

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR

from .basethumbgenerator import BaseThumbGenerator


class ThumbStreamGenerator (BaseThumbGenerator):
    """
    Создание списка превьюшек в виде простой последовательсности
    (не в виде таблицы)
    """
    def __init__(self, items, thumbsize, parser):
        """
        items - список кортежей, описывающие прикрепленные файлов,
            из которых надо сделать превьюшки (первый элемент),
            и комментарии к ним (второй элемент)
        thumbsize - размер превьюшек (по наибольшей стороне)
        parser - экземпляр википарсера (Parser)
        """
        super().__init__(items, thumbsize, parser)

        # Обертка для галереи в целом
        self._fullTemplate = u'<div class="thumblist">{content}</div>'

        # Обертка для одной картинки
        self._singleThumbTemplate = u'<div class="thumblist-thumb"><div class="thumblist-image"><A HREF="{attachdir}/{imagename}"><IMG SRC="{thumbpath}"/></A></div></div>'

        self._style = """<!-- Begin Thumblist styles -->
<style>
    div.thumblist {
        }

    div.thumblist-thumb {
        display: inline;
        }

    div.thumblist-image {
        display: inline;
        }

    div.thumblist-image img{
		padding: 0.3em 0.3em 0.5em 0.5em;
        }
</style>
<!-- End Thumblist styles -->"""

    def generate(self):
        """
        Возвращает строку, содержащую HTML-текст галереи
        """
        resultContent = u"".join([self._singleThumbTemplate.format(attachdir=PAGE_ATTACH_DIR,
                                                                   imagename=item[0],
                                                                   thumbpath=self._getThumbnail(self._parser.page, item[0]))
                                  for item in self._items])

        if self._style not in self._parser.head:
            self._parser.appendToHead(self._style)

        return self._fullTemplate.format(content=resultContent)
