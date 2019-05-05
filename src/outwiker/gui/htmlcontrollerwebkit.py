# -*- coding: utf-8 -*-

from .htmlcontroller import UriIdentifier


class UriIdentifierWebKit(UriIdentifier):
    """
    Класс для идентификации ссылок. На что ссылки
    """
    def __init__(self, currentpage, basepath):
        """
        currentpage - страница, которая в данный момент открыта
        basepath - базовый путь для HTML-рендера
        """
        super().__init__(currentpage, basepath)

    def _removeAnchor(self, href, currentpage):
        """
        Удалить якорь из адреса текущей загруженной страницы
        То есть из /bla-bla-bla/#anchor сделать /bla-bla-bla/
        """
        if currentpage is None:
            return href

        result = self.__removeFileProtokol(href)

        if (result.startswith(href) and
                len(result) > len(href)):

            # Если после полного пути до страницы есть символ #
            index = result.find("#", len(href))
            if index != -1:
                result = result[:index]

        return result

    def _prepareHref(self, href):
        result = self.__removeFileProtokol(href)
        return result

    def __removeFileProtokol(self, href):
        """
        Так как WebKit к адресу без протокола прибавляет file://,
        то избавимся от этой надписи
        """
        fileprotocol = u"file://"
        if href.startswith(fileprotocol):
            return href[len(fileprotocol):]

        return href

    def _findWikiPage(self, href):
        """
        Попытка найти страницу вики, если ссылка, на которую щелкнули
        не интернетная (http, ftp, mailto)
        """
        if self._currentPage is None:
            return None

        if href.startswith(self._basepath):
            href = href[len(self._basepath) + 1:]

        if len(href) == 0:
            return None

        newSelectedPage = None

        if href[0] == "/":
            if href.startswith(self._currentPage.root.path):
                href = href[len(self._currentPage.root.path):]

            if len(href) > 1 and href.endswith("/"):
                href = href[:-1]

        if href[0] == "/":
            # Поиск страниц осуществляем только с корня
            newSelectedPage = self._currentPage.root[href[1:]]
        else:
            # Сначала попробуем найти вложенные страницы с таким href
            newSelectedPage = self._currentPage[href]

            if newSelectedPage is None:
                # Если страница не найдена, попробуем поискать, начиная с корня
                newSelectedPage = self._currentPage.root[href]

        return newSelectedPage

    def _findAnchor(self, href):
        """
        Проверить, а не указывает ли href на якорь
        """
        basepath = self._basepath
        if not basepath.endswith('/'):
            basepath += '/'

        anchor = None
        if (href.startswith(basepath) and
                len(href) > len(basepath) and
                href[len(basepath)] == "#"):
            anchor = href[len(basepath):]

        return anchor
