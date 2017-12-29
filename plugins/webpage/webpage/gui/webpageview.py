# -*- coding: utf-8 -*-

from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.pages.html.basehtmlpanel import (BaseHtmlPanel,
                                               EVT_PAGE_TAB_CHANGED)

from ..misc import polyActions


class WebPageView(BaseHtmlPanel):
    def __init__(self, parent, application):
        super(WebPageView, self).__init__(parent, application)
        self.__htmlMenu = None

        self._application.mainWindow.updateShortcuts()
        self.mainWindow.UpdateAuiManager()

        self.Bind(EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)

    def getTextEditor(self):
        return HtmlTextEditor

    def onTabChanged(self, event):
        if self._currentpage is not None:
            if event.tab == self.RESULT_PAGE_INDEX:
                self._onSwitchToPreview()
            else:
                self._onSwitchToCode()

            self.savePageTab(self._currentpage)

        event.Skip()

    def Clear(self):
        self.Unbind(EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)
        super(WebPageView, self).Clear()

    def _enableActions(self, enabled):
        actionController = self._application.actionController

        # Активируем / дизактивируем полиморфные действия
        map(lambda strid: actionController.enableTools(strid, enabled),
            polyActions)

    def updateHtml(self):
        self._updateHtmlWindow()
