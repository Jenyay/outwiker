# -*- coding: UTF-8 -*-

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
    # Depricated. Leave for compatibility with Thumbgallery plug-in.
    attachDir = PAGE_ATTACH_DIR

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
    def sortByName(fname1, fname2):
        """
        Метод для сортировки файлов по имени
        """
        fname1_lower = fname1.lower()
        fname2_lower = fname2.lower()

        if fname1_lower > fname2_lower:
            return 1
        elif fname1_lower < fname2_lower:
            return -1
        return 0

    @staticmethod
    def sortByExt(fname1, fname2):
        """
        Метод для сортировки файлов по расширению
        """
        ext1 = os.path.splitext(os.path.basename(fname1).lower())[1]
        ext2 = os.path.splitext(os.path.basename(fname2).lower())[1]

        if ext1 > ext2:
            return 1
        elif ext1 < ext2:
            return -1

        return Attachment.sortByName(fname1, fname2)

    @staticmethod
    def sortByDate(fname1, fname2):
        """
        Метод для сортировки файлов по дате.
        Пути до файлов должны быть полные
        """
        stat1 = os.stat(fname1)
        stat2 = os.stat(fname2)

        if stat1.st_mtime > stat2.st_mtime:
            return 1
        elif stat1.st_mtime < stat2.st_mtime:
            return -1

        return Attachment.sortByName(fname1, fname2)

    @staticmethod
    def sortBySize(fname1, fname2):
        """
        Метод для сортировки файлов по размеру.
        Пути до файлов должны быть полные
        """
        stat1 = os.stat(fname1)
        stat2 = os.stat(fname2)

        if stat1.st_size > stat2.st_size:
            return 1
        elif stat1.st_size < stat2.st_size:
            return -1

        return Attachment.sortByName(fname1, fname2)

    def sortBySizeRelative(self, fname1, fname2):
        """
        Метод для сортировки файлов по дате.
        Пути до файлов - относительные
        """
        stat1 = os.stat(self.getFullPath(fname1))
        stat2 = os.stat(self.getFullPath(fname2))

        if stat1.st_size > stat2.st_size:
            return 1
        elif stat1.st_size < stat2.st_size:
            return -1

        return Attachment.sortByName(fname1, fname2)

    def sortByDateRelative(self, fname1, fname2):
        """
        Метод для сортировки файлов по дате.
        Пути до файлов - относительные
        """
        stat1 = os.stat(self.getFullPath(fname1))
        stat2 = os.stat(self.getFullPath(fname2))

        if stat1.st_mtime > stat2.st_mtime:
            return 1
        elif stat1.st_mtime < stat2.st_mtime:
            return -1

        return Attachment.sortByName(fname1, fname2)

    def getFullPath(self, fname, create=False):
        """
        Возвращает полный путь до прикрепленного файла с именем fname.
        Файл fname не обязательно должен существовать.
        create - нужно ли создавать папку PAGE_ATTACH_DIR,
        если ее еще не существует?
        """
        return os.path.join(self.getAttachPath(create), fname)
