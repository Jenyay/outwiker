# -*- coding: utf-8 -*-

import os
from typing import List

from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.utilites.textfile import readTextFile
from outwiker.utilites.downloader import Downloader
from buildtools.defines import (
    DOWNLOAD_TIMEOUT,
    OUTWIKER_VERSIONS_FILENAME,
    PLUGIN_VERSIONS_FILENAME,
    PLUGINS_LIST,
    PLUGINS_DIR,
)


def readAppInfo(fname: str) -> 'outwiker.core.appinfo.AppInfo':
    text = readTextFile(fname)
    return XmlVersionParser([u'en']).parse(text)


def downloadAppInfo(url):
    downloader = Downloader(DOWNLOAD_TIMEOUT)
    version_parser = XmlVersionParser(['en'])
    xml_content = downloader.download(url)
    appinfo = version_parser.parse(xml_content)
    return appinfo


def getOutwikerAppInfo():
    return readAppInfo(u'src/versions.xml')


def getOutwikerVersion():
    """
    Return a tuple: (version number, build number)
    """
    # The file with the version number
    version = getOutwikerAppInfo().currentVersion
    version_major = u'.'.join([str(item) for item in version[:-1]])
    version_build = str(version[-1])

    return (version_major, version_build)


def getOutwikerVersionStr():
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
         readAppInfo(os.path.join(u'src', OUTWIKER_VERSIONS_FILENAME)),
    ]

    # Fill url_list with plugins.xml paths
    for plugin in PLUGINS_LIST:
        path = getPluginVersionsPath(plugin)
        app_list.append(readAppInfo(path))
    return app_list


def getPluginVersionsPath(plugin):
    return os.path.join(PLUGINS_DIR,
                        plugin,
                        plugin,
                        PLUGIN_VERSIONS_FILENAME)
