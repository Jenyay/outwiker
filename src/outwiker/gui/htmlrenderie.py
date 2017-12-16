# -*- coding: UTF-8 -*-

import urllib.request, urllib.parse, urllib.error

import wx
import wx.lib.iewin

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
from outwiker.core.defines import APP_DATA_KEY_ANCHOR
from outwiker.gui.htmlrender import HtmlRender
from outwiker.gui.htmlcontrollerie import UriIdentifierIE
from outwiker.gui.defines import (ID_MOUSE_LEFT,
                                  ID_KEY_CTRL,
                                  ID_KEY_SHIFT)
from outwiker.gui.guiconfig import GeneralGuiConfig


class HtmlRenderIE (HtmlRender):
    """
    Класс для рендеринга HTML с использованием движка IE под Windows
    """
    def __init__ (self, parent):
        HtmlRender.__init__ (self, parent)
        config = GeneralGuiConfig(Application.config)

        self.render = wx.lib.iewin.IEHtmlWindow (self)
        self.render.silent = not config.debug.value

        # Подпишемся на события IE
        self.render.AddEventSink(self)

        self.canOpenUrl = False                # Можно ли открывать ссылки

        self.__layout()

        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_COPY)
        self.Bind (wx.EVT_MENU, self.__onCopyFromHtml, id = wx.ID_CUT)


    def Print (self):
        self.render.Print (True)


    def SetPage (self, htmltext, basepath):
        """
        Загрузить страницу из строки
        htmltext - текст страницы
        basepath - путь, относительно которого отсчитываются относительные пути (НЕ ИСПОЛЬЗУЕТСЯ!!!)
        """
        self.canOpenUrl = True
        self.render.LoadString (htmltext)
        self.canOpenUrl = False


    def StatusTextChange(self, status):
        statustext = u""

        if len (status) != 0:
            (url, page, filename, anchor) = self.__identifyUri (status)

            if page is not None:
                text = page.display_subpath
                if anchor is not None:
                    text = u"{}/{}".format (text, anchor)

                statustext = text
            elif filename is not None:
                statustext = filename
            elif anchor is not None:
                statustext = anchor
            else:
                statustext = status

        self.setStatusText (status, statustext)


    def __onCopyFromHtml(self, event):
        document = self.render.document
        selection = document.selection

        if selection is not None:
            selrange = selection.createRange()
            if selrange is not None:
                outwiker.core.commands.copyTextToClipboard (selrange.text)
                event.Skip()


    def __layout (self):
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.render, 1, wx.EXPAND)

        self.SetSizer(self.box)
        self.Layout()


    def LoadPage (self, fname):
        self.canOpenUrl = True
        path = fname

        if APP_DATA_KEY_ANCHOR in Application.sharedData:
            path += Application.sharedData[APP_DATA_KEY_ANCHOR]
            del Application.sharedData[APP_DATA_KEY_ANCHOR]

        self.render.Navigate (path)


    def __cleanUpUrl (self, href):
        """
        Почистить ссылку, убрать file:///
        """
        result = self.__removeFileProtokol (href)
        result = urllib.parse.unquote (result)
        result = result.replace ("/", u"\\")

        return result


    def __removeFileProtokol (self, href):
        """
        Избавиться от протокола file:///, то избавимся от этой надписи
        """
        fileprotocol = u"file:///"
        if href.startswith (fileprotocol):
            return href[len (fileprotocol):]

        return href


    def BeforeNavigate2 (self, this, pDisp, URL, Flags,
                         TargetFrameName, PostData, Headers, Cancel):
        href = URL[0]
        curr_href = self.__cleanUpUrl (self.render.locationurl)

        # Пока другого признака о том, что пытаемся открыть встроенный фрейм, не нашел
        if 'LocationURL' in dir (pDisp) and pDisp.LocationURL == "about:blank":
            Cancel[0] = False
            return

        if self.canOpenUrl or href == curr_href:
            Cancel[0] = False
            self.canOpenUrl = False
        else:
            Cancel[0] = True
            self.__onLinkClicked (href)


    def NewWindow3 (self, this, pDisp, Cancel, dwFlags, currentURL, href):
        Cancel[0] = True

        (url, page, filename, anchor) = self.__identifyUri (href)
        if page is not None:
            Application.mainWindow.tabsController.openInTab (page, True)


    def __identifyUri (self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename)
        """
        identifier = UriIdentifierIE (self._currentPage,
                                      self.__cleanUpUrl (self.render.locationurl))

        return identifier.identify (href)


    def __getKeyCode (self):
        modifier = 0

        if wx.GetKeyState(wx.WXK_SHIFT):
            modifier |= ID_KEY_SHIFT

        if wx.GetKeyState(wx.WXK_CONTROL):
            modifier |= ID_KEY_CTRL

        return modifier


    def __onLinkClicked (self, href):
        """
        Клик по ссылке
        """
        (url, page, filename, anchor) = self.__identifyUri (href)

        button = ID_MOUSE_LEFT
        modifier = self.__getKeyCode()

        params = self._getClickParams (href,
                                       button,
                                       modifier,
                                       url,
                                       page,
                                       filename,
                                       anchor)

        Application.onLinkClick (self._currentPage, params)
        if params.process:
            return

        if url is not None:
            self.openUrl (url)
        elif page is not None and modifier == ID_KEY_CTRL:
            if anchor is not None:
                Application.sharedData[APP_DATA_KEY_ANCHOR] = anchor
            Application.mainWindow.tabsController.openInTab (page, True)
        elif page is not None:
            if anchor is not None:
                Application.sharedData[APP_DATA_KEY_ANCHOR] = anchor
            self._currentPage.root.selectedPage = page
        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile (filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                outwiker.core.commands.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)
        elif anchor is not None:
            self.LoadPage (href)

