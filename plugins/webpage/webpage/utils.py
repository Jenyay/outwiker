# -*- coding: UTF-8 -*-


def isLink(text):
    lowerString = text.lower()
    return (lowerString.startswith(u'http://') or
            lowerString.startswith(u'https://'))
