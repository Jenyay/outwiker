#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import shutil

from outwiker.core.attachment import Attachment
from .exceptions import FileAlreadyExists


class BaseExporter (object):
    """
    Базовый класс для экспорта разных типов страниц
    """
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
            raise FileAlreadyExists (_(u"File {0} already exists").format (exportfile) )

        with open (exportfile, "wb") as fp:
            fp.write (content.encode ("utf8"))

        self.__exportAttaches (page, exportdir, imagesonly)


    def __exportAttaches (self, page, exportdir, imagesonly):
        """
        Экспортировать вложения
        """
        if not os.path.exists (exportdir):
            os.mkdir (exportdir)

        attach = Attachment (page)

        for fname in attach.attachmentFull:
            if not imagesonly or self.__isImage (fname):
                newpath = os.path.join (exportdir, os.path.basename (fname) )
                shutil.copy (fname, newpath)


    def __isImage (self, fname):
        images = [".gif", ".png", ".jpeg", ".jpg", ".tif", ".tiff"]
        isimage = False
        for extension in images:
            if fname.endswith (extension):
                isimage = True
                break

        return isimage
