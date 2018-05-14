# -*- coding: UTF-8 -*-


def splitTags(tagsStr):
    """
    Return list of the tags. Tags must be comma separated with optional spaces.
    The tags will be in lower case.
    """
    return [tag.strip().lower() for tag in tagsStr.split(u',') if tag.strip()]
