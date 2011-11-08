#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from .htmlcontroller import UriIdentifier


class UriIdentifierIE (UriIdentifier):
    """
    Класс для идентификации ссылок. На что ссылки
    """
    def __init__ (self, currentpage, basepath):
        """
        currentpage - страница, которая в данный момент открыта
        basepath - базовый путь для HTML-рендера
        """
        UriIdentifier.__init__ (self, currentpage, basepath)


    def _prepareHref (self, href):
        """
        Обработать ссылку, если требуется
        """
        return href


    def _findWikiPage (self, subpath):
        """
        Попытка найти страницу вики
        """
        assert self._currentPage != None

        newSelectedPage = None

        # Проверим, вдруг IE посчитал, что это не ссылка, а якорь
        # В этом случае ссылка будет выглядеть, как x:\...\{contentfile}#link
        anchor = self._findAnchor (subpath)
        if anchor != None and self._currentPage[anchor.replace("\\", "/")] != None:
            return self._currentPage[anchor.replace("\\", "/")]


        if subpath.startswith (self._currentPage.path):
            subpath = subpath[len (self._currentPage.path) + 1: ].replace ("\\", "/")
        elif len (subpath) > 1 and subpath[1] == ":":
            subpath = subpath[2:].replace ("\\", "/")
            #print subpath

        if subpath.startswith ("about:"):
            subpath = self.__removeAboutBlank (subpath).replace ("\\", "/")
        
        if len (subpath) > 0 and subpath[0] == "/":
            # Поиск страниц осуществляем только с корня
            newSelectedPage = self._currentPage.root[subpath[1:] ]
        else:
            # Сначала попробуем найти вложенные страницы с таким subpath
            newSelectedPage = self._currentPage[subpath]

            if newSelectedPage == None:
                # Если страница не найдена, попробуем поискать, начиная с корня
                newSelectedPage = self._currentPage.root[subpath]

        return newSelectedPage


    def __removeAboutBlank (self, href):
        """
        Удалить about: и about:blank из начала адреса
        """
        about_full = u"about:blank"
        about_short = u"about:"

        result = href
        if result.startswith (about_full):
            result = result[len (about_full): ]

        elif result.startswith (about_short):
            result = result[len (about_short): ]

        return result


    def _removeAnchor (self, href, currentpage):
        """
        Удалить якорь из адреса текущей загруженной страницы
        То есть из x:\\bla-bla-bla\\__content.html#anchor сделать x:\\bla-bla-bla\\__content.html
        """
        assert currentpage != None

        result = href

        if (result.startswith (currentpage.path) and
                len (result) > len (currentpage.path)):

            # Если после полного пути до страницы есть символ #
            index = result.find ("#")
            if index != -1 and index >= len (currentpage.path):
                result = result[:index]

        return result
