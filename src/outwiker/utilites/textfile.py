# -*- coding: utf-8 -*-


def readTextFile(fname):
    """
    Read text content. Content must be in utf-8 encoding.
    The function return unicode object
    """
    with open(fname, "r", encoding="utf-8", errors='surrogatepass') as fp:
        return fp.read()


def writeTextFile(fname, text):
    """
    Write text with utf-8 encoding
    """
    with open(fname, "w", encoding="utf-8", errors='surrogatepass') as fp:
        fp.write(text)
        fp.flush()