# -*- coding: utf-8 -*-
"""
Действия, которые зависят от ОС, на которой запущена программа
"""

import locale
import os
import os.path as op
import shutil
import sys
import subprocess

import wx

from .pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester
from outwiker.gui.fileicons import WindowsFileIcons, UnixFileIcons
from outwiker.core.defines import (ICONS_FOLDER_NAME,
                                   IMAGES_FOLDER_NAME,
                                   STYLES_FOLDER_NAME,
                                   PLUGINS_FOLDER_NAME,
                                   SPELL_FOLDER_NAME,
                                   )


# Имя файла настроек по умолчанию
DEFAULT_CONFIG_NAME = u"outwiker.ini"

# Имя по умолчанию для папки с настройками в профиле пользователя (устарело)
DEFAULT_OLD_CONFIG_DIR = u".outwiker"

# Новая местоположение конфигурационной директории
# По стандарту, если переменная XDG_CONFIG_HOME не задана в окружении,
# то берется значение по умолчанию т.е. ~/.config
# http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
DEFAULT_CONFIG_DIR = u"outwiker"


class System(object):
    def migrateConfig(self,
                      oldConfDirName=DEFAULT_OLD_CONFIG_DIR,
                      newConfDirName=DEFAULT_CONFIG_DIR):
        """
        Remove config directory from HOME$/.outwiker to idealogic right place
        (depends of the OS)
        """
        confDir = op.join(self.settingsDir, newConfDirName)

        homeDir = str(op.expanduser("~"))
        oldConfDir = op.join(homeDir, oldConfDirName)

        if op.exists(oldConfDir) and not op.exists(confDir):
            shutil.move(oldConfDir, confDir)


class Windows(System):
    def init(self):
        pass

    @property
    def name(self):
        return u'windows'

    def startFile(self, path):
        """
        Запустить программу по умолчанию для path
        """
        os.startfile(path.replace("/", "\\"))

    @property
    def filesEncoding(self):
        return sys.getfilesystemencoding()

    @property
    def inputEncoding(self):
        """
        Кодировка, используемая для преобразования нажатой клавиши в строку
        """
        return "mbcs"

    @property
    def dragFileDataObject(self):
        """
        Получить класс для перетаскивания файлов
        из окна OutWiker'а в другие приложения.
        Под Linux'ом wx.FileDataObject не правильно работает с Unicode
        """
        return wx.FileDataObject

    @property
    def pageTitleTester(self):
        return WindowsPageTitleTester()

    @property
    def fileIcons(self):
        return WindowsFileIcons()

    @property
    def settingsDir(self):
        """
        Возвращает папку, внутри которой хранятся настройки всех программ,
        и где будет создаваться папка для хранения настроек OutWiker
        """
        homeDir = op.expanduser("~")
        appdata = (os.environ["APPDATA"]
                   if "APPDATA" in os.environ
                   else homeDir)
        return appdata

    def getHtmlRender(self, parent):
        from outwiker.gui.htmlrenderie import HtmlRenderIE
        return HtmlRenderIE(parent)


class Unix(System):
    @property
    def name(self):
        return u'unix'

    def init(self):
        import gi
        gi.require_version('Gdk', '3.0')

        from gi.repository import Gdk
        Gdk.threads_init()

    def startFile(self, path):
        """
        Запустить программу по умолчанию для path
        """
        subprocess.Popen([u'xdg-open', path])

    @property
    def settingsDir(self):
        """
        Возвращает папку, внутри которой хранятся настройки всех программ,
        и где будет создаваться папка для хранения настроек OutWiker.
        ($XDG_CONFIG_HOME/outwiker или .config/outwiker)
        """
        homeDir = str(op.expanduser("~"))
        settingsDir = os.environ.get("XDG_CONFIG_HOME", ".config")

        if not op.isabs(settingsDir):
            settingsDir = op.join(homeDir, settingsDir)

        return settingsDir

    @property
    def filesEncoding(self):
        return sys.getfilesystemencoding()

    @property
    def inputEncoding(self):
        encoding = locale.getpreferredencoding()

        if not encoding:
            encoding = "utf8"

        return encoding

    @property
    def dragFileDataObject(self):
        """
        Получить класс для перетаскивания файлов из окна OutWiker'а
        в другие приложения.
        Под Linux'ом wx.FileDataObject не правильно работает с Unicode
        """
        class GtkFileDataObject(wx.PyDataObjectSimple):
            """
            Класс данных для перетаскивания файлов. Использовать вместо
            wx.FileDataObject, который по сути не работает с Unicode
            """
            def __init__(self):
                wx.PyDataObjectSimple.__init__(self,
                                               wx.DataFormat(wx.DF_FILENAME))
                self._fnames = []

            def AddFile(self, fname):
                self._fnames.append(fname)

            def GetDataHere(self):
                result = ""
                for fname in self._fnames:
                    result += u"file:%s\r\n" % (fname)

                # Преобразуем в строку
                return result.strip().encode("utf8")

            def GetDataSize(self):
                return len(self.GetDataHere())

        return GtkFileDataObject

    @property
    def pageTitleTester(self):
        return LinuxPageTitleTester()

    @property
    def fileIcons(self):
        return UnixFileIcons()

    def getHtmlRender(self, parent):
        from outwiker.gui.htmlrenderwebkit import HtmlRenderWebKit
        return HtmlRenderWebKit(parent)


