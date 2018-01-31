# -*- coding: utf-8 -*-

import os
import os.path
import shutil

from outwiker.core.exceptions import ReadonlyException
from outwiker.core.defines import PAGE_ATTACH_DIR
from . import events


class Attachment(object):
    """
    Класс для работы с прикрепленными файлами
    """
    def __init__(self, page):
        """
        page - страница, для которой интересуют прикрепленные файлы
        """
        self.page = page

    def getAttachPath(self, create=False):
        """
        Возвращает путь до папки с прикрепленными файлами
        create - создать папку для прикрепленных файлов,
        если она еще не создана?
        """
        path = os.path.join(self.page.path, PAGE_ATTACH_DIR)

        if create and not os.path.exists(path):
            os.mkdir(path)

        return path

    @property
    def attachmentFull(self):
        """
        Возвращает список прикрепленных файлов.
        Пути до файлов полные
        """
        path = self.getAttachPath()
        return [os.path.join(path, fname)
                for fname in self.getAttachRelative()]

    def getAttachRelative(self, dirname="."):
        """
        Возвращает список прикрепленных файлов
        (только имена файлов без путей относительно директории dirname).
        dirname - поддиректория в PAGE_ATTACH_DIR,
        где хотим получить список файлов
        """
        path = self.getAttachPath()

        if not os.path.exists(path):
            return []

        fullpath = os.path.join(path, dirname)

        return os.listdir(fullpath)

    def attach(self, files):
        """
        Прикрепить файлы к странице
        files -- список файлов (или папок), которые надо прикрепить
        """
        if self.page.readonly:
            raise ReadonlyException

        attachPath = self.getAttachPath(True)

        for name in files:
            if os.path.isdir(name):
                basename = os.path.basename(name)
                shutil.copytree(name, os.path.join(attachPath, basename))
            else:
                shutil.copy(name, attachPath)

        self.page.updateDateTime()
        self.page.root.onPageUpdate(self.page,
                                    change=events.PAGE_UPDATE_ATTACHMENT)

    def removeAttach(self, files):
        """
        Удалить прикрепленные файлы
        files - список имен файлов (путей относительно папки PAGE_ATTACH_DIR)
        """
        if self.page.readonly:
            raise ReadonlyException

        attachPath = self.getAttachPath(True)

        for fname in files:
            path = os.path.join(attachPath, fname)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except OSError:
                self.page.root.onPageUpdate(
                    self.page,
                    change=events.PAGE_UPDATE_ATTACHMENT)
                raise IOError(u"Can't remove %s" % fname)

        self.page.updateDateTime()
        self.page.root.onPageUpdate(self.page,
                                    change=events.PAGE_UPDATE_ATTACHMENT)

    @staticmethod
    def sortByName(fname):
        """
        Deprecated. Please use kye=str.lower instead.

        Метод для сортировки файлов по имени
        Key stile method to sort files by name.

        Args:
            fname: path to the file.
        Returns:
            fname.lower()
        """
        return fname.lower()

    @staticmethod
    def sortByExt(fname):
        """
        Метод для сортировки файлов по расширению
        Key stile method to sort files by extension.
        If the extension is equivalent for 2 files they will be sorted by name.

        Args:
            fname: path to the file.
        Returns:
            (file_ext, file_name)
        """
        name, ext = os.path.splitext(os.path.basename(fname).lower())

        return ext, name

    @staticmethod
    def sortByDate(full_file_path):
        """
        Метод для сортировки файлов по дате последней модификации.
        Key stile method to sort files by last modified date.
        If the date is equivalent for 2 files they will be sorted by name.

        Args:
            full_file_path: full path to the existing file.
        Returns:
            (os.stat().st_mtimem, full_file_path.lower())
        """
        stat = os.stat(full_file_path)

        return stat.st_mtime, full_file_path.lower()

    @staticmethod
    def sortBySize(full_file_path):
        """
        Метод для сортировки файлов по размеру файла.
        Key stile method to sort files by file size.
        If the size is equivalent for 2 files they will be sorted by name.

        Args:
            full_file_path: full path to the existing file.
        Returns:
            (os.stat().st_mtimem, full_file_path.lower())
        """
        stat = os.stat(full_file_path)

        return stat.st_size, full_file_path.lower()

    def sortBySizeRelative(self, relative_file_path):
        """
        Метод для сортировки файлов по размеру файла.
        Key stile method to sort files by file size.
        If the size is equivalent for 2 files they will be sorted by name.

        Args:
            relative_file_path: relative path to the file.
        Returns:
            (os.stat().st_mtimem, relative_file_path.lower())
        """
        stat = os.stat(self.getFullPath(relative_file_path))

        return stat.st_size, relative_file_path.lower()

    def sortByDateRelative(self, relative_file_path):
        """
        Метод для сортировки файлов по дате.
        Key stile method to sort files by last modified date.
        If the date is equivalent for 2 files they will be sorted by name.

        Args:
            relative_file_path: relative path to the file.
        Returns:
            (os.stat().st_mtimem, relative_file_path.lower())
        """
        stat = os.stat(self.getFullPath(relative_file_path))

        return stat.st_mtime, relative_file_path.lower()

    def getFullPath(self, fname, create=False):
        """
        Возвращает полный путь до прикрепленного файла с именем fname.
        Файл fname не обязательно должен существовать.
        create - нужно ли создавать папку PAGE_ATTACH_DIR,
        если ее еще не существует?
        """
        return os.path.join(self.getAttachPath(create), fname)
