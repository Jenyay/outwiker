# -*- coding: UTF-8 -*-

from outwiker.actions.showhidebase import ShowHideBaseAction


class ShowHideAttachesAction (ShowHideBaseAction):
    """
    Показать / скрыть панель с прикрепленными файлами
    """
    stringId = u"ShowHideAttaches"

    def __init__ (self, application):
        super (ShowHideAttachesAction, self).__init__ (application)


    @property
    def title (self):
        return _(u"Attachments")


    @property
    def description (self):
        return _(u"Show / hide a attachments panel")


    def getPanel (self):
        return self._application.mainWindow.attachPanel
