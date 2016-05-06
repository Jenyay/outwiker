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
import subprocess

import wx

from .pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester
from outwiker.gui.fileicons import WindowsFileIcons, UnixFileIcons


# Папки, используемые в программе
IMAGES_DIR = u"images"
STYLES_DIR = u"styles"
PLUGINS_DIR = u"plugins"
ICONS_DIR = u"iconset"
SPELL_DIR = u"spell"

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
    def migrateConfig (self,
                       oldConfDirName=DEFAULT_OLD_CONFIG_DIR,
                       newConfDirName=DEFAULT_CONFIG_DIR):
        """
        Remove config directory from HOME$/.outwiker to idealogic right place (depends of the OS)
        """
        confDir = op.join(self.settingsDir, newConfDirName)

        homeDir = unicode (op.expanduser("~"), getOS().filesEncoding)
        oldConfDir = op.join(homeDir, oldConfDirName)

        if op.exists(oldConfDir) and not op.exists(confDir):
            shutil.move(oldConfDir, confDir)



class Windows (System):
    def init (self):
        pass


    @property
    def name (self):
        return u'windows'


    def startFile (self, path):
        """
        Запустить программу по умолчанию для path
        """
        os.startfile (path.replace ("/", "\\"))


    @property
    def filesEncoding (self):
        return sys.getfilesystemencoding()


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


    @property
    def settingsDir (self):
        """
        Возвращает папку, внутри которой хранятся настройки всех программ, и где будет создаваться папка для хранения настроек OutWiker
        """
        homeDir = unicode (op.expanduser("~"), self.filesEncoding)
        appdata = unicode (os.environ["APPDATA"], self.filesEncoding) if "APPDATA" in os.environ else homeDir
        return appdata


    def getHtmlRender (self, parent):
        from outwiker.gui.htmlrenderie import HtmlRenderIE
        return HtmlRenderIE (parent)


class Unix (System):
    @property
    def name (self):
        return u'unix'


    def init (self):
        if 'LD_PRELOAD' in os.environ:
            del os.environ['LD_PRELOAD']


    def startFile (self, path):
        """
        Запустить программу по умолчанию для path
        """
        subprocess.Popen ([u'xdg-open', path])


    @property
    def settingsDir (self):
        """
        Возвращает папку, внутри которой хранятся настройки всех программ, и где будет создаваться папка для хранения настроек OutWiker.
        ($XDG_CONFIG_HOME/outwiker или .config/outwiker)
        """
        homeDir = unicode (op.expanduser("~"), getOS().filesEncoding)
        settingsDir = os.environ.get (u"XDG_CONFIG_HOME", u".config")

        if not op.isabs (settingsDir):
            settingsDir = op.join (homeDir, settingsDir)

        return settingsDir


    @property
    def filesEncoding (self):
        return sys.getfilesystemencoding()


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


    def getHtmlRender (self, parent):
        from outwiker.gui.htmlrenderwebkit import HtmlRenderWebKit
        return HtmlRenderWebKit (parent)


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
        mainConfDir = op.join (getOS().settingsDir, dirname)
        confPath = op.join (mainConfDir, fname)

        if not op.exists (mainConfDir):
            os.mkdir (mainConfDir)

        pluginsDir = op.join (mainConfDir, PLUGINS_DIR)
        if not op.exists (pluginsDir):
            os.mkdir (pluginsDir)

        stylesDir = op.join (mainConfDir, STYLES_DIR)
        if not op.exists (stylesDir):
            os.mkdir (stylesDir)

        iconsDir = op.join (mainConfDir, ICONS_DIR)
        if not op.exists (iconsDir):
            os.mkdir (iconsDir)

        spellDir = op.join (mainConfDir, SPELL_DIR)
        if not op.exists (spellDir):
            os.mkdir (spellDir)

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


def getIconsDirList (configDirName=DEFAULT_CONFIG_DIR, configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий, где могут располагаться иконки для страниц
    """
    return getSpecialDirList (ICONS_DIR, configDirName, configFileName)


def getStylesDirList (configDirName=DEFAULT_CONFIG_DIR,
                      configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return getSpecialDirList (STYLES_DIR, configDirName, configFileName)


def getSpellDirList (configDirName=DEFAULT_CONFIG_DIR,
                     configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий со словарями для проверки орфографии
    """
    return getSpecialDirList (SPELL_DIR, configDirName, configFileName)


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
    Read text content. Content must be in utf-8 encoding.
    The function return unicode object
    """
    with codecs.open (fname, "r", "utf-8") as fp:
        return fp.read()


def writeTextFile (fname, text):
    """
    Write text with utf-8 encoding
    """
    with codecs.open (fname, "w", "utf-8") as fp:
        fp.write (text)


def openInNewWindow (path, readonly=False):
    """ Open wiki tree in the new OutWiker window
    """
    exeFile = getExeFile()
    encoding = getOS().filesEncoding

    params = [exeFile.encode (encoding),
              path.encode (encoding)]

    if readonly:
        params += ['--readonly']

    if exeFile.endswith (".exe"):
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen (params, creationflags=DETACHED_PROCESS)
    else:
        subprocess.Popen (["python"] + params)
