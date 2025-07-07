# -*- coding: utf-8 -*-

from abc import abstractmethod
import logging
import os
import urllib.request
import urllib.parse
import urllib.error

import wx

import outwiker.core.system
from outwiker.app.services.messages import showError
from outwiker.core.defines import APP_DATA_KEY_ANCHOR
from outwiker.gui.defines import ID_KEY_CTRL, ID_MOUSE_LEFT
from outwiker.utilites.textfile import readTextFile


from .htmlrender import HtmlRenderBase, HTMLRenderForPageMixin
from .urirecognizers import (
    URLRecognizer,
    AnchorRecognizerWebKit,
    FileRecognizerWebKit,
    PageRecognizerWebKit,
)

logger = logging.getLogger("outwiker.gui.htmlrenderwebkit")


class HtmlRenderWebKitBase(HtmlRenderBase):
    """
    A base class for HTML render. Engine - WebKit.
    """

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._basepath = None

        self.Awake()
        self.Bind(wx.EVT_CLOSE, handler=self._onClose)

    @abstractmethod
    def _onLinkClicked(self, href: str) -> bool:
        pass

    @abstractmethod
    def LoadPage(self, fname: str) -> None:
        pass

    def _createRender(self):
        import wx.html2

        return wx.html2.WebView.New(self)

    def getBasePath(self) -> str:
        return self._basepath

    def Print(self):
        self.render.Print()

    def SetPage(self, htmltext, basepath, anchor=None):
        self._basepath = basepath
        path = self._pathToURL(basepath)
        if anchor:
            path += anchor

        self.canOpenUrl += 1
        self.render.SetPage(htmltext, path)

    def Sleep(self):
        import wx.html2 as webview

        self.render.Unbind(webview.EVT_WEBVIEW_NAVIGATING, handler=self._onNavigating)
        self.Unbind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_COPY)
        self.Unbind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_CUT)

    def Awake(self):
        self.canOpenUrl = 0
        self._navigate_id = 1

        import wx.html2 as webview

        self.Bind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_CUT)
        self.render.Bind(webview.EVT_WEBVIEW_NAVIGATING, handler=self._onNavigating)

    def _pathToURL(self, path: str) -> str:
        """
        Convert file system path to file:// URL
        """
        return "file://" + urllib.parse.quote(path)

    def _onClose(self, event):
        import wx.html2 as webview

        self.render.Unbind(webview.EVT_WEBVIEW_NAVIGATING, handler=self._onNavigating)
        self.render.Stop()
        event.Skip()

    def _onCopyFromHtml(self, event):
        self.render.Copy()
        event.Skip()

    def _onNavigating(self, event):
        nav_id = self._navigate_id
        self._navigate_id += 1

        logger.debug(
            "_onNavigating (%d) begin. canOpenUrl = %r", nav_id, self.canOpenUrl
        )

        # Проверка на то, что мы не пытаемся открыть вложенный фрейм
        frame = event.GetTarget()
        if frame:
            logger.debug("_onNavigating (%d) frame=%s", nav_id, frame)
            logger.debug("_onNavigating (%d) end", nav_id)
            return

        href = event.GetURL()
        curr_href = self.render.GetCurrentURL()
        logger.debug(
            "_onNavigating (%d). href=%s; curr_href=%s; canOpenUrl=%r",
            nav_id,
            href,
            curr_href,
            self.canOpenUrl
        )

        # Open empty page
        if href == "about:blank" or href == "":
            logger.debug("_onNavigating. Skip about:blank")
            event.Veto()
            return

        # Link clicked
        if self.canOpenUrl == 0:
            logger.debug("_onNavigating (%d). Link clicked.", nav_id)
            processed = self._onLinkClicked(href)
            if processed:
                event.Veto()
                logger.debug("_onNavigating (%d) end. Veto", nav_id)
            else:
                logger.debug(
                    "_onNavigating (%d) end. Allow href processing. href=%s",
                    nav_id,
                    href,
                )
            return

        self.canOpenUrl -= 1

        logger.debug("_onNavigating (%d) end. canOpenUrl=%r", nav_id, self.canOpenUrl)


