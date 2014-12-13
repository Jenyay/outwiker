# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class PlotAction (BaseAction):
    """
    Описание действия
    """
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"DataGraph_Plot"


    @property
    def title (self):
        return _(u"Plot graph (:plot:)")


    @property
    def description (self):
        return _(u"[DataGraph] Insert (:plot:) command for graph plotting")


    def run (self, params):
        startCommand = u'(:plot:)'
        endCommand = u'(:plotend:)'

        pageView = self._getPageView()
        pageView.codeEditor.turnText (startCommand, endCommand)


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView
