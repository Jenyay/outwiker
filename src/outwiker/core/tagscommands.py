# -*- coding: utf-8 -*-

from typing import List

from .tagslist import TagsList


def parseTagsList(tagsString: str) -> List[str]:
    """
    Преобразовать строку тегов, разделенных запятой, в список
    """
    tags = [tag.strip() for tag in tagsString.lower().split(",")
            if len(tag.strip()) > 0]

    return tags


def getTagsString(tags: List[str]) -> str:
    """
    Получить строку тегов
    """
    return ", ".join(tags)


def removeTag(page, tag: str):
    """
    Удалить тег из страницы
    """
    taglower = tag.lower()
    pageTags = page.tags

    if taglower not in pageTags:
        return

    while taglower in pageTags:
        pageTags.remove(taglower)

    page.tags = pageTags


def appendTag(page, tag: str):
    pageTags = page.tags[:]
    pageTags.append(tag)
    page.tags = pageTags


def appendTagsList(page, tagslist):
    pageTags = page.tags[:]
    pageTags.extend(tagslist)
    page.tags = pageTags


def tagBranch(parentPage, tags):
    """
    Добавить теги к ветке, начиная с родительской страницы

    parentPage - страница, с которой начинается ветка
    tags - список тегов для добавления
    """
    if "tags" in dir(parentPage):
        appendTagsList(parentPage, tags)
    [tagBranch(child, tags) for child in parentPage.children]


def removeTagsFromBranch(parentPage, tags):
    """
    Удалить теги из ветки, начиная с родительской страницы

    parentPage - страницы, с которой начинается ветка
    tags - список тегов, которые надо удалить
    """
    if "tags" in dir(parentPage):
        [removeTag(parentPage, tag) for tag in tags]

    [removeTagsFromBranch(child, tags) for child in parentPage.children]


def renameTag(wikiroot, oldName, newName):
    """
    Переименовать тег
    """
    tags = TagsList(wikiroot)
    for page in tags[oldName]:
        removeTag(page, oldName)
        appendTag(page, newName)
