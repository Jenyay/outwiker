# -*- coding: UTF-8 -*-

import os

import wx
import wx.html

import outwiker.core.system
import outwiker.core.commands


class HtmlRenderWX (wx.Panel):
    """
    Класс для рендеринга HTML с использованием встроенного в wxPython рендера
    """
    def __init__ (self, parent, *args, **kwds):
        wx.Panel.__init__ (self, parent, *args, **kwds)

        self.render = wx.html.HtmlWindow (self, style=wx.html.HW_SCROLLBAR_AUTO)

        self._status_item = 0
        self.__layout()

        self._currentPage = None

        self.render.Bind (wx.html.EVT_HTML_LINK_CLICKED, self.onLinkClicked)
        self.render.Bind (wx.html.EVT_HTML_CELL_HOVER, self.onCellHover)
        self.render.Bind (wx.EVT_ENTER_WINDOW, self.onMouseEnter)
        self.render.Bind (wx.EVT_MOTION, self.onMouseMove)

        self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_COPY)
        self.Bind (wx.EVT_MENU, self.onCopyFromHtml, id = wx.ID_CUT)


    def __layout (self):
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.render, 1, wx.EXPAND)

        self.SetSizer(self.box)
        self.Layout()


    def LoadPage (self, fname):
        self.render.LoadPage (fname)


    def SetPage (self, html):
        self.render.SetPage (html)


    def onCellHover (self, event):
        cell = event.GetCell()
        text = cell.GetLink().GetHref() if cell.GetLink() else u""
        outwiker.core.commands.setStatusText(text, self._status_item)


    def onMouseMove (self, event):
        outwiker.core.commands.setStatusText(u"", self._status_item)
        event.Skip()


    def onMouseEnter (self, event):
        self.render.SetFocus()


    def onCopyFromHtml(self, event):
        text = self.render.SelectionToText()
        if len(text) == 0:
            return

        outwiker.core.commands.copyTextToClipboard(text)
        event.Skip()


    @property
    def page (self):
        return self._currentPage


    @page.setter
    def page (self, value):
        self._currentPage = value


    def onLinkClicked (self, event):
        """
        Клик по ссылке
        """
        info = event.GetLinkInfo()
        href = info.GetHref()

        if self.__isUrl (href):
            self.openUrl (href)
        else:
            page = self.__findWikiPage (href)
            file = self.__findFile (href)

            if page is not None:
                self._currentPage.root.selectedPage = page
            elif file is not None:
                try:
                    outwiker.core.system.getOS().startFile (file)
                except OSError:
                    text = _(u"Can't execute file '%s'") % file
                    outwiker.core.commands.MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)



    def __isUrl (self, href):
        return (href.lower().startswith ("http://") or
                href.lower().startswith ("https://") or
                href.lower().startswith ("ftp://") or
                href.lower().startswith ("mailto:"))


    def __findFile (self, href):
        path = os.path.join (self._currentPage.path, href)
        if os.path.exists (path):
            return path


    def __findWikiPage (self, subpath):
        """
        Попытка найти страницу вики, если ссылка, на которую щелкнули не интернетная (http, ftp, mailto)
        """
        assert self._currentPage is not None

        newSelectedPage = None

        if subpath[0] == "/":
            # Поиск страниц осуществляем только с корня
            newSelectedPage = self._currentPage.root[subpath[1:]]
        else:
            # Сначала попробуем найти вложенные страницы с таким subpath
            newSelectedPage = self._currentPage[subpath]

            if newSelectedPage is None:
                # Если страница не найдена, попробуем поискать, начиная с корня
                newSelectedPage = self._currentPage.root[subpath]

        return newSelectedPage


    def openUrl (self, href):
        """
        Открыть ссылку в браузере (или почтовый адрес в почтовике)
        """
        try:
            outwiker.core.system.getOS().startFile (href)
        except OSError:
            text = _(u"Can't execute file '%s'") % (href)
            outwiker.core.commands.MessageBox (text, "Error", wx.ICON_ERROR | wx.OK)
