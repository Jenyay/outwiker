# -*- coding: utf-8 -*-

import logging
import urllib.request
import urllib.parse
import urllib.error

import wx
import wx.lib.iewin

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
from outwiker.core.defines import APP_DATA_KEY_ANCHOR
from outwiker.gui.htmlrender import HtmlRenderBase
from outwiker.gui.defines import (ID_MOUSE_LEFT,
                                  ID_KEY_CTRL,
                                  ID_KEY_SHIFT)
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.events import HoverLinkParams

from .urirecognizers import (
    URLRecognizer, AnchorRecognizerIE, FileRecognizerIE, PageRecognizerIE)


logger = logging.getLogger('outwiker.gui.htmlrenderie')


class HtmlRenderIEBase(HtmlRenderBase):
    '''
    A base class for HTML render. Engine - Internet Explorer.
    '''
    def __init__(self, parent):
        super().__init__(parent)

        config = GeneralGuiConfig(Application.config)

        self.render = wx.lib.iewin.IEHtmlWindow(self)
        self.render.silent = not config.debug.value

        # Подпишемся на события IE
        self.render.AddEventSink(self)

        self.canOpenUrl = False                # Можно ли открывать ссылки

        self._layout()

        self.Bind(wx.EVT_MENU, self._onCopyFromHtml, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self._onCopyFromHtml, id=wx.ID_CUT)

    def _layout(self):
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.render, 1, wx.EXPAND)

        self.SetSizer(self.box)
        self.Layout()

    def Print(self):
        self.render.Print(True)

    def SetPage(self, htmltext, basepath):
        """
        Загрузить страницу из строки
        htmltext - текст страницы
        basepath - путь, относительно которого отсчитываются относительные
            пути (НЕ ИСПОЛЬЗУЕТСЯ!!!)
        """
        self.canOpenUrl = True
        self.render.LoadString(htmltext)
        self.canOpenUrl = False

    def Sleep(self):
        pass

    def Awake(self):
        pass

    def _onCopyFromHtml(self, event):
        document = self.render.document
        selection = document.selection

        if selection is not None:
            selrange = selection.createRange()
            if selrange is not None:
                outwiker.core.commands.copyTextToClipboard(selrange.text)
                event.Skip()

    def _cleanUpUrl(self, href):
        """
        Почистить ссылку, убрать file:///
        """
        result = self._removeFileProtokol(href)
        result = urllib.parse.unquote(result)
        result = result.replace("/", u"\\")

        return result

    def _removeFileProtokol(self, href):
        """
        Избавиться от протокола file:///, то избавимся от этой надписи
        """
        fileprotocol = u"file:///"
        if href.startswith(fileprotocol):
            return href[len(fileprotocol):]

        return href

    def BeforeNavigate2(self, this, pDisp, URL, Flags,
                        TargetFrameName, PostData, Headers, Cancel):
        href = urllib.parse.unquote(URL[0])
        curr_href = self._cleanUpUrl(self.render.locationurl)

        # Пока другого признака о том, что пытаемся открыть встроенный фрейм,
        # не нашел
        if 'LocationURL' in dir(pDisp) and pDisp.LocationURL == "about:blank":
            Cancel[0] = False
            return

        if self.canOpenUrl or href == curr_href:
            Cancel[0] = False
            self.canOpenUrl = False
        else:
            Cancel[0] = True
            self._onLinkClicked(href)


