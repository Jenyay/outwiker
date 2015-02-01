# -*- coding: UTF-8 -*-

from outwiker.gui.baselinkdialogcontroller import BaseLinkDialogController
from outwiker.pages.wiki.linkcreator import LinkCreator
from outwiker.pages.wiki.wikiconfig import WikiConfig


class WikiLinkDialogController (BaseLinkDialogController):
    def __init__ (self, application, page, dialog, selectedString):
        super (WikiLinkDialogController, self).__init__ (page, dialog, selectedString)
        self._application = application


    @property
    def linkResult (self):
        """
        Возвращает строку, представляющую собой оформленную ссылку
        в нужном представлении (HTML, wiki и т.п.)
        """
        linkCreator = LinkCreator (WikiConfig (self._application.config))
        return linkCreator.create (self.link, self.comment)


    def createFileLink (self, fname):
        """
        Создать ссылку на прикрепленный файл
        """
        return u'Attach:' + fname
