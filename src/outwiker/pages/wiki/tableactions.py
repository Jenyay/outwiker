# -*- coding: UTF-8 -*-

import re

from outwiker.pages.wiki.utils import getCommandsByPos


def getTableByPos (text, position):
    """
    Return suffix for command name for most nested (:tableNN:) command in the position
    """
    regex = re.compile (r'table(?P<suffix>\d*)$', re.UNICODE)
    matches = getCommandsByPos (text, position)
    matches.reverse()

    for match in matches:
        name = match.groupdict()['name']
        tableMatch = regex.match (name)
        if tableMatch:
            return tableMatch.groupdict()['suffix']

    return None
