# -*- coding: UTF-8 -*-

import html
import os.path

from outwiker.utilites.textfile import writeTextFile

from .template import loadTemplate


class IndexContentGenerator (object):
    """
    Класс для создания списка страниц в виде HTML
    """
    def __init__ (self, rootpage, renames):
        """
        rootpage - корневая страница, с которой начинается экспорт
        renames - словарь соответствия страницы (ключ) и ее имени после экспорта (значение)
        """
        self.__rootpage = rootpage
        self.__renames = renames

        self.__contenttemplate = u"content.html"
        self.__indent = u"    "


    def generate (self, fname):
        """
        Создать файл (с имемени fname), содержащий список страниц
        """
        resultList = []

        resultList.append ("<ul>")
        self.__addpage (resultList, self.__rootpage, 1)
        resultList.append ("</ul>")

        finalresult = self.__prepareResult (u"\n".join (resultList))

        writeTextFile(fname, finalresult)


    def __prepareResult (self, result):
        template = loadTemplate(self.__contenttemplate)
        resultcontent = template.substitute (content=result)
        return resultcontent


    def __getIcon (self, page):
        """
        Возвращает путь до сохраненной иконки или None, если ее нет
        """
        if page.icon is None:
            return

        dirname = self.__renames[page]
        iconpath = u"{dirname}/{iconname}".format (dirname=dirname,
                                                   iconname=os.path.basename (page.icon))

        return iconpath


    def __prepareUrl (self, url):
        """
        Заменить в ссылке "опасные" символы
        """
        result = url.replace ("%", "%25")
        result = result.replace ("#", "%23")
        result = result.replace ("?", "%3F")
        result = result.replace (" ", "%20")
        return result


    def __getPageLink (self, page, level):
        """
        Метод возвращает оформленную ссылку на страницу
        """
        template = u"{indent}<li><a href='{url}' target='main'>{title}</a></li>"

        templateIcon = u"{indent}<li><span style='white-space:nowrap'><a href='{url}' target='main'><img src='{iconpath}'></a><a href='{url}' target='main'>{title}</a></span></li>"

        if page.icon is None:
            itemstring = template.format (indent=self.__indent * level,
                                          url=self.__prepareUrl (self.__renames[page] + ".html"),
                                          title=html.escape(page.title))
        else:
            iconpath = self.__getIcon (page)

            itemstring = templateIcon.format (indent=self.__indent * level,
                                              url=self.__prepareUrl (self.__renames[page] + ".html"),
                                              title=html.escape(page.title),
                                              iconpath=self.__prepareUrl (iconpath))

        return itemstring


    def __addpage (self, resultList, page, level):
        if page in list(self.__renames.keys()):
            if "title" in dir (page):
                itemstring = self.__getPageLink (page, level)
                resultList.append (itemstring)

        if len (page.children) != 0:
            resultList.append (self.__indent * level + "<ul>")

            for child in page.children:
                self.__addpage (resultList, child, level + 1)

            resultList.append (self.__indent * level + "</ul>")
