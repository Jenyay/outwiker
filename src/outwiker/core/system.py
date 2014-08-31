#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Действия, которые зависят от ОС, на которой запущена программа
"""

import codecs
import locale
import os
import os.path as op
import shutil
import sys

import wx

from .pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester
from outwiker.gui.fileicons import WindowsFileIcons, UnixFileIcons


# Папки, используемые в программе
IMAGES_DIR = u"images"
STYLES_DIR = u"styles"
PLUGINS_DIR = u"plugins"

# Имя файла настроек по умолчанию
DEFAULT_CONFIG_NAME = u"outwiker.ini"

# Имя по умолчанию для папки с настройками в профиле пользователя(устарело)
DEFAULT_OLD_CONFIG_DIR = u".outwiker"

# Новая местоположение конфигурационной директории
# По стандарту, если переменная XDG_CONFIG_HOME не задана в окружении,
# то берется значение по умолчанию т.е. ~/.config
# http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
DEFAULT_CONFIG_DIR = u"outwiker"


class System (object):
    def moveConfig(self, oldConfDir, newConfDir):
        shutil.move(oldConfDir, newConfDir)



class Windows (System):
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


    def migrateConfig(self):
        pass



class Unix (System):
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


    def migrateConfig(self):
        """
        Метод migrateConfig переносит конфигурационную директорию из старого местоположения (HOME$/.outwiker)
        в новое ($XDG_CONFIG_HOME/outwiker или .config/outwiker если переменная окружения не задана)
        """
        confDir = op.join(os.environ.get(u"XDG_CONFIG_HOME", u".config"),
                          DEFAULT_CONFIG_DIR)

        homeDir = unicode (op.expanduser("~"), getOS().filesEncoding)

        oldConfDir = op.join(homeDir, DEFAULT_OLD_CONFIG_DIR)

        if not op.isabs(confDir):
            confDir = op.join(homeDir, confDir)

        if op.exists(oldConfDir) and not op.exists(confDir):
            shutil.move(oldConfDir, confDir)


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
    return unicode (op.dirname (sys.argv[0]), getOS().filesEncoding)


def getConfigPath (dirname=DEFAULT_CONFIG_DIR, fname=DEFAULT_CONFIG_NAME):
    """
    Вернуть полный путь до файла настроек.
    Поиск пути осуществляется следующим образом:
    1. Если в папке с программой есть файл настроек, то вернуть путь до него
    2. Иначе настройки будут храниться в домашней конфигурационной директории outwiker (Пример: .conf/outwiker)
    """
    confSrc = op.join (getCurrentDir(), fname)

    if op.exists (confSrc):
        confPath = confSrc
    else:
        homeDir = unicode (op.expanduser("~"), getOS().filesEncoding)

        confDir = op.join (os.environ.get (u"XDG_CONFIG_HOME", u".config"),
                           dirname)

        if not op.isabs (confDir):
            confDir = op.join (homeDir, confDir)

        oldConfDir = op.join (homeDir, DEFAULT_OLD_CONFIG_DIR)
        oldConfPath = op.join (oldConfDir, fname)

        if op.exists (oldConfPath):
            mainConfDir = oldConfDir
            confPath = oldConfPath
        else:
            mainConfDir = confDir
            confPath = op.join (confDir, fname)

        pluginsDir = op.join (mainConfDir, PLUGINS_DIR)
        if not op.exists (pluginsDir):
            os.mkdir (pluginsDir)

        stylesDir = op.join (mainConfDir, STYLES_DIR)
        if not op.exists (stylesDir):
            os.mkdir (stylesDir)

    return confPath


def getImagesDir ():
    return op.join (getCurrentDir(), IMAGES_DIR)


def getTemplatesDir ():
    return op.join (getCurrentDir(), STYLES_DIR)


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
    programSpecialDir = op.join (getCurrentDir(), dirname)

    # Директория рядом с файлом настроек
    configdir = op.dirname (getConfigPath (configDirName, configFileName))
    specialDir = op.join (configdir, dirname)

    dirlist = [programSpecialDir]
    if op.abspath (programSpecialDir) != op.abspath (specialDir):
        dirlist.append (specialDir)

    return dirlist


def readTextFile (fname):
    """
    Читать файл в кодировке UTF-8.
    Возвращает unicode-строку
    """
    with codecs.open (fname, "r", "utf-8") as fp:
        return fp.read()


def writeTextFile (fname, text):
    """
    Записать текст в кодировке utf-8
    """
    with codecs.open (fname, "w", "utf-8") as fp:
        return fp.write (text)
