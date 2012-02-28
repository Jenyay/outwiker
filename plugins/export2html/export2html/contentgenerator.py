#!/usr/bin/python
# -*- coding: UTF-8 -*-

from string import Template
import cgi
import os.path


class ContentGenerator (object):
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
        resultList = []

        resultList.append ("<ul>")
        result = self.__addpage (resultList, self.__rootpage, 1)
        resultList.append ("</ul>")

        finalresult = self.__prepareResult (u"\n".join (resultList) )

        with open (fname, "w") as fp:
            fp.write (finalresult)


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


    def __addpage (self, resultList, page, level):
        indent = u"    "
        template = u"{indent}<li><a href='{url}'>{title}</a></li>"

        if "title" in dir (page):
            resultList.append (template.format (indent=indent * level,
                url=self.__renames[page] + ".html", 
                title=cgi.escape(page.title) ) )

        if len (page.children) != 0:
            resultList.append (indent * level + "<ul>")

            for child in page.children:
                self.__addpage (resultList, child, level + 1)

            resultList.append (indent * level + "</ul>")
