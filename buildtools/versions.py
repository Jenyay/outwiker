# -*- coding: utf-8 -*-

import os
from typing import List, Tuple

import outwiker
from outwiker.core.appinfo import AppInfo
from outwiker.core.appinfofactory import AppInfoFactory
from outwiker.utilites.textfile import readTextFile
from outwiker.utilites.downloader import Downloader
from buildtools.defines import (
    DOWNLOAD_TIMEOUT,
    OUTWIKER_INFO_FILENAME,
    PLUGIN_INFO_FILENAME,
    PLUGIN_VERSIONS_FILENAME,
    PLUGINS_LIST,
    PLUGINS_DIR,
)


def readAppInfo(fname: str) -> AppInfo:
    text = readTextFile(fname)
    return AppInfoFactory.fromString(text, '')


def downloadAppInfo(url):
    downloader = Downloader(DOWNLOAD_TIMEOUT)
    xml_content = downloader.download(url)
    appinfo = AppInfoFactory.fromString(xml_content, '')
    return appinfo


def getOutwikerAppInfo():
    return readAppInfo(u'src/versions.xml')


def getOutwikerVersion() -> Tuple[str, str]:
    """
    Return a tuple: (version number, build number)
    """
    version_major = u'.'.join([str(item) for item in outwiker.__version__[:-1]])
    version_build = str(outwiker.__version__[-1])

    return (version_major, version_build)


def getOutwikerVersionStr() -> str:
    '''
    Return version as "x.x.x.xxx" string
    '''
    version = getOutwikerVersion()
    return u'{}.{}'.format(version[0], version[1])


def getLocalAppInfoList() -> List['outwiker.core.appinfo.AppInfo']:
    """
    Return AppInfo list for OutWiker and plug-ins.
    """
    app_list = [
         readAppInfo(os.path.join(u'src', OUTWIKER_INFO_FILENAME)),
    ]

    # Fill url_list with plugins.xml paths
    for plugin in PLUGINS_LIST:
        path = getPluginInfoPath(plugin)
        app_list.append(readAppInfo(path))
    return app_list


def getPluginVersionsPath(plugin):
    return os.path.join(PLUGINS_DIR,
                        plugin,
                        plugin,
                        PLUGIN_VERSIONS_FILENAME)


def getPluginInfoPath(plugin):
    return os.path.join(PLUGINS_DIR,
                        plugin,
                        plugin,
                        PLUGIN_INFO_FILENAME)
