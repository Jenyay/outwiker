# -*- coding: utf-8 -*-
"""
Действия, которые зависят от ОС, на которой запущена программа
"""

import ctypes
import locale
import os
import os.path as op
import shutil
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Union
from uuid import UUID

import wx

from outwiker.core.images import find_svg

from .pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester
from .spellchecker.cyhunspellwrapper import CyHunspellWrapper

from outwiker.gui.fileicons import WindowsFileIcons, UnixFileIcons
from outwiker.core.defines import (ICONS_FOLDER_NAME,
                                   IMAGES_FOLDER_NAME,
                                   STYLES_FOLDER_NAME,
                                   PLUGINS_FOLDER_NAME,
                                   SPELL_FOLDER_NAME,
                                   STYLES_BLOCK_FOLDER_NAME,
                                   STYLES_INLINE_FOLDER_NAME,
                                   DEFAULT_CONFIG_DIR,
                                   DEFAULT_CONFIG_NAME,
                                   )


# Имя по умолчанию для папки с настройками в профиле пользователя (устарело)
DEFAULT_OLD_CONFIG_DIR = ".outwiker"

logger = logging.getLogger('outwiker.core.system')


class System:
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
        return 'windows'

    @property
    def python(self):
        return 'python'

    def startFile(self, path: Union[str, Path]):
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

    @property
    def documentsDir(self):
        # Get from https://gist.github.com/mkropat/7550097#file-knownpaths-py
        from ctypes import windll, wintypes

        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8)
            ] 

            def __init__(self, uuid):
                ctypes.Structure.__init__(self)
                self.Data1, self.Data2, self.Data3, self.Data4[0], self.Data4[1], rest = UUID(uuid).fields
                for i in range(2, 8):
                    self.Data4[i] = rest>>(8 - i - 1)*8 & 0xff

        documents_uuid = GUID('{FDD39AD0-238F-46AF-ADB4-6C85480369C7}')
        S_OK = 0
        p_path = ctypes.c_wchar_p()
        result = windll.shell32.SHGetKnownFolderPath(
                ctypes.byref(documents_uuid), 
                0, 
                wintypes.HANDLE(0),
                ctypes.byref(p_path))

        if result != S_OK:
            logger.error("Can't get documents directory")
            windll.ole32.CoTaskMemFree(p_path)
            return

        path = p_path.value
        windll.ole32.CoTaskMemFree(p_path)
        return path

    def getHtmlRender(self, parent):
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake
            return HtmlRenderFake(parent)
        else:
            from outwiker.gui.htmlrenderie import HtmlRenderIEGeneral
            return HtmlRenderIEGeneral(parent)

    def getHtmlRenderForPage(self, parent):
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake
            return HtmlRenderFake(parent)
        else:
            from outwiker.gui.htmlrenderie import HtmlRenderIEForPage
            return HtmlRenderIEForPage(parent)

    def getHtmlRenderSearchController(self, searchPanel, htmlRender):
        from outwiker.gui.controls.htmlsearchpanelcontrollerwindows import HtmlSearchPanelControllerWindows
        return HtmlSearchPanelControllerWindows(searchPanel, htmlRender)

    def getSpellChecker(self, langlist, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return CyHunspellWrapper(langlist, folders)

    @property
    def windowIconFile(self) -> str:
        return getBuiltinImagePath("outwiker_small.ico")


class Unix(System):
    @property
    def name(self):
        return 'unix'

    @property
    def python(self):
        return 'python3'

    def startFile(self, path: Union[str, Path]):
        """
        Запустить программу по умолчанию для path
        """
        subprocess.Popen(['xdg-open', str(path)])

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
    def documentsDir(self):
        return op.expanduser("~")

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
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake
            return HtmlRenderFake(parent)
        else:
            from outwiker.gui.htmlrenderwebkit import HtmlRenderWebKitGeneral
            return HtmlRenderWebKitGeneral(parent)

    def getHtmlRenderForPage(self, parent):
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake
            return HtmlRenderFake(parent)
        else:
            from outwiker.gui.htmlrenderwebkit import HtmlRenderWebKitForPage
            return HtmlRenderWebKitForPage(parent)

    def getSpellChecker(self, langlist, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return CyHunspellWrapper(langlist, folders)

    @property
    def windowIconFile(self) -> str:
        return getBuiltinImagePath("outwiker.ico")

    def getHtmlRenderSearchController(self, searchPanel, htmlRender):
        from outwiker.gui.controls.htmlsearchpanelcontrollerunix import HtmlSearchPanelControllerUnix
        return HtmlSearchPanelControllerUnix(searchPanel, htmlRender)


def getOS():
    if os.name == "nt":
        return Windows()
    else:
        return Unix()


def getCurrentDir() -> str:
    if __file__.endswith('.pyc'):
        # For compiled with cx_freeze package
        current_dir = str(Path(__file__).parents[3].resolve())
    else:
        # For sources executing
        current_dir = str(Path(__file__).parents[2].resolve())
    return current_dir


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


def getImagesDir() -> str:
    return op.join(getCurrentDir(), IMAGES_FOLDER_NAME)


def getBuiltinImagePath(*relative_image_name: str) -> str:
    '''
    Return absolute path to image file from "images" directory
    '''
    path = os.path.abspath(os.path.join(getImagesDir(), *relative_image_name))
    return find_svg(path)


def getTemplatesDir() -> str:
    return op.join(getCurrentDir(), STYLES_FOLDER_NAME)


def getExeFile() -> str:
    """
    Возвращает имя запускаемого файла
    """
    return sys.argv[0]


def getPluginsDirList(configDirName=DEFAULT_CONFIG_DIR,
                      configFileName=DEFAULT_CONFIG_NAME) -> List[str]:
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return getSpecialDirList(PLUGINS_FOLDER_NAME,
                             configDirName,
                             configFileName)


def getIconsDirList(configDirName=DEFAULT_CONFIG_DIR,
                    configFileName=DEFAULT_CONFIG_NAME) -> List[str]:
    """
    Возвращает список директорий, где могут располагаться иконки для страниц
    """
    return getSpecialDirList(ICONS_FOLDER_NAME, configDirName, configFileName)


def getStylesDirList(configDirName=DEFAULT_CONFIG_DIR,
                     configFileName=DEFAULT_CONFIG_NAME) -> List[str]:
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return getSpecialDirList(STYLES_FOLDER_NAME, configDirName, configFileName)


def getSpellDirList(configDirName=DEFAULT_CONFIG_DIR,
                    configFileName=DEFAULT_CONFIG_NAME) -> List[str]:
    """
    Возвращает список директорий со словарями для проверки орфографии
    """
    return getSpecialDirList(SPELL_FOLDER_NAME, configDirName, configFileName)


def getSpecialDirList(dirname,
                      configDirName=DEFAULT_CONFIG_DIR,
                      configFileName=DEFAULT_CONFIG_NAME) -> List[str]:
    """
    Возвращает список "специальных" директорий (директорий для плагинов,
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
    python = getOS().python

    logger.debug('openInNewWindow. Params: %s', params)

    env = os.environ.copy()

    if exeFile.endswith(".exe"):
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(params, creationflags=DETACHED_PROCESS, env=env)
    elif exeFile.endswith(".py"):
        subprocess.Popen([python] + params, env=env)
    else:
        subprocess.Popen(params, env=env)