def getOS():
    if os.name == "nt":
        return Windows()
    else:
        return Unix()


def getCurrentDir():
    return str(op.dirname(sys.argv[0]))


def getConfigPath(dirname=DEFAULT_CONFIG_DIR, fname=DEFAULT_CONFIG_NAME):
    """
    Вернуть полный путь до файла настроек.
    Поиск пути осуществляется следующим образом:
    1. Если в папке с программой есть файл настроек, то вернуть путь до него
    2. Иначе настройки будут храниться в домашней конфигурационной директории
    outwiker (Пример: .conf/outwiker)
    """
    confSrc = op.join(getCurrentDir(), fname)

    if op.exists(confSrc):
        confPath = confSrc
    else:
        mainConfDir = op.join(getOS().settingsDir, dirname)
        confPath = op.join(mainConfDir, fname)

        if not op.exists(mainConfDir):
            os.mkdir(mainConfDir)

        pluginsDir = op.join(mainConfDir, PLUGINS_FOLDER_NAME)
        if not op.exists(pluginsDir):
            os.mkdir(pluginsDir)

        stylesDir = op.join(mainConfDir, STYLES_FOLDER_NAME)
        if not op.exists(stylesDir):
            os.mkdir(stylesDir)

        iconsDir = op.join(mainConfDir, ICONS_FOLDER_NAME)
        if not op.exists(iconsDir):
            os.mkdir(iconsDir)

        spellDir = op.join(mainConfDir, SPELL_FOLDER_NAME)
        if not op.exists(spellDir):
            os.mkdir(spellDir)

    return confPath


def getImagesDir():
    return op.join(getCurrentDir(), IMAGES_FOLDER_NAME)


def getTemplatesDir():
    return op.join(getCurrentDir(), STYLES_FOLDER_NAME)


def getExeFile():
    """
    Возвращает имя запускаемого файла
    """
    return unicode(sys.argv[0], getOS().filesEncoding)


def getPluginsDirList(configDirName=DEFAULT_CONFIG_DIR,
                      configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return getSpecialDirList(PLUGINS_FOLDER_NAME,
                             configDirName,
                             configFileName)


def getIconsDirList(configDirName=DEFAULT_CONFIG_DIR,
                    configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий, где могут располагаться иконки для страниц
    """
    return getSpecialDirList(ICONS_FOLDER_NAME, configDirName, configFileName)


def getStylesDirList(configDirName=DEFAULT_CONFIG_DIR,
                     configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return getSpecialDirList(STYLES_FOLDER_NAME, configDirName, configFileName)


def getSpellDirList(configDirName=DEFAULT_CONFIG_DIR,
                    configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список директорий со словарями для проверки орфографии
    """
    return getSpecialDirList(SPELL_FOLDER_NAME, configDirName, configFileName)


def getSpecialDirList(dirname,
                      configDirName=DEFAULT_CONFIG_DIR,
                      configFileName=DEFAULT_CONFIG_NAME):
    """
    Возвращает список "специальных" директорий(директорий для плагинов,
    стилей и т.п., расположение которых зависит от расположения файла настроек)
    """
    # Директория рядом с запускаемым файлом
    programSpecialDir = op.abspath(op.join(getCurrentDir(), dirname))

    # Директория рядом с файлом настроек
    configdir = op.dirname(getConfigPath(configDirName, configFileName))
    specialDir = op.abspath(op.join(configdir, dirname))

    dirlist = [programSpecialDir]
    if programSpecialDir != specialDir:
        dirlist.append(specialDir)

    return dirlist


def openInNewWindow(path, args=[]):
    """ Open wiki tree in the new OutWiker window
    """
    exeFile = getExeFile()
    encoding = getOS().filesEncoding

    params = [exeFile.encode(encoding), path.encode(encoding)] + args

    env = os.environ.copy()

    if exeFile.endswith(".exe"):
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(params, creationflags=DETACHED_PROCESS, env=env)
    else:
        subprocess.Popen(["python"] + params, env=env)
