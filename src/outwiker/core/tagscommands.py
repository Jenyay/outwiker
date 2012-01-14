#!/usr/bin/python
# -*- coding: UTF-8 -*-

def parseTagsList (tagsString):
    """
    Преобразовать строку тегов, разделенных запятой, в список
    """
    tags = [tag.strip() for tag in tagsString.split (",") 
            if len (tag.strip()) > 0]

    return tags


def getTagsString (tags):
    """
    Получить строку тегов
    """
    result = u""
    count = len (tags)

    for n in range (count):
        result += tags[n]
        if n != count - 1:
            result += ", "

    return result
