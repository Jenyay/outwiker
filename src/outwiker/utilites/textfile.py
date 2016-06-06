# -*- coding: UTF-8 -*-

import codecs


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
