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

from .pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester
from .spellchecker.enchantwrapper import EnchantWrapper
from outwiker.gui.fileicons import WindowsFileIcons, UnixFileIcons
from outwiker.core.defines import (ICONS_FOLDER_NAME,
                                   IMAGES_FOLDER_NAME,
                                   STYLES_FOLDER_NAME,
                                   PLUGINS_FOLDER_NAME,
                                   SPELL_FOLDER_NAME,
                                   STYLES_BLOCK_FOLDER_NAME,
                                   STYLES_INLINE_FOLDER_NAME
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
    @property
    def name(self):
        return u'windows'

    def startFile(self, path):
        """
        Запустить программу по умолчанию для path
        """
        os.startfile(path)

    @property
    def inputEncoding(self):
        """
        Кодировка, используемая для преобразования нажатой клавиши в строку
        """
        return "mbcs"

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

    def getSpellChecker(self, langlist, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return EnchantWrapper(langlist, folders)


class Unix(System):
    @property
    def name(self):
        return u'unix'

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
        homeDir = op.expanduser("~")
        settingsDir = os.environ.get("XDG_CONFIG_HOME", ".config")

        if not op.isabs(settingsDir):
            settingsDir = op.join(homeDir, settingsDir)

        return settingsDir

    @property
    def inputEncoding(self):
        encoding = locale.getpreferredencoding()

        if not encoding:
            encoding = "utf8"

        return encoding

    @property
    def pageTitleTester(self):
        return LinuxPageTitleTester()

    @property
    def fileIcons(self):
        return UnixFileIcons()

    def getHtmlRender(self, parent):
        from outwiker.gui.htmlrenderwebkit import HtmlRenderWebKit
        return HtmlRenderWebKit(parent)

    def getSpellChecker(self, langlist, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return EnchantWrapper(langlist, folders)


def getOS():
    if os.name == "nt":
        return Windows()
    else:
        return Unix()


def getCurrentDir():
    return op.dirname(sys.argv[0])


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

        os.makedirs(op.join(mainConfDir, STYLES_BLOCK_FOLDER_NAME),
                    exist_ok=True)
        os.makedirs(op.join(mainConfDir, STYLES_INLINE_FOLDER_NAME),
                    exist_ok=True)

    return confPath


def getImagesDir():
    return op.join(getCurrentDir(), IMAGES_FOLDER_NAME)


def getTemplatesDir():
    return op.join(getCurrentDir(), STYLES_FOLDER_NAME)


def getExeFile():
    """
    Возвращает имя запускаемого файла
    """
    return sys.argv[0]


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

    params = [exeFile, path] + args

    env = os.environ.copy()

    if exeFile.endswith(".exe"):
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(params, creationflags=DETACHED_PROCESS, env=env)
    elif exeFile.endswith(".py"):
        subprocess.Popen(["python"] + params, env=env)
    else:
        subprocess.Popen(params, env=env)
