#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os


class HtmlReport (object):
    """
    Класс для генерации HTML-а, для вывода найденных страниц
    """
    def __init__ (self, pages, searchPhrase, searchTags):
        """
        pages - список найденных страниц
        searchPhrase - искомая фраза
        searchTags - теги, которые участвуют в поиске
        """
        self.__pages = pages
        self.__searchPhrase = searchPhrase
        self.__searchTags = searchTags

    def generate (self):
        """
        Сгенерить отчет
        """
        shell = u"""<html>
                <head>
                <meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
                </head>
                <body>
                <ol type='1'>
                %s
                </ol>
                </body>
                </html>"""

        items = u""

        for page in self.__pages:
            items += self.generataPageView (page)

        result = shell % items
        return result
    

    def generataPageView (self, page):
        """
        Вернуть представление для одной страницы
        """
        item = "<b><a href='/%s'>%s</a></b>" % (page.subpath, page.title)
        if page.parent.parent != None:
            item += u" (%s)" % page.parent.subpath

        item += "<br>" + self.generatePageTags (page) + "<p>"

        result = u"<li>%s</li>\n" % item

        return result


    def generatePageTags (self, page):
        """
        Создать список тегов для страницы
        """
        result = "<FONT SIZE='-1'>" + _(u"Tags: ")
        for tag in page.tags:
            result += self.generageTagView (tag) + u", "

        if result.endswith (", "):
            result = result [: -2]

        result += "</FONT>"

        return result


    def generageTagView (self, tag):
        """
        Оформление для одного тега
        """
        if tag in self.__searchTags:
            style = u"font-weight: bold; background-color: rgb(255,255,36);"
            return u"<span style='{style}'>{tag}</span>".format (style=style, tag=tag)
        else:
            return tag
