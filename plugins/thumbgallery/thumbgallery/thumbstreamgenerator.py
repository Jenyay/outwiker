# -*- coding: utf-8 -*-

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR

from .basethumbgenerator import BaseThumbGenerator


class ThumbStreamGenerator(BaseThumbGenerator):
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
        self._fullTemplate = '<div class="thumbgallery">{content}</div>'

        # Обертка для одной картинки
        self._singleThumbTemplate = '<div class="thumbgallery-thumb"><div class="thumbgallery-image"><a href="{attachdir}/{imagename}"><img src="{thumbpath}"/></a></div></div>'

        self._style = """<!-- Begin thumbgallery styles -->
<style>
    div.thumbgallery {
        }

    div.thumbgallery-thumb {
        display: inline;
        }

    div.thumbgallery-image {
        display: inline;
        }

    div.thumbgallery-image img{
		padding: 0.3em 0.3em 0.5em 0.5em;
        }
</style>
<!-- End thumbgallery styles -->"""

    def generate(self):
        """
        Возвращает строку, содержащую HTML-текст галереи
        """
        resultContent = "".join(
            [
                self._singleThumbTemplate.format(
                    attachdir=PAGE_ATTACH_DIR,
                    imagename=item[0].replace('\\', '/'),
                    thumbpath=self._getThumbnail(self._parser.page, item[0]),
                )
                for item in self._items
            ]
        )

        if self._style not in self._parser.head:
            self._parser.appendToHead(self._style)

        return self._fullTemplate.format(content=resultContent)
