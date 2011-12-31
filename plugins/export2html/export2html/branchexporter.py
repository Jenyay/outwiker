#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

from .exporterfactory import ExporterFactory
from outwiker.core.tree import WikiDocument


class BranchExporter (object):
    def __init__ (self, startpage):
        self.__startpage = startpage

        # Список ошибок, возникших при экспорте
        self.__log = []


    @property
    def log (self):
        return self.__log


    def export (self, outdir, imagesonly, alwaysOverwrite):
        self.__log = []

        self.__export (self.__startpage, 
                self.__startpage, 
                outdir, 
                imagesonly, 
                alwaysOverwrite)

        return self.log


    def __export (self, page, root, outdir, imagesonly, alwaysOverwrite):
        """
        page - страница, начиная с которой надо начать экспортирование
        root - корневая страница, откуда началось общее экспортирование (для определения имени файлов)
        outdir - директория для экспорта
        imagesonly - из вложений оставлять только картинки?
        alwaysOverwrite - перезаписывать существующие файлы?
        """
        if page.getTypeString() != WikiDocument.getTypeString():
            try:
                exporter = ExporterFactory.getExporter (page)
                exportname = self.__getExportName(root, page)
                exporter.export (outdir, exportname, imagesonly, alwaysOverwrite)
            except BaseException, error:
                self.__log.append (u"{0}: {1}".format (page.title, str (error) ) )

        for child in page.children:
            self.__export (
                    child,
                    root, 
                    outdir,
                    imagesonly,
                    alwaysOverwrite)


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
