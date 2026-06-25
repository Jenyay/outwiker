# -*- coding: utf-8 -*-

import os
import os.path
import hashlib
from abc import ABCMeta, abstractmethod
from typing import List

from outwiker.core.attachment import Attachment

class BaseHashCalculator(metaclass=ABCMeta):
    def __init__(self, application):
        self._application = application

    @abstractmethod
    def getFullContent(self, page) -> List[str]:
        """
        Get the content for calculating the checksum, which determines
        whether the page needs to be updated
        """

    @property
    def application(self):
        return self._application

    def getHash(self, page) -> str:
        text = "".join(self.getFullContent(page))
        return hashlib.md5(text.encode("utf-8", errors="ignore")).hexdigest()


class SimpleHashCalculator(BaseHashCalculator):
    def getFullContent(self, page) -> List[str]:
        """
        Get the content for calculating the checksum, which determines
        whether the page needs to be updated
        """
        # Here we accumulate the list of interesting strings (by which we determine
        # whether the page has changed)
        items: List[str] = []

        self._getPageTitleContent(page, items)
        self._getPageContent(page, items)
        self._getDirContent(page, items)
        self._getPluginsListContent(items)
        self._getPageChildrenContent(page, items)
        return items

    def _getPageTitleContent(self, page, content: List[str]) -> None:
        content.append(page.title)

    def _getPageContent(self, page, content: List[str]) -> None:
        content.append(page.content)

    def _getPageChildrenContent(self, page, content: List[str]) -> None:
        for child in page.children:
            content.append(child.display_title)

    def _getPluginsListContent(self, content: List[str]) -> None:
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

    def _getDirContent(self, page, content: List[str], dirname=".") -> None:
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
                        self._getDirContent(page, content, os.path.join(dirname, fname))
                except OSError:
                    # If there are access issues with the file, we don't
                    # pay attention to them here
                    pass
