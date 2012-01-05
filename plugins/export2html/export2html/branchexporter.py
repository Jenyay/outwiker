#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

from .exporterfactory import ExporterFactory
from outwiker.core.tree import WikiDocument


class BranchExporter (object):
    def __init__ (self, startpage, nameGenerator):
        self.__startpage = startpage

        # Список ошибок, возникших при экспорте
        self.__log = []
        self.__nameGenerator = nameGenerator

        # Словарь, который сохраняет, как была названа каждая страница при экспорте
        # Ключ - страница, значение - имя ее директории или файла (без расширения) после экспорта
        self.__renames = {}


    @property
    def log (self):
        return self.__log


    def export (self, outdir, imagesonly, alwaysOverwrite):
        self.__log = []
        self.__renames = {}

        self.__export (self.__startpage, 
                self.__startpage, 
                outdir, 
                imagesonly, 
                alwaysOverwrite)

        return self.log


    def __export (self, 
            page, 
            root, 
            outdir, 
            imagesonly, 
            alwaysOverwrite):
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
                exportname = self.__nameGenerator.getName (page)
                self.__renames[page] = exportname

                exporter.export (outdir, exportname, imagesonly, alwaysOverwrite)
            except BaseException, error:
                self.__log.append (u"{0}: {1}".format (page.title, unicode (error) ) )

        for child in page.children:
            self.__export (
                    child,
                    root, 
                    outdir,
                    imagesonly,
                    alwaysOverwrite)
