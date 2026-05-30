# -*- coding: utf-8 -*-

from typing import List

from .tagslist import TagsList


def parseTagsList(tagsString: str) -> List[str]:
    """
    Convert a comma-separated tag string to a list
    """
    tags = [tag.strip() for tag in tagsString.lower().split(",")
            if len(tag.strip()) > 0]

    return tags


def getTagsString(tags: List[str]) -> str:
    """
    Get a tag string
    """
    return ", ".join(tags)


def removeTag(page, tag: str):
    """
    Remove a tag from the page
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
    Add tags to a branch starting from the parent page

    parentPage - the page where the branch starts
    tags - list of tags to add
    """
    if "tags" in dir(parentPage):
        appendTagsList(parentPage, tags)
    [tagBranch(child, tags) for child in parentPage.children]


def removeTagsFromBranch(parentPage, tags):
    """
    Remove tags from a branch starting from the parent page

    parentPage - the page where the branch starts
    tags - list of tags to remove
    """
    if "tags" in dir(parentPage):
        [removeTag(parentPage, tag) for tag in tags]

    [removeTagsFromBranch(child, tags) for child in parentPage.children]


def renameTag(wikiroot, oldName, newName):
    """
    Rename a tag
    """
    tags = TagsList(wikiroot)
    for page in tags[oldName]:
        removeTag(page, oldName)
        appendTag(page, newName)
