# -*- coding: UTF-8 -*-

import os.path

from .indexcontentgenerator import IndexContentGenerator
from .template import loadTemplate


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

        self.__templatename = u"index.html"


    def generatefiles (self, indexfname, contentfname):
        """
        Создать файлы с оглавлением
        outdir - папка, где должны быть созданы файлы
        indexfname - имя главного файла содержания (index.html)
        contentfname - имя файла со ссылками на страницы
        """
        # Создать экземпляр класса, оформляющий список страниц
        contentgenerator = IndexContentGenerator (self.__rootpage, self.__renames)
        contentgenerator.generate (contentfname)

        # Создать файл с фреймами, отображающий все оглавление
        indextemplate = loadTemplate (self.__templatename)
        indexresult = indextemplate.substitute (contentfname=os.path.basename (contentfname))

        with open (indexfname, "w") as fp:
            fp.write (indexresult)
