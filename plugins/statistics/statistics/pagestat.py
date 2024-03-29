# -*- coding: utf-8 -*-

import os
import os.path
import re

from outwiker.api.core.attachment import Attachment


class PageStat:
    """
    Класс для сбора статистики одиночной страницы
    """

    def __init__(self, page):
        """
        page - страница, для которой показывается статистика
        """
        self._page = page

        # Типы страниц, по которым можно собрать статистику
        self._supportedPages = ["html", "text", "wiki", "markdown", "web"]
        self._wordsRegExp = re.compile(r"\w+", re.M)

    def _testPageType(self):
        if self._page.getTypeString() not in self._supportedPages:
            raise TypeError

    @property
    def symbols(self):
        """
        Возвращает количество символов в тексте страницы
        """
        self._testPageType()
        return len(self._page.content)

    @property
    def symbolsNotWhiteSpaces(self):
        """
        Возвращает количество символов в тексте страницы, исключая пробелы,
        табуляции и переводы строк
        """
        self._testPageType()
        chars = [char for char in self._page.content if len(char.strip()) != 0]
        return len(chars)

    @property
    def lines(self):
        """
        Возвращает количество непустых строк в тексте страницы
        """
        self._testPageType()
        lines = [
            line for line in self._page.content.split("\n") if len(line.strip()) != 0
        ]
        return len(lines)

    @property
    def words(self):
        """
        Возвращает количество слов в тексте страницы
        """
        self._testPageType()
        return len(self._wordsRegExp.findall(self._page.content))

    @property
    def attachmentsCount(self):
        """
        Возвращает количество прикрепленных файлов, включая файлы, вложенные
        в прикрепленные директории. Сами директории не учитываются
        """
        attachment = Attachment(self._page)
        currentFiles = attachment.attachmentFull

        filesList = []
        self._getFilesListRecursive(currentFiles, filesList)

        return len(filesList)

    @property
    def attachmentsSize(self):
        """
        Возвращает общий размер прикрепленных файлов, включая файлы,
        вложенные в прикрепленные директории.
        """
        attachment = Attachment(self._page)
        currentFiles = attachment.attachmentFull

        filesList = []
        self._getFilesListRecursive(currentFiles, filesList)

        return sum([os.stat(fname).st_size for fname in filesList])

    def _getFilesListRecursive(self, currentDirFiles, filesListFlat):
        """
        currentDirFiles - список файлов и директорий в директории,
            которая будет считаться корневой
        filesListFlat - заполняемый список файлов
        """
        for fname in currentDirFiles:
            if os.path.isfile(fname):
                filesListFlat.append(fname)
            elif os.path.isdir(fname):
                currentFiles = [
                    os.path.join(fname, listItem) for listItem in os.listdir(fname)
                ]
                self._getFilesListRecursive(currentFiles, filesListFlat)