class HtmlRenderWebKitForPage(HtmlRenderWebKitBase, HTMLRenderForPageMixin):
    """
    HTML render for using as note page render. Engine - WebKit.
    """

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._currentPage = None

    @property
    def page(self):
        return self._currentPage

    @page.setter
    def page(self, value):
        self._currentPage = value

    def LoadPage(self, fname):
        self.render.Stop()

        try:
            html = readTextFile(fname)
        except IOError:
            text = _("Can't read file %s") % (fname)
            self.canOpenUrl += 1
            self.SetPage(text, os.path.dirname(fname))

        basepath = os.path.dirname(fname)

        if not basepath.endswith("/"):
            basepath += "/"

        # Add anchor for references
        anchor = None
        if APP_DATA_KEY_ANCHOR in self._application.sharedData:
            anchor = self._application.sharedData[APP_DATA_KEY_ANCHOR]
            del self._application.sharedData[APP_DATA_KEY_ANCHOR]

        self.SetPage(html, basepath, anchor)

    def _identifyUri(self, href):
        """
        Recognize href type and return tuple (url, page, filename, anchor).
        Every tuple item may be None.
        """
        uri = self.render.GetCurrentURL()

        logger.debug("_identifyUri. href=%s", href)
        logger.debug("_identifyUri. current URI=%s", uri)

        if uri is not None:
            basepath = self.getBasePath()

            url = URLRecognizer(basepath).recognize(href)
            page = PageRecognizerWebKit(basepath, self._application).recognize(href)
            filename = FileRecognizerWebKit(basepath).recognize(href)
            anchor = AnchorRecognizerWebKit(basepath).recognize(href)

            logger.debug("_identifyUri. url=%s", url)
            logger.debug("_identifyUri. page=%s", page)
            logger.debug("_identifyUri. filename=%s", filename)
            logger.debug("_identifyUri. anchor=%s", anchor)

            return (url, page, filename, anchor)

        return (None, None, None, None)

    def _onLinkClicked(self, href):
        """
        Клик по ссылке
        Возвращает False, если обрабатывать ссылку разрешить компоненту,
        в противном случае - True (если обрабатываем сами)
        href - ссылка
        """
        modifier = self.getKeyCode()
        mouse_button = ID_MOUSE_LEFT
        source_href = href
        href = urllib.parse.unquote(href)
        href = self.decodeIDNA(href)

        logger.debug("_onLinkClicked. href_src=%s", source_href)

        (url, page, filename, anchor) = self._identifyUri(href)

        params = self.getClickParams(
            source_href, mouse_button, modifier, url, page, filename, anchor
        )

        self._application.onLinkClick(self._currentPage, params)
        if params.process:
            return True

        if page is not None and anchor is not None:
            self._application.sharedData[APP_DATA_KEY_ANCHOR] = anchor

        if url is not None:
            self.openUrl(url)
        elif page is not None and modifier == ID_KEY_CTRL:
            self._application.mainWindow.tabsController.openInTab(page, True)
        elif page is not None:
            self._currentPage.root.selectedPage = page
        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile(filename)
            except OSError:
                text = _("Can't execute file '%s'") % filename
                showError(self._application.mainWindow, text)
        elif anchor is not None:
            return False

        return True


class HtmlRenderWebKitGeneral(HtmlRenderWebKitBase):
    """
    HTML render for common using. Engine - WebKit.
    """

    def __init__(self, parent, application):
        super().__init__(parent, application)

    def LoadPage(self, fname):
        self.render.Stop()

        try:
            html = readTextFile(fname)
        except IOError:
            text = _("Can't read file %s") % (fname)
            self.canOpenUrl += 1
            self.SetPage(text, os.path.dirname(fname))

        basepath = os.path.dirname(fname)

        if not basepath.endswith("/"):
            basepath += "/"

        self.SetPage(html, basepath, anchor=None)

    def _identifyUri(self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, filename, anchor)
        """
        uri = self.render.GetCurrentURL()

        logger.debug("_identifyUri. href=%s", href)
        logger.debug("_identifyUri. current URI=%s", uri)

        if uri is not None:
            basepath = self.getBasePath()

            url = URLRecognizer(basepath).recognize(href)
            filename = FileRecognizerWebKit(basepath).recognize(href)
            anchor = AnchorRecognizerWebKit(basepath).recognize(href)

            logger.debug("_identifyUri. url=%s", url)
            logger.debug("_identifyUri. filename=%s", filename)
            logger.debug("_identifyUri. anchor=%s", anchor)

            return (url, filename, anchor)

        return (None, None, None)

    def _onLinkClicked(self, href):
        """
        Клик по ссылке
        Возвращает False, если обрабатывать ссылку разрешить компоненту,
        в противном случае - True (если обрабатываем сами)
        href - ссылка
        """
        source_href = href
        href = urllib.parse.unquote(href)
        href = self.decodeIDNA(href)

        logger.debug("_onLinkClicked. href_src=%s", source_href)

        (url, filename, anchor) = self._identifyUri(href)

        if url is not None:
            self.openUrl(url)
        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile(filename)
            except OSError:
                text = _("Can't execute file '%s'") % filename
                showError(self._application.mainWindow, text)
        elif anchor is not None:
            return False

        return True
