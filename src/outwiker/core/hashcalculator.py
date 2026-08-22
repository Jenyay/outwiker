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

        self._WATCHED_ATTACHMENTS_PARAM = "watch_attachments"
        self._watched_attachments_separator = "|"

    def clearWatchAttachments(self, page: WikiPage):
        registry = page.root.registry.get_page_registry(page)
        registry.set(self._WATCHED_ATTACHMENTS_PARAM, "")

    def getWatchAttachments(self, page: WikiPage) -> List[str]:
        registry = page.root.registry.get_page_registry(page)
        return [
            item
            for item in registry.getstr(
                self._WATCHED_ATTACHMENTS_PARAM, default=""
            ).split(self._watched_attachments_separator)
            if len(item) != 0
        ]

    def addWatchAttachments(self, page: WikiPage, attachments_relative: List[str]):
        if not attachments_relative:
            return

        registry = page.root.registry.get_page_registry(page)
        src_str_items = registry.getstr(self._WATCHED_ATTACHMENTS_PARAM, default="")
        new_items = self._watched_attachments_separator.join(attachments_relative)
        new_str_items = (
            new_items
            if not src_str_items
            else self._watched_attachments_separator.join([src_str_items, new_items])
        )
        registry.set(self._WATCHED_ATTACHMENTS_PARAM, new_str_items)

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

    def _getAttachContent(self, page: WikiPage, content: List[str]) -> None:
        """
        Form a list of string elements for hash calculation based on data in the nested
        subdirectory dirname (path relative to __attach)
        page - the page for which we collect the attachments list
        """
        attach = Attachment(page)
        attachroot = attach.getAttachPath()
        watch_attach_list = [
            os.path.join(attachroot, fname) for fname in self.getWatchAttachments(page)
        ]

        for fullpath in watch_attach_list:
            if not os.path.exists(fullpath):
                content.append("None")
                continue

            try:
                content.append(str(os.stat(fullpath).st_mtime))
            except OSError:
                content.append("None")
