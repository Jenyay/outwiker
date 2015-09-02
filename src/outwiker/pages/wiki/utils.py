# -*- coding: UTF-8 -*-

import re

from outwiker.pages.wiki.parser.tokencommand import CommandToken


def getCommandsByPos (text, position):
    regex = re.compile (CommandToken.regex, re.U | re.M | re.S | re.X)
    result = []

    startpos = 0
    endpos = len (text)

    found = True

    while found:
        parsedText = text[startpos: endpos]
        found = False

        matches = list (regex.finditer (parsedText))
        if not matches:
            break

        for match in matches:
            if (position > match.start() + startpos and
                    position <= match.end() + startpos - 1 and
                    not match.groupdict()['name'].endswith(u'end')):
                result.append (match)
                startpos = startpos + match.start() + 1
                endpos = startpos + match.end()
                found = True

    return result
