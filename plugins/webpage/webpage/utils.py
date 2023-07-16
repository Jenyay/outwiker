# -*- coding: utf-8 -*-


def isLink(text):
    lowerString = text.lower()
    return lowerString.startswith("http://") or lowerString.startswith("https://")
