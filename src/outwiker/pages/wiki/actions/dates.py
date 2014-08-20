# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiDateCreation (BaseAction):
    """
    Вставка команды для вывода даты создания страницы
    """
    stringId = u"WikiDateCreation"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Creation date (:crdate:)")


    @property
    def description (self):
        return _(u"Insert the creation date command (:crdate:)")


    def run (self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        text = u"(:crdate:)"

        self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText (text)
