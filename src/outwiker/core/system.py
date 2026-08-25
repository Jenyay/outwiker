# -*- coding: utf-8 -*-
"""
OS-dependent actions for the program
"""

from abc import ABC, abstractmethod
import ctypes
import locale
import os
import os.path as op
import shutil
import sys
import subprocess
import logging
from pathlib import Path
from typing import List, Optional, Union
from uuid import UUID
from functools import lru_cache

import wx

import outwiker
from outwiker.core.images import find_svg

from .pagetitletester import (
    PageTitleTester,
    WindowsPageTitleTester,
    LinuxPageTitleTester,
)
from .spellchecker.cyhunspellwrapper import CyHunspellWrapper

from outwiker.gui.fileicons import BaseFileIcons, WindowsFileIcons, UnixFileIcons
from outwiker.core.defines import (
    ICONS_FOLDER_NAME,
    IMAGES_FOLDER_NAME,
    STYLES_FOLDER_NAME,
    PLUGINS_FOLDER_NAME,
    SPELL_FOLDER_NAME,
    STYLES_BLOCK_FOLDER_NAME,
    STYLES_INLINE_FOLDER_NAME,
    DEFAULT_CONFIG_DIR,
    DEFAULT_CONFIG_NAME,
    DATA_FOLDER_NAME,
    OUTWIKER_PATH_ENV_VAR,
)


# Default name for the settings folder in user profile (deprecated)
DEFAULT_OLD_CONFIG_DIR = ".outwiker"

logger = logging.getLogger("outwiker.core.system")


class System(ABC):
    def migrateConfig(
        self, oldConfDirName=DEFAULT_OLD_CONFIG_DIR, newConfDirName=DEFAULT_CONFIG_DIR
    ):
        """
        Remove config directory from HOME$/.outwiker to idealogic right place
        (depends of the OS)
        """
        confDir = op.join(self.settingsDir, newConfDirName)

        homeDir = str(op.expanduser("~"))
        oldConfDir = op.join(homeDir, oldConfDirName)

        if op.exists(oldConfDir) and not op.exists(confDir):
            shutil.move(oldConfDir, confDir)

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def python(self) -> str: ...

    @abstractmethod
    def startFile(self, path: Union[str, Path]) -> None: ...

    @property
    @abstractmethod
    def inputEncoding(self) -> str: ...

    @property
    @abstractmethod
    def pageTitleTester(self) -> PageTitleTester: ...

    @property
    @abstractmethod
    def fileIcons(self) -> BaseFileIcons: ...

    @property
    @abstractmethod
    def settingsDir(self) -> str: ...

    @property
    @abstractmethod
    def documentsDir(self) -> Optional[str]: ...

    @abstractmethod
    def getHtmlRender(self, parent, application): ...

    @abstractmethod
    def getHtmlRenderForPage(self, parent, application): ...

    @abstractmethod
    def getHtmlRenderSearchController(self, searchPanel, htmlRender): ...

    @property
    @abstractmethod
    def windowIconFile(self) -> str: ...

    @property
    @abstractmethod
    def defaultLanguage(self) -> str: ...