class HtmlRenderIEForPage(HtmlRenderIEBase):
    """
    HTML render for using as note page render. Engine - Internet Explorer.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self._currentPage = None

        # Номер элемента статусной панели, куда выводится текст
        self._status_item = 0

    @property
    def page(self):
        return self._currentPage

    @page.setter
    def page(self, value):
        self._currentPage = value

    def StatusTextChange(self, status):
        statustext = u""

        if len(status) != 0:
            (url, page, filename, anchor) = self._identifyUri(status)

            if page is not None:
                text = page.display_subpath
                if anchor is not None:
                    text = u"{}/{}".format(text, anchor)

                statustext = text
            elif filename is not None:
                statustext = filename
            elif anchor is not None:
                statustext = anchor
            else:
                statustext = status

        self._setStatusText(status, statustext)

    def _setStatusText(self, link, text):
        """
        Execute onHoverLink event and set status text
        """
        link_decoded = self._decodeIDNA(link)

        params = HoverLinkParams(link=link_decoded, text=text)
        Application.onHoverLink(page=self._currentPage, params=params)

        outwiker.core.commands.setStatusText(params.text, self._status_item)

    def LoadPage(self, fname):
        self.canOpenUrl = True
        path = fname

        if APP_DATA_KEY_ANCHOR in Application.sharedData:
            path += Application.sharedData[APP_DATA_KEY_ANCHOR]
            del Application.sharedData[APP_DATA_KEY_ANCHOR]

        self.render.Navigate(path)

    def NewWindow3(self, this, pDisp, Cancel, dwFlags, currentURL, href):
        Cancel[0] = True

        (url, page, filename, anchor) = self._identifyUri(href)
        if page is not None:
            Application.mainWindow.tabsController.openInTab(page, True)

    def _identifyUri(self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename, anchor)
        """
        location = self.render.locationurl
        basepath = self._cleanUpUrl(location)

        logger.debug('_identifyUri. href={href}'.format(href=href))
        logger.debug(
            '_identifyUri. current location={location}'.format(location=location))
        logger.debug(
            '_identifyUri. basepath={basepath}'.format(basepath=basepath))

        url = URLRecognizer(basepath).recognize(href)
        page = PageRecognizerIE(basepath, Application).recognize(href)
        anchor = AnchorRecognizerIE(basepath).recognize(href)
        filename = FileRecognizerIE(basepath).recognize(href)

        logger.debug('_identifyUri. url={url}'.format(url=url))
        logger.debug('_identifyUri. page={page}'.format(page=page))
        logger.debug(
            '_identifyUri. filename={filename}'.format(filename=filename))
        logger.debug('_identifyUri. anchor={anchor}'.format(anchor=anchor))

        return (url, page, filename, anchor)

    def _onLinkClicked(self, href):
        """
        Клик по ссылке
        """
        (url, page, filename, anchor) = self._identifyUri(href)

        button = ID_MOUSE_LEFT
        modifier = self._getKeyCode()

        params = self._getClickParams(self._decodeIDNA(href),
                                      button,
                                      modifier,
                                      url,
                                      page,
                                      filename,
                                      anchor)

        Application.onLinkClick(self._currentPage, params)
        if params.process:
            return

        if url is not None:
            self.openUrl(url)
        elif page is not None and modifier == ID_KEY_CTRL:
            if anchor is not None:
                Application.sharedData[APP_DATA_KEY_ANCHOR] = anchor
            Application.mainWindow.tabsController.openInTab(page, True)
        elif page is not None:
            if anchor is not None:
                Application.sharedData[APP_DATA_KEY_ANCHOR] = anchor
            self._currentPage.root.selectedPage = page
        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile(filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                outwiker.core.commands.showError(Application.mainWindow, text)
        elif anchor is not None:
            self.LoadPage(href)


class HtmlRenderIEGeneral(HtmlRenderIEBase):
    """
    HTML render for common using. Engine - Internet Explorer.
    """

    def __init__(self, parent):
        super().__init__(parent)

    def LoadPage(self, fname):
        self.canOpenUrl = True
        self.render.Navigate(fname)

    def NewWindow3(self, this, pDisp, Cancel, dwFlags, currentURL, href):
        Cancel[0] = True
        self._onLinkClicked(href)

    def _identifyUri(self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename, anchor)
        """
        location = self.render.locationurl
        basepath = self._cleanUpUrl(location)

        logger.debug('_identifyUri. href={href}'.format(href=href))
        logger.debug(
            '_identifyUri. current location={location}'.format(location=location))
        logger.debug(
            '_identifyUri. basepath={basepath}'.format(basepath=basepath))

        url = URLRecognizer(basepath).recognize(href)
        anchor = AnchorRecognizerIE(basepath).recognize(href)
        filename = FileRecognizerIE(basepath).recognize(href)

        logger.debug('_identifyUri. url={url}'.format(url=url))
        logger.debug(
            '_identifyUri. filename={filename}'.format(filename=filename))
        logger.debug('_identifyUri. anchor={anchor}'.format(anchor=anchor))

        return (url, filename, anchor)

    def _onLinkClicked(self, href):
        """
        Клик по ссылке
        """
        (url, filename, anchor) = self._identifyUri(href)

        if url is not None:
            self.openUrl(url)
        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile(filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                outwiker.core.commands.showError(Application.mainWindow, text)
        elif anchor is not None:
            self.LoadPage(href)
