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


def removeTag (page, tag):
    """
    Удалить тег из страницы
    """
    pageTags = page.tags[:]

    while tag in pageTags:
        pageTags.remove (tag)

    page.tags = pageTags


def appendTag (page, tag):
    pageTags = page.tags[:]
    pageTags.append (tag)
    page.tags = pageTags
