#!/usr/bin/python
# -*- coding: UTF-8 -*-

from string import Template
import os.path


class PageListGenerator (object):
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


    def generate (self, fname):
        """
        Создать файл (с имемени fname), содержащий список страниц
        """
        pageList = []
        self.__addpage (pageList, self.__rootpage)

        result = self.__prepareResult (u"<br>\n".join (pageList) )

        with open (fname, "w") as fp:
            fp.write (result)


    def __prepareResult (self, result):
        template = self.__loadTemplate()
        resultcontent = template.substitute (content=result)
        return resultcontent
        

    def __loadTemplate (self):
        """
        Загрузить шаблон.
        """
        templatedir = u"templates"

        templateFileName = os.path.join (os.path.dirname (__file__), 
                templatedir, 
                self.__contenttemplate)

        with open (templateFileName) as fp:
            template = unicode (fp.read(), "utf8")

        return Template (template)


    def __addpage (self, pageList, page):
        template = u"<a href='{url}'>{title}</a>"

        if "title" in dir (page):
            pageList.append (template.format (url=self.__renames[page] + ".html", title=page.title) )

        for child in page.children:
            self.__addpage (pageList, child)