class Windows(System):
    @property
    def name(self) -> str:
        return "windows"

    @property
    def python(self) -> str:
        return "python"

    def startFile(self, path: Union[str, Path]) -> None:
        """
        Start the default program for path
        """
        os.startfile(path)

    @property
    def inputEncoding(self) -> str:
        """
        Encoding used to convert a pressed key to a string
        """
        return "mbcs"

    @property
    def pageTitleTester(self) -> PageTitleTester:
        return WindowsPageTitleTester()

    @property
    def fileIcons(self) -> BaseFileIcons:
        return WindowsFileIcons()

    @property
    def settingsDir(self) -> str:
        """
        Returns the folder where all programs' settings are stored,
        and where the folder for OutWiker settings will be created
        """
        homeDir = op.expanduser("~")
        appdata = os.environ["APPDATA"] if "APPDATA" in os.environ else homeDir
        return appdata

    @property
    def documentsDir(self) -> Optional[str]:
        # Get from https://gist.github.com/mkropat/7550097#file-knownpaths-py
        from ctypes import windll, wintypes

        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", wintypes.DWORD),
                ("Data2", wintypes.WORD),
                ("Data3", wintypes.WORD),
                ("Data4", wintypes.BYTE * 8),
            ]

            def __init__(self, uuid):
                ctypes.Structure.__init__(self)
                (
                    self.Data1,
                    self.Data2,
                    self.Data3,
                    self.Data4[0],
                    self.Data4[1],
                    rest,
                ) = UUID(uuid).fields
                for i in range(2, 8):
                    self.Data4[i] = rest >> (8 - i - 1) * 8 & 0xFF

        documents_uuid = GUID("{FDD39AD0-238F-46AF-ADB4-6C85480369C7}")
        S_OK = 0
        p_path = ctypes.c_wchar_p()
        result = windll.shell32.SHGetKnownFolderPath(
            ctypes.byref(documents_uuid), 0, wintypes.HANDLE(0), ctypes.byref(p_path)
        )

        if result != S_OK:
            logger.error("Can't get documents directory")
            windll.ole32.CoTaskMemFree(p_path)
            return

        path = p_path.value
        windll.ole32.CoTaskMemFree(p_path)
        return path

    def _isEdgeEngineAvaible(self):
        import wx.html2 as webview
        return webview.WebView.IsBackendAvailable(webview.WebViewBackendEdge)

    def getHtmlRender(self, parent, application):
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake

            return HtmlRenderFake(parent, application)
        else:
            from outwiker.gui.htmlrenderedge import HtmlRenderEdgeGeneral
            return HtmlRenderEdgeGeneral(parent, application) if self._isEdgeEngineAvaible() else HtmlRenderIEGeneral(parent, application)

    def getHtmlRenderForPage(self, parent, application):
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake

            return HtmlRenderFake(parent, application)
        else:
            from outwiker.gui.htmlrenderedge import HtmlRenderEdgeForPage
            return HtmlRenderEdgeForPage(parent, application) if self._isEdgeEngineAvaible() else HtmlRenderIEForPage(parent, application)

    def getHtmlRenderSearchController(self, searchPanel, htmlRender):
        from outwiker.gui.controls.htmlsearchpanelcontrollerwindows import (
            HtmlSearchPanelControllerWindows,
        )

        return HtmlSearchPanelControllerWindows(searchPanel, htmlRender)

    def getSpellChecker(self, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return CyHunspellWrapper(folders)

    @property
    def windowIconFile(self) -> str:
        return getBuiltinImagePath("outwiker_small.ico")

    @property
    def defaultLanguage(self) -> str:
        lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        return locale.windows_locale.get(lang_id, "en")


class Unix(System):
    @property
    def name(self):
        return "unix"

    @property
    def python(self):
        return "python3"

    def startFile(self, path: Union[str, Path]):
        """
        Start the default program for path
        """
        subprocess.Popen(["xdg-open", str(path)])

    @property
    def settingsDir(self):
        """
        Returns the folder where all programs' settings are stored,
        and where the folder for OutWiker settings will be created.
        ($XDG_CONFIG_HOME/outwiker or .config/outwiker)
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

    def getHtmlRender(self, parent, application):
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake

            return HtmlRenderFake(parent, application)
        else:
            from outwiker.gui.htmlrenderwebkit import HtmlRenderWebKitGeneral

            return HtmlRenderWebKitGeneral(parent, application)

    def getHtmlRenderForPage(self, parent, application):
        if wx.GetApp().use_fake_html_render:
            from outwiker.gui.htmlrenderfake import HtmlRenderFake

            return HtmlRenderFake(parent, application)
        else:
            from outwiker.gui.htmlrenderwebkit import HtmlRenderWebKitForPage

            return HtmlRenderWebKitForPage(parent, application)

    def getSpellChecker(self, folders):
        """
        Return wrapper for "real" spell checker (hunspell, enchant, etc)
        """
        return CyHunspellWrapper(folders)

    @property
    def windowIconFile(self) -> str:
        return getBuiltinImagePath("outwiker.ico")

    def getHtmlRenderSearchController(self, searchPanel, htmlRender):
        from outwiker.gui.controls.htmlsearchpanelcontrollerunix import (
            HtmlSearchPanelControllerUnix,
        )

        return HtmlSearchPanelControllerUnix(searchPanel, htmlRender)

    @property
    def defaultLanguage(self) -> str:
        lang = locale.getlocale()[0]
        return lang if lang is not None else "en"


def getOS():
    if os.name == "nt":
        return Windows()
    else:
        return Unix()


def getCurrentDir() -> str:
    if __file__.endswith(".pyc"):
        # For compiled with cx_freeze package
        current_dir = str(Path(__file__).parents[3].resolve())
    else:
        # For sources executing
        current_dir = str(Path(__file__).parents[2].resolve())
    return current_dir


@lru_cache
def getMainModulePath() -> str:
    return str(Path(outwiker.__file__).parent.resolve())


def getConfigPath(dirname=DEFAULT_CONFIG_DIR, fname=DEFAULT_CONFIG_NAME):
    """
    Return the full path to the settings file.
    The path is searched as follows:
    1. If there is a settings file in the program folder, return the path to it
    2. Otherwise, settings will be stored in the home configuration directory
    outwiker (Example: .config/outwiker)
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

        os.makedirs(op.join(mainConfDir, STYLES_BLOCK_FOLDER_NAME), exist_ok=True)
        os.makedirs(op.join(mainConfDir, STYLES_INLINE_FOLDER_NAME), exist_ok=True)

    return confPath


@lru_cache
def getMainModuleDataPath() -> str:
    return os.path.join(getMainModulePath(), DATA_FOLDER_NAME)


@lru_cache
def getImagesDir() -> str:
    return op.join(getMainModuleDataPath(), IMAGES_FOLDER_NAME)


@lru_cache
def getBuiltinImagePath(*relative_image_name: str) -> str:
    """
    Return absolute path to image file from "images" directory
    """
    path = os.path.abspath(os.path.join(getImagesDir(), *relative_image_name))
    return find_svg(path)


def getExtraIconPath(relative_image_name: str) -> str:
    """
    Return absolute path to image file from "images/extraicons" directory
    """
    path = os.path.abspath(
        os.path.join(getImagesDir(), "extraicons", relative_image_name)
    )
    return find_svg(path)


def getTemplatesDir() -> str:
    return op.join(getMainModuleDataPath(), STYLES_FOLDER_NAME)


def getExeFile() -> str:
    """
    Returns the name of the executable file
    """
    return sys.argv[0]


def getPluginsDirList(
    configDirName=DEFAULT_CONFIG_DIR, configFileName=DEFAULT_CONFIG_NAME
) -> List[str]:
    """
    Returns a list of directories from which plugins should be loaded
    """
    return getSpecialDirList(PLUGINS_FOLDER_NAME, configDirName, configFileName)


def getIconsDirList(
    configDirName=DEFAULT_CONFIG_DIR, configFileName=DEFAULT_CONFIG_NAME
) -> List[str]:
    """
    Returns a list of directories where page icons may be located
    """
    return getSpecialDirList(ICONS_FOLDER_NAME, configDirName, configFileName)


def getStylesDirList(
    configDirName=DEFAULT_CONFIG_DIR, configFileName=DEFAULT_CONFIG_NAME
) -> List[str]:
    """
    Returns a list of directories from which styles should be loaded
    """
    return getSpecialDirList(STYLES_FOLDER_NAME, configDirName, configFileName)


def getSpellDirList(
    configDirName=DEFAULT_CONFIG_DIR, configFileName=DEFAULT_CONFIG_NAME
) -> List[str]:
    """
    Returns a list of directories with spelling dictionaries
    """
    return getSpecialDirList(SPELL_FOLDER_NAME, configDirName, configFileName)


def getSpecialDirList(
    dirname, configDirName=DEFAULT_CONFIG_DIR, configFileName=DEFAULT_CONFIG_NAME
) -> List[str]:
    """
    Returns a list of "special" directories (directories for plugins,
    styles, etc., whose location depends on the location of the settings file)
    """
    dirlist = []

    # Data directory in outwiker module directory
    moduleDataDir = getMainModuleDataPath()
    dirlist.append(moduleDataDir)

    # Directory next to the executable file
    programSpecialDir = op.abspath(getCurrentDir())
    dirlist.append(programSpecialDir)

    # Path from OUTWIKER_PATH environment variable
    custom_path = os.environ.get(OUTWIKER_PATH_ENV_VAR, "")
    if custom_path:
        dirlist.append(custom_path)

    # Directory next to the settings file
    configdir = op.dirname(getConfigPath(configDirName, configFileName))

    if programSpecialDir != configdir:
        dirlist.append(configdir)

    return [os.path.join(parent, dirname) for parent in dirlist]


def openInNewWindow(path, args=[]):
    """Open wiki tree in the new OutWiker window"""
    exeFile = getExeFile()
    params = [exeFile, path] + args
    python = getOS().python

    logger.debug("openInNewWindow. Params: %s", params)

    env = os.environ.copy()

    if exeFile.endswith(".exe"):
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(params, creationflags=DETACHED_PROCESS, env=env)
    elif exeFile.endswith(".py"):
        subprocess.Popen([python] + params, env=env)
    else:
        subprocess.Popen(params, env=env)
