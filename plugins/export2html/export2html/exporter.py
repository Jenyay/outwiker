#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path
import shutil

from outwiker.core.attachment import Attachment

from BeautifulSoup import BeautifulSoup

from .exceptions import HtmlNotFoundError


class Exporter (object):
    """
    Класс для экспорта страниц в HTML
    """
    def __init__ (self):
        self.__htmlFileName = u"__content.html"
        self.__attachDir = "__attach"


    def exportPage (self, 
            page,
            outdir,
            imagesonly):
        assert page != None

        if page.getTypeString() == "html" or page.getTypeString() == "wiki":
            func = self.__exportHtml
        elif page.getTypeString() == "text":
            func = self.__exportText
        else:
            return

        func (page, outdir, imagesonly)


    def __prepareContent (self, content, pagetitle):
        """
        Заменить ссылки на прикрепленные файлы
        """
        soup = BeautifulSoup (content)
        images = soup.findAll ("img")
        self.__replaceAttaches (images, "src", pagetitle)

        links = soup.findAll ("a")
        self.__replaceAttaches (links, "href", pagetitle)

        return unicode (soup.renderContents(), "utf8")


    def __replaceAttaches (self, tags, attrib, pagetitle):
        """
        Заменить ссылки на папку __attach на новую папку с вложениями
        """
        for tag in tags:
            if tag.has_key (attrib) and tag[attrib].startswith (self.__attachDir):
                tag[attrib] = tag[attrib].replace (self.__attachDir, pagetitle, 1)
                # print tag[attrib]


    def __exportHtml (self, page, outdir, imagesonly):
        assert (page.getTypeString() == "html" or 
                page.getTypeString() == "wiki" )

        # Чтение файла с содержимым
        try:
            with open (os.path.join (page.path, self.__htmlFileName) ) as fp:
                content = unicode (fp.read(), "utf8")
        except IOError:
            raise HtmlNotFoundError (_(u"{0} not found").format (self.__htmlFileName) )

        changedContent = self.__prepareContent (content, page.title)

        exportfile = os.path.join (outdir, page.title + ".html")
        exportdir = os.path.join (outdir, page.title)

        with open (exportfile, "wb") as fp:
            fp.write (changedContent.encode ("utf8"))

        self.__exportAttaches (page, exportdir, imagesonly)


    def __exportAttaches (self, page, exportdir, imagesonly):
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


    def __exportText (self, page, outdir, imagesonly):
        assert page.getTypeString() == "text"
        pass
