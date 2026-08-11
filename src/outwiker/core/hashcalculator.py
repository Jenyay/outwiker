# -*- coding: utf-8 -*-

import os
import os.path
import hashlib
from typing import Callable, List

from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiPage


class BaseHashCalculator:
    def __init__(self, application: Application):
        self._application = application
        self._content_functions: List[Callable[[WikiPage, List[str]], None]] = []

    def getFullContent(self, page: WikiPage) -> List[str]:
        """
        Get the content for calculating the checksum, which determines
        whether the page needs to be updated
        """
        content: List[str] = []
        for func in self._content_functions:
            func(page, content)
        return content

    def addContentFunction(self, func: Callable[[WikiPage, List[str]], None]):
        self._content_functions.append(func)

    @property
    def application(self):
        return self._application

    def getHash(self, page: WikiPage) -> str:
        text = "".join(self.getFullContent(page))
        return hashlib.md5(text.encode("utf-8", errors="ignore")).hexdigest()


class SimpleHashCalculator(BaseHashCalculator):
    def __init__(self, application: Application):
        super().__init__(application)
        self.addContentFunction(self._getPageModDateContent)
        self.addContentFunction(self._getAttachContent)
        self.addContentFunction(self._getPluginsListContent)
        self.addContentFunction(self._getPageChildrenContent)

    def _getPageModDateContent(self, page: WikiPage, content: List[str]) -> None:
        content.append(str(page.datetime))

    def _getPageChildrenContent(self, page: WikiPage, content: List[str]) -> None:
        for child in page.children:
            content.append(child.display_title)

    def _getPluginsListContent(self, page: WikiPage, content: List[str]) -> None:
        """
        Create a list of plugins with version numbers
        Returns a string
        """
        if len(self._application.plugins) == 0:
            return

        items = sorted(
            [plugin.name + str(plugin.version) for plugin in self._application.plugins]
        )
        for item in items:
            content.append(item)

    def _getAttachContent(self, page: WikiPage, content: List[str], dirname=".") -> None:
        """
        Form a list of string elements for hash calculation based on data in the nested
        subdirectory dirname (path relative to __attach)
        page - the page for which we collect the attachments list
        """
        attach = Attachment(page)
        attachroot = attach.getAttachPath()

        attachlist = attach.getAttachRelative(dirname)
        attachlist.sort(key=str.lower)

        for fname in attachlist:
            fullpath = os.path.join(attachroot, dirname, fname)

            # Skip directories that start with __
            if not os.path.isdir(fname) or not fname.startswith("__"):
                try:
                    content.append(fname)
                    content.append(str(os.stat(fullpath).st_mtime))

                    if os.path.isdir(fullpath):
                        self._getAttachContent(
                            page, content, os.path.join(dirname, fname)
                        )
                except OSError:
                    # If there are access issues with the file, we don't
                    # pay attention to them here
                    pass
