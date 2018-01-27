# -*- coding: utf-8 -*-

from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel

from ..misc import polyActions


class WebPageView(BaseHtmlPanel):
    def __init__(self, parent, application):
        super(WebPageView, self).__init__(parent, application)
        self.__htmlMenu = None

        self.mainWindow.UpdateAuiManager()

        self._application.onPageModeChange += self.onTabChanged

    def getTextEditor(self):
        return HtmlTextEditor

    def onTabChanged(self, page, params):
        if self._currentpage is not None:
            if params.pagemode == PAGE_MODE_PREVIEW:
                self._onSwitchToPreview()
            elif params.pagemode == PAGE_MODE_TEXT:
                self._onSwitchToCode()
            else:
                assert False

            self.savePageTab(self._currentpage)

    def Clear(self):
        self._application.onPageModeChange -= self.onTabChanged
        super(WebPageView, self).Clear()

    def _enableActions(self, enabled):
        actionController = self._application.actionController

        # Активируем / дизактивируем полиморфные действия
        map(lambda strid: actionController.enableTools(strid, enabled),
            polyActions)

    def updateHtml(self):
        self._updateHtmlWindow()
