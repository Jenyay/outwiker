# -*- coding: UTF-8 -*-

import sys
import os

from fabric.api import local

from buildtools.defines import BUILD_DIR, DEB_SOURCE_BUILD_DIR


def addToSysPath(path):
    """
    Add path to sys.path to use outwiker modules
    """
    encoding = sys.getfilesystemencoding()
    cmd_folder = os.path.abspath(path)

    syspath = [unicode(item, encoding)
               if not isinstance(item, unicode)
               else item for item in sys.path]

    if cmd_folder not in syspath:
        sys.path.insert(0, cmd_folder)


def getPython():
    if os.name == 'posix':
        return u'python2.7'
    else:
        return u'py -2'


def execute(command):
    if os.name == 'posix':
        local(u'LD_PRELOAD=libwx_gtk2u_webview-3.0.so.0 ' + command)
    else:
        local(command)


def getCurrentUbuntuDistribName():
    with open('/etc/lsb-release') as fp:
        for line in fp:
            line = line.strip()
            if line.startswith(u'DISTRIB_CODENAME'):
                codename = line.split(u'=')[1].strip()
                return codename


def getPathToPlugin(plugin_name):
    return os.path.join(u'plugins', plugin_name, plugin_name)


def getResultDistribPath():
    """
    Return directory name like build/x.x.x.xxx
    """
    from buildtools.versions import getOutwikerVersion

    version = getOutwikerVersion()
    distrib_dir_name = version[0] + u'.' + version[1]
    return os.path.join(BUILD_DIR, distrib_dir_name)


def getDebSourceResultPath():
    """
    Return directory name like build/x.x.x.xxx/deb_source
    """
    return os.path.join(getResultDistribPath(), DEB_SOURCE_BUILD_DIR)
