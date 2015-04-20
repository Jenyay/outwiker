# -*- coding: UTF-8 -*-

import re

import lib.ushlex


class ExecInfo (object):
    """
    Contain single command.
        command - program for executing
        params - list of the program params
    """
    def __init__ (self, command, params):
        self.command = command
        self.params = params[:]



class CommandExecParser (object):
    def __init__ (self):
        self._joinRegexp = re.compile (r'\\\s*$\s*', re.MULTILINE)


    """
    Class for parsing text between (:exec:) and (:execend:)
    """
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
            items = lib.ushlex.split (line)
            assert len (items) != 0

            command = items[0]
            params = items[1:] if len (items) > 1 else []

            result.append (ExecInfo (command, params))

        return result
