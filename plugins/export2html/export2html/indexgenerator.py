#!/usr/bin/python
# -*- coding: UTF-8 -*-

from string import Template
import os.path

from contentgenerator import ContentGenerator


class IndexGenerator (object):
    """
    Класс для создания списка экспортируемых страниц
    """
    def __init__ (self, rootpage, renames):
        """
        rootpage - страница, с которой начинается экспортирование ветки.ы
        renames - словарь, который дает соответствие между страницей (ключ) и тем, как называется файл (без расширения) и директория, созданные при экспорте этой страницы.
        """
        self.__rootpage = rootpage
        self.__renames = renames


    def generatefiles (self, indexfname, contentfname):
        """
        Создать файлы с оглавлением
        outdir - папка, где должны быть созданы файлы
        indexfname - имя главного файла содержания (index.html)
        contentfname - имя файла со ссылками на страницы
        """
        # Создать экземпляр класса, оформляющий список страниц
        contentgenerator = ContentGenerator (self.__rootpage, self.__renames)
        contentgenerator.generate (contentfname)

        # Создать файл с фреймами, отображающий все оглавление
        indextemplate = self.__loadTemplate (u"index.html")
        indexresult = indextemplate.substitute (contentfname=os.path.basename (contentfname) )

        with open (indexfname, "w") as fp:
            fp.write (indexresult)


    def __loadTemplate (self, fname):
        """
        Загрузить шаблон.
        """
        templatedir = u"templates"

        templateFileName = os.path.join (os.path.dirname (__file__), 
                templatedir, 
                fname)

        with open (templateFileName) as fp:
            template = unicode (fp.read(), "utf8")

        return Template (template)
