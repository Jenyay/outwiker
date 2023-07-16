# -*- coding: utf-8 -*-

from outwiker.gui.dialogs.baselinkdialogcontroller import BaseLinkDialogController
from outwiker.core.defines import PAGE_ATTACH_DIR


class HtmlLinkDialogController (BaseLinkDialogController):
    def prepareAttachLink(self, text: str) -> str:
        attach_prefix = PAGE_ATTACH_DIR

        if (text.startswith(attach_prefix + '/') or
                text.startswith(attach_prefix + '\\')):
            text = text[len(attach_prefix) + 1:]
            # text = text.replace('\\', '/')
        return text

    @property
    def linkResult(self):
        """
        Возвращает строку, представляющую собой оформленную ссылку
        в нужном представлении (HTMl, wiki и т.п.)
        """
        return '<a href="{link}">{comment}</a>'.format(comment=self.comment,
                                                       link=self.link)

    def createFileLink(self, fname):
        """
        Создать ссылку на прикрепленный файл
        """
        return '{}/{}'.format(PAGE_ATTACH_DIR, fname.replace('\\', '/'))
