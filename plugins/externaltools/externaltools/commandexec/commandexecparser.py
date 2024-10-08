# -*- coding: utf-8 -*-

import os.path
import re
import shlex

from outwiker.api.core.attachment import Attachment
from outwiker.api.core.defines import PAGE_CONTENT_FILE

from .execinfo import ExecInfo
from . import commandparams


class CommandExecParser:
    """
    Class for parsing text between (:exec:) and (:execend:)
    """

    def __init__(self, page):
        self._page = page

        self._commentsRegexp = re.compile(r"^#.*?$", re.MULTILINE)
        self._joinRegexp = re.compile(r"\\\s*$\s*", re.MULTILINE)

    def parse(self, text):
        """
        Return list of the ExecInfo instances
        """
        text = self._commentsRegexp.sub("", text)
        text = self._joinRegexp.sub(" ", text)

        lines = [line.strip() for line in text.split("\n") if line.strip()]

        result = []
        for line in lines:
            items = shlex.split(line)
            assert len(items) != 0

            params = [self._substituteMacros(item) for item in items]

            result.append(ExecInfo(params[0], params[1:]))

        return result

    def _substituteMacros(self, paramText):
        result = self._substitutePage(paramText)
        result = self._substituteHtml(result)
        result = self._substituteFolder(result)
        result = self._substituteAttach(result)

        return result

    def _substitutePage(self, paramText):
        pagePath = os.path.join(self._page.path, PAGE_CONTENT_FILE)
        return paramText.replace(commandparams.MACROS_PAGE, pagePath)

    def _substituteHtml(self, paramText):
        htmlPath = os.path.join(self._page.path, "__content.html")
        return paramText.replace(commandparams.MACROS_HTML, htmlPath)

    def _substituteFolder(self, paramText):
        return paramText.replace(commandparams.MACROS_FOLDER, self._page.path)

    def _substituteAttach(self, paramText):
        attachPath = Attachment(self._page).getAttachPath(True)
        if attachPath.endswith("/") or attachPath.endswith("\\"):
            attachPath = attachPath[:-1]

        # Substitute %attach%
        result = paramText.replace(commandparams.MACROS_ATTACH, attachPath)

        # Substitute Attach:
        result = self._substituteAttachWiki(result)

        return result

    def _substituteAttachWiki(self, paramText):
        attachWiki = "Attach:"
        attachPath = Attachment(self._page).getAttachPath(False)

        # "Attach:" may be at the beginning only
        if not paramText.startswith(attachWiki):
            return paramText

        fname = paramText[len(attachWiki) :]

        return os.path.join(attachPath, fname)
