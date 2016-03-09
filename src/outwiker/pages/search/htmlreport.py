# -*- coding: UTF-8 -*-

import cgi

from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.system import getOS


class HtmlReport (object):
    """
    Класс для генерации HTML-а, для вывода найденных страниц
    """
    def __init__ (self, pages, searchPhrase, searchTags, application):
        """
        pages - список найденных страниц
        searchPhrase - искомая фраза
        searchTags - теги, которые участвуют в поиске
        """
        self.__pages = pages
        self.__searchPhrase = searchPhrase
        self.__searchTags = searchTags
        self.__application = application

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
        item = u'<b><a href="/%s">%s</a></b>' % (cgi.escape (page.subpath, True), page.title)
        if page.parent.parent is not None:
            item += u" (%s)" % page.parent.subpath

        item += u"<br>" + self.generatePageInfo (page) + "<p></p>"

        result = u"<li>%s</li>\n" % item

        return result


    def generatePageInfo (self, page):
        tags = self.generatePageTags (page)
        date = self.generateDate (page)

        pageinfo = u"<font size='-1'>{tags}<br>{date}</font>".format (tags=tags, date=date)
        return pageinfo


    def generateDate (self, page):
        config = GeneralGuiConfig (self.__application.config)
        dateStr = unicode (page.datetime.strftime (config.dateTimeFormat.value),
                           getOS().filesEncoding)
        result = _(u"Last modified date: {0}").format (dateStr)

        return result


    def generatePageTags (self, page):
        """
        Создать список тегов для страницы
        """
        result = _(u"Tags: ")
        for tag in page.tags:
            result += self.generageTagView (tag) + u", "

        if result.endswith (", "):
            result = result [: -2]

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
