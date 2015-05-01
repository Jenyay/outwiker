# -*- coding: UTF-8 -*-

import re

from externaltools.libs import ushlex
from execinfo import ExecInfo


class CommandExecParser (object):
    """
    Class for parsing text between (:exec:) and (:execend:)
    """
    def __init__ (self):
        self._joinRegexp = re.compile (r'\\\s*$\s*', re.MULTILINE)


    def parse (self, text):
        """
        Return list of the ExecInfo instances
        """
        joinedLines = self._joinRegexp.sub (u' ', text)

        lines = [line.strip()
                 for line
                 in joinedLines.split (u'\n')
                 if line.strip()]

        result = []
        for line in lines:
            items = ushlex.split (line)
            assert len (items) != 0

            command = items[0]
            params = items[1:] if len (items) > 1 else []

            result.append (ExecInfo (command, params))

        return result
