# -*- coding: utf-8 -*-

import os
from typing import Tuple

import outwiker
from outwiker.core.appinfo import AppInfo
from outwiker.core.appinfofactory import AppInfoFactory
from outwiker.utilites.textfile import readTextFile
from outwiker.utilites.downloader import Downloader
from buildtools.defines import (
    DOWNLOAD_TIMEOUT,
    PLUGIN_INFO_FILENAME,
    PLUGINS_DIR,
    OUTWIKER_VERSIONS_FILENAME,
    NEED_FOR_BUILD_DIR
)


def readAppInfo(fname: str) -> AppInfo:
    text = readTextFile(fname)
    return AppInfoFactory.fromString(text, '')


def downloadAppInfo(url):
    downloader = Downloader(DOWNLOAD_TIMEOUT)

    try:
        xml_content = downloader.download(url)
        appinfo = AppInfoFactory.fromString(xml_content, '')
    except ValueError:
        appinfo = AppInfoFactory.fromString('', '')

    return appinfo


def getOutwikerAppInfo():
    return readAppInfo(os.path.join('src',
                                    NEED_FOR_BUILD_DIR,
                                    OUTWIKER_VERSIONS_FILENAME))


def getOutwikerVersion() -> Tuple[str, str]:
    """
    Return a tuple: (version number, build number)
    """
    version_major = '.'.join([str(item) for item in outwiker.__version__[:-1]])
    version_build = str(outwiker.__version__[-1])

    return (version_major, version_build)


def getOutwikerVersionStr() -> str:
    '''
    Return version as "x.x.x.xxx" string
    '''
    version = getOutwikerVersion()
    return u'{}.{}'.format(version[0], version[1])


def getPluginInfoPath(plugin):
    return os.path.join(PLUGINS_DIR,
                        plugin,
                        plugin,
                        PLUGIN_INFO_FILENAME)


def getPluginChangelogPath(plugin):
    return os.path.join(PLUGINS_DIR,
                        plugin,
                        OUTWIKER_VERSIONS_FILENAME)
