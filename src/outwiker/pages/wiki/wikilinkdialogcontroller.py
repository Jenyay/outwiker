# -*- coding: utf-8 -*-

from outwiker.gui.dialogs.baselinkdialogcontroller import BaseLinkDialogController
from outwiker.pages.wiki.linkcreator import LinkCreator
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.parser.tokenattach import AttachToken


class WikiLinkDialogController(BaseLinkDialogController):
    def __init__(self, application, page, dialog, selectedString):
        super().__init__(page, dialog, selectedString)
        self._application = application

    def prepareAttachLink(self, text: str) -> str:
        if text.startswith(AttachToken.attachString):
            text = text[len(AttachToken.attachString):]
            # text = text.replace('\\', '/')

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
        return 'Attach:' + fname
