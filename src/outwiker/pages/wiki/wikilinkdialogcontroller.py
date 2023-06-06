# -*- coding: utf-8 -*-

from outwiker.gui.dialogs.baselinkdialogcontroller import BaseLinkDialogController
from outwiker.pages.wiki.linkcreator import LinkCreator
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.parser.tokenattach import AttachToken


class WikiLinkDialogController(BaseLinkDialogController):
    def __init__(self, application, page, dialog, selectedString):
        super().__init__(page, dialog, selectedString)
        self._application = application
        self._quotes = None

    def prepareAttachLink(self, text: str) -> str:
        if text.startswith(AttachToken.attachString):
            text = text[len(AttachToken.attachString):]

            if text.startswith('"') and text.endswith('"'):
                self._quotes = '"'
                return text[1:-1]

            if text.startswith("'") and text.endswith("'"):
                self._quotes = "'"
                return text[1:-1]

        return text

    @property
    def linkResult(self):
        """
        Возвращает строку, представляющую собой оформленную ссылку
        в нужном представлении (HTML, wiki и т.п.)
        """
        linkCreator = LinkCreator(WikiConfig(self._application.config))
        return linkCreator.create(self.link, self.comment)

    def createFileLink(self, fname):
        """
        Создать ссылку на прикрепленный файл
        """
        # Add quotes for path with spaces and slashes and if user add quotes to comment
        if ((' ' in fname or '\\' in fname or '/' in fname) or
                self._quotes is not None):
            quotes = self._quotes if self._quotes is not None else '"'
            return 'Attach:{quotes}{fname}{quotes}'.format(fname=fname, quotes=quotes)

        return 'Attach:{fname}'.format(fname=fname)
