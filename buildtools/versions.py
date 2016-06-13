# -*- coding: UTF-8 -*-

from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.utilites.textfile import readTextFile


def readAppInfo(fname):
    text = readTextFile(fname)
    return XmlVersionParser([u'en']).parse(text)


def getOutwikerAppInfo():
    return readAppInfo(u'src/versions.xml')


def getOutwikerVersion():
    """
    Return a tuple: (version number, build number)
    """
    # The file with the version number
    version = getOutwikerAppInfo().currentVersion
    version_major = u'.'.join([unicode(item) for item in version[:-1]])
    version_build = unicode(version[-1])

    return (version_major, version_build)
