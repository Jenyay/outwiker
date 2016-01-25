# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

from outwiker.core.application import Application
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel, EVT_PAGE_TAB_CHANGED

from webpage.misc import polyActions, onPrepareHtmlEventString
from webpage.events import PrepareHtmlEventParams


class WebPageView (BaseHtmlPanel):
    def __init__ (self, parent, *args, **kwds):
        super (WebPageView, self).__init__ (parent, *args, **kwds)
        self._application = Application
        self.__htmlMenu = None

        self._application.mainWindow.updateShortcuts()
        self.mainWindow.UpdateAuiManager()

        self._application.onPageUpdate += self.__onPageUpdate
        self.Bind (EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)


    def getTextEditor(self):
        return HtmlTextEditor


    def onTabChanged (self, event):
        if self._currentpage is not None:
            if event.tab == self.RESULT_PAGE_INDEX:
                self._onSwitchToPreview()
            else:
                self._onSwitchToCode()

            self.savePageTab(self._currentpage)

        event.Skip()


    def Clear (self):
        self._application.onPageUpdate -= self.__onPageUpdate
        self.Unbind (EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)

        super (WebPageView, self).Clear()


    def _enableActions (self, enabled):
        actionController = self._application.actionController

        # Активируем / дизактивируем полиморфные действия
        map (lambda strid: actionController.enableTools (strid, enabled),
             polyActions)


    def __onPageUpdate (self, sender, **kwargs):
        if sender == self._currentpage:
            if self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
                self.updateHtml()


    def updateHtml (self):
        self._updateResult()


    def generateHtml (self, page):
        soup = BeautifulSoup (page.content, "html.parser")
        params = PrepareHtmlEventParams (self._application.selectedPage,
                                         soup)
        self._application.getEvent(onPrepareHtmlEventString)(params)
        html = params.soup.prettify()

        return html


    def removeGui (self):
        super (WebPageView, self).removeGui ()


    def _changeContentByEvent (self, page, params, event):
        event (page, params)
        return params.result
