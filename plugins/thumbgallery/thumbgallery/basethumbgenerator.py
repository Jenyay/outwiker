# -*- coding: utf-8 -*-

from outwiker.api.core.images import PageThumbmaker
from outwiker.api.pages.wiki.config import WikiConfig


class BaseThumbGenerator:
    """
    Базовый класс для генератора галерей
    """

    def __init__(self, items, thumbsize, parser):
        """
        items - список кортежей, описывающие прикрепленные файлов,
            из которых надо сделать превьюшки (первый элемент),
            и комментарии к ним (второй элемент)
        thumbsize - размер превьюшек (по наибольшей стороне)
        parser - экземпляр википарсера (Parser)
        """
        self._items = items
        self._parser = parser
        self._thumbsize = self._parseThumbSize(thumbsize)

    def _getThumbnail(self, page, fname):
        """
        Метод создает превьюшку и возвращает относительный путь до нее
        (относительно корня страницы)
        """
        thumbmaker = PageThumbmaker()

        return thumbmaker.createThumbByMaxSize(page, fname, self._thumbsize).replace(
            "\\", "/"
        )

    def _parseThumbSize(self, thumbsize):
        """
        Возвращает размер превьюшки. Если thumbsize (строка) не
        удается преобразовать в int, возвращает значение
        по умолчанию из настроек
        """
        try:
            return int(thumbsize)
        except ValueError:
            # Получим значение из настроек
            config = WikiConfig(self._parser.config)
            return config.thumbSizeOptions.value
