#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Действия, которые зависят от ОС, на которой запущена программа
"""

import os
import os.path
import sys
import locale
import codecs

import wx

from .pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester
from outwiker.gui.fileicons import WindowsFileIcons, UnixFileIcons


# Папки, используемые в программе
IMAGES_DIR = u"images"
STYLES_DIR = u"styles"
PLUGINS_DIR = u"plugins"

# Имя файла настроек по умолчанию
DEFAULT_CONFIG_NAME = u"outwiker.ini"

# Имя по умолчанию для папки с настройками в профиле пользователя
DEFAULT_CONFIG_DIR = u".outwiker"


class Windows (object):
    def __init__ (self):
        pass


    def init (self):
        pass


    def startFile (self, path):
        """
        Запустить программу по умолчанию для path
        """
        os.startfile (path.replace ("/", "\\"))


    @property
    def filesEncoding (self):
        return "1251"


    @property
    def inputEncoding (self):
        """
        Кодировка, используемая для преобразования нажатой клавиши в строку
        """
        return "mbcs"


    @property
    def dragFileDataObject (self):
        """
        Получить класс для перетаскивания файлов из окна OutWiker'а в другие приложения.
        Под Linux'ом wx.FileDataObject не правильно работает с Unicode
        """
        return wx.FileDataObject


    @property
    def pageTitleTester (self):
        return WindowsPageTitleTester()


    @property
    def fileIcons (self):
        return WindowsFileIcons()



class Unix (object):
    def __init__ (self):
        pass


    def init (self):
        """
        Активировать дополнительные библиотеки, в частности, pyGTK
        """
        import gobject
        gobject.threads_init()

        import pygtk
        pygtk.require('2.0')
        import gtk
        import gtk.gdk


    def startFile (self, path):
        """
        Запустить программу по умолчанию для path
        """
        runcmd = "xdg-open '%s'" % path
        wx.Execute (runcmd)


    @property
    def filesEncoding (self):
        return "utf-8"


    @property
    def inputEncoding (self):
        encoding = locale.getpreferredencoding()

        if not encoding:
            encoding = "utf8"

        return encoding


    @property
    def dragFileDataObject (self):
        """
        Получить класс для перетаскивания файлов из окна OutWiker'а в другие приложения.
        Под Linux'ом wx.FileDataObject не правильно работает с Unicode
        """
        class GtkFileDataObject (wx.PyDataObjectSimple):
            """
            Класс данных для перетаскивания файлов. Использовать вместо wx.FileDataObject, который по сути не работает с Unicode
            """
            def __init__ (self):
                wx.PyDataObjectSimple.__init__ (self, wx.DataFormat (wx.DF_FILENAME))
                self._fnames = []

            def AddFile (self, fname):
                self._fnames.append (fname)

            def GetDataHere (self):
                result = ""
                for fname in self._fnames:
                    result += u"file:%s\r\n" % (fname)

                # Преобразуем в строку
                return result.strip().encode("utf8")

            def GetDataSize (self):
                return len (self.GetDataHere())

        return GtkFileDataObject


    @property
    def pageTitleTester (self):
        return LinuxPageTitleTester()


    @property
    def fileIcons (self):
        return UnixFileIcons()


def getOS ():
    if os.name == "nt":
        return Windows()
    else:
        return Unix()


def getCurrentDir ():
    return unicode (os.path.dirname (sys.argv[0]), getOS().filesEncoding)


def getConfigPath (dirname=DEFAULT_CONFIG_DIR, fname=DEFAULT_CONFIG_NAME):
    """
    Вернуть полный путь до файла настроек.
    Поиск пути осуществляется следующим образом:
    1. Если в папке с программой есть файл настроек, то вернуть путь до него
    2. Иначе настройки будут храниться в домашней поддиректории. При этом создать директорию .outwiker в домашней директории.
    """
    someDir = os.path.join (getCurrentDir(), fname)
    if os.path.exists (someDir):
        path = someDir
    else:
        homeDir = os.path.join (unicode (os.path.expanduser("~"), getOS().filesEncoding), dirname)
        if not os.path.exists (homeDir):
            os.mkdir (homeDir)

        pluginsDir = os.path.join (homeDir, PLUGINS_DIR)
        if not os.path.exists (pluginsDir):
            os.mkdir (pluginsDir)

        stylesDir = os.path.join (homeDir, STYLES_DIR)
        if not os.path.exists (stylesDir):
            os.mkdir (stylesDir)

        path = os.path.join (homeDir, fname)

    return path


def getImagesDir ():
    return os.path.join (getCurrentDir(), IMAGES_DIR)


def getTemplatesDir ():
    return os.path.join (getCurrentDir(), STYLES_DIR)


def getExeFile ():
    """
    Возвращает имя запускаемого файла
    """
    return unicode (sys.argv[0], getOS().filesEncoding)


def getPluginsDirList (configDirName=DEFAULT_CONFIG_DIR, configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return getSpecialDirList (PLUGINS_DIR, configDirName, configFileName)


def getStylesDirList (configDirName=DEFAULT_CONFIG_DIR,
                      configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return getSpecialDirList (STYLES_DIR, configDirName, configFileName)


def getSpecialDirList (dirname,
                       configDirName=DEFAULT_CONFIG_DIR,
                       configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список "специальных" директорий (директорий для плагинов, стилей и т.п., расположение которых зависит от расположения файла настроек)
    """
    # Директория рядом с запускаемым файлом
    programSpecialDir = os.path.join (getCurrentDir(), dirname)

    # Директория рядом с файлом настроек
    configdir = os.path.dirname (getConfigPath (configDirName, configFileName))
    specialDir = os.path.join (configdir, dirname)

    dirlist = [programSpecialDir]
    if os.path.abspath (programSpecialDir) != os.path.abspath (specialDir):
        dirlist.append (specialDir)

    return dirlist


def readTextFile (fname):
    """
    Читать файл в кодировке UTF-8.
    Возвращает unicode-строку
    """
    with codecs.open (fname, "r", "utf-8") as fp:
        return fp.read()
