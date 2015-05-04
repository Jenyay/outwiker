# -*- coding: UTF-8 -*-

from outwiker.gui.baselinkdialogcontroller import BaseLinkDialogController
from outwiker.core.defines import PAGE_ATTACH_DIR


class HtmlLinkDialogController (BaseLinkDialogController):
    @property
    def linkResult (self):
        """
        Возвращает строку, представляющую собой оформленную ссылку
        в нужном представлении (HTMl, wiki и т.п.)
        """
        return u'<a href="{link}">{comment}</a>'.format (comment=self.comment,
                                                         link=self.link)


    def createFileLink (self, fname):
        """
        Создать ссылку на прикрепленный файл
        """
        return u'{}/{}'.format (PAGE_ATTACH_DIR, fname)
