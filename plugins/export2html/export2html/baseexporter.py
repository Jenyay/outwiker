# -*- coding: UTF-8 -*-

import os
import os.path
import shutil
from abc import ABCMeta, abstractmethod

from outwiker.core.attachment import Attachment
from .exceptions import FileAlreadyExists, FolderNotExists


class BaseExporter (object):
    """
    Базовый класс для экспорта разных типов страниц
    """
    __meta__ = ABCMeta

    def __init__ (self, page):
        self._page = page

        from .i18n import _
        global _


    @property
    def page (self):
        return self._page


    @abstractmethod
    def export (self, outdir, exportname, imagesonly, alwaisOverwrite):
        pass


    def _exportContent (self,
                        page,
                        content,
                        exportname,
                        outdir,
                        imagesonly,
                        alwaisOverwrite):
        """
        Экспортировать обработанное содержимое и вложения
        """
        exportfile = os.path.join (outdir, exportname + ".html")
        exportdir = os.path.join (outdir, exportname)

        if not alwaisOverwrite and os.path.exists (exportfile):
            raise FileAlreadyExists (_(u"File {0} already exists").format (exportfile))

        if not os.path.exists (outdir):
            raise FolderNotExists (_(u"Folder {0} not exists").format (outdir))

        with open (exportfile, "wb") as fp:
            fp.write (content.encode ("utf8"))

        self.__exportAttaches (page, exportdir, imagesonly, alwaisOverwrite)
        self.__exportIcon (page, exportdir, alwaisOverwrite)


    def __exportAttaches (self, page, exportdir, imagesonly, alwaisOverwrite):
        """
        Экспортировать вложения
        """
        if not os.path.exists (exportdir):
            os.mkdir (exportdir)

        attach = Attachment (page)

        for fname in attach.attachmentFull:
            if not imagesonly or self.__isImage (fname):
                newpath = os.path.join (exportdir, os.path.basename (fname))
                self.__checkForExists (newpath, alwaisOverwrite)
                self.__copy (fname, newpath)


    def __exportIcon (self, page, exportdir, alwaisOverwrite):
        assert os.path.exists (exportdir)

        if page.icon is None:
            return

        newIconPath = os.path.join (exportdir, os.path.basename (page.icon))
        self.__checkForExists (newIconPath, alwaisOverwrite)
        self.__copy (page.icon, newIconPath)


    def __delete (self, path):
        """
        Удалить файл или директорию
        """
        if os.path.isdir (path):
            shutil.rmtree (path)
        else:
            os.remove (path)


    def __copy (self, src, dsc):
        """
        Скопировать файл или директорию
        """
        if os.path.isdir (src):
            shutil.copytree (src, dsc)
        else:
            shutil.copy (src, dsc)


    def __checkForExists (self, path, alwaisOverwrite):
        """
        Проверка на то, что файл существует.
        Если alwaisOverwrite == True, то существующий файл удаляется, иначе бросается исключение
        """
        if os.path.exists (path):
            if not alwaisOverwrite:
                raise FileAlreadyExists (_(u"File {0} already exists").format (path))
            else:
                self.__delete (path)


    def __isImage (self, fname):
        images = [".gif", ".png", ".jpeg", ".jpg", ".tif", ".tiff"]
        isimage = False
        for extension in images:
            if fname.endswith (extension):
                isimage = True
                break

        if os.path.basename (fname).lower() == u"__thumb":
            isimage = True

        return isimage
