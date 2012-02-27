#!/usr/bin/python
# -*- coding: UTF-8 -*-

from pagelistgenerator import PageListGenerator


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


    def generatefiles (self, indexfname, treefname):
        """
        Создать файлы с оглавлением
        outdir - папка, где должны быть созданы файлы
        indexfname - имя главного файла содержания (index.html)
        treefname - имя файла со ссылками на страницы
        """
        ## Создать файл со списком экспортируемых страниц

        # Создать экземпляр класса, оформляющий список страниц
        pagelistgenerator = PageListGenerator (self.__rootpage, self.__renames)
        pagelistgenerator.generate (treefname)

        ## Создать файл с фреймами, отображающий все оглавление
        pass
