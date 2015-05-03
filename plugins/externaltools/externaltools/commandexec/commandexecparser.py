# -*- coding: UTF-8 -*-

import os.path
import re

from externaltools.libs import ushlex
from execinfo import ExecInfo
import commandparams


class CommandExecParser (object):
    """
    Class for parsing text between (:exec:) and (:execend:)
    """
    def __init__ (self, page):
        self._page = page

        self._joinRegexp = re.compile (r'\\\s*$\s*', re.MULTILINE)
        self._macrosPage = re.compile (commandparams.MACROS_PAGE, re.I)
        self._macrosHtml = re.compile (commandparams.MACROS_HTML, re.I)
        self._macrosFolder = re.compile (commandparams.MACROS_FOLDER, re.I)


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
            params = [self._substituteMacros (item) for item in items[1:]]

            result.append (ExecInfo (command, params))

        return result


    def _substituteMacros (self, paramText):
        result = self._substitutePage (paramText)
        result = self._substituteHtml (result)
        result = self._substituteFolder (result)

        return result


    def _substitutePage (self, paramText):
        pagePath = os.path.join (self._page.path, u'__page.text')
        return self._macrosPage.sub (pagePath, paramText)


    def _substituteHtml (self, paramText):
        htmlPath = os.path.join (self._page.path, u'__content.html')
        return self._macrosHtml.sub (htmlPath, paramText)


    def _substituteFolder (self, paramText):
        return self._macrosFolder.sub (self._page.path, paramText)
