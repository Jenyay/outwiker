# -*- coding: utf-8 -*-

from outwiker.api.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW
from outwiker.api.gui.controls import HtmlTextEditor
from outwiker.api.pages.html.gui import BaseHtmlPanel

from ..misc import polyActions


class WebPageView(BaseHtmlPanel):
    def __init__(self, parent, application):
        super().__init__(parent, application)

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
        for strid in polyActions:
            actionController.enableTools(strid, enabled)

    def updateHtml(self):
        self._updateHtmlWindow()
