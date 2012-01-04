#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.tree import WikiDocument


class LongNameGenerator (object):
    """
    Класс для создания имени экспортируемых страниц. Имена включают в себя заголовки родительских страниц
    """
    def __init__ (self, rootpage):
        """
        rootpage - корневая страница для экспортируемой ветки
        """
        self._root = rootpage


    def getName (self, page):
        """
        Получить имя файла и директории для экспортируемой страницы page
        """
        return self.__getExportName (self._root, page)


    def __getExportName (self, root, page):
        if root.getTypeString() == WikiDocument.getTypeString():
            exportname = os.path.basename (root.path) + "_" + page.subpath.replace ("/", "_")
        else:
            if page == root:
                exportname = page.title
            else:
                exportname = self.__getSubpathExportName(root, page)
        return exportname


    def __getSubpathExportName(self, root, page):
        assert page.subpath.startswith (root.subpath)
        exportname = page.subpath.replace (root.subpath, u"", 1)

        assert len (exportname) > 0
        if exportname[0] == "/":
            exportname = exportname[1:]

        exportname = root.title + "_" + exportname.replace ("/", "_")
        return exportname
