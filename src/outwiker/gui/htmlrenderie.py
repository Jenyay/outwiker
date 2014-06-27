#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import urllib

import wx
import wx.lib.iewin

from .htmlrender import HtmlRender
import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
from .htmlcontrollerie import UriIdentifierIE


class HtmlRenderIE (HtmlRender):
    """
    Класс для рендеринга HTML с использованием движка IE под Windows
    """
    def __init__ (self, parent):
        HtmlRender.__init__ (self, parent)

        self.render = wx.lib.iewin.IEHtmlWindow (self)

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
        if len (status) != 0:
            (url, page, filename, anchor) = self.__identifyUri (status)

            if page is not None:
                text = page.subpath
                if anchor is not None:
                    text = u"{}/{}".format (text, anchor)

                outwiker.core.commands.setStatusText (text, self._status_item)
            elif filename is not None:
                outwiker.core.commands.setStatusText (filename, self._status_item)
            elif anchor is not None:
                outwiker.core.commands.setStatusText (anchor, self._status_item)
            else:
                outwiker.core.commands.setStatusText (status, self._status_item)
        else:
            outwiker.core.commands.setStatusText (status, self._status_item)


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

        if self._anchor is not None:
            path += self._anchor
            self._anchor = None

        self.render.Navigate (path)


    def __cleanUpUrl (self, href):
        """
        Почистить ссылку, убрать file:///
        """
        result = self.__removeFileProtokol (href)
        result = urllib.unquote (result)
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
        if pDisp.LocationURL == "about:blank":
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


    def __onLinkClicked (self, href):
        """
        Клик по ссылке
        """
        (url, page, filename, anchor) = self.__identifyUri (href)
        ctrlstate = wx.GetKeyState(wx.WXK_CONTROL)

        if url is not None:
            self.openUrl (url)

        elif page is not None and ctrlstate:
            self._anchor = anchor
            Application.mainWindow.tabsController.openInTab (page, True)

        elif page is not None:
            self._anchor = anchor
            self._currentPage.root.selectedPage = page

        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile (filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                outwiker.core.commands.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)

        elif anchor is not None:
            self.LoadPage (href)
