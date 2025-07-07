# -*- coding: utf-8 -*-

from abc import abstractmethod
import json
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
    URLRecognizer, AnchorRecognizerEdge, FileRecognizerEdge,
    PageRecognizerEdge)

logger = logging.getLogger('outwiker.gui.htmlrenderedge')


class HtmlRenderEdgeBase(HtmlRenderBase):
    '''
    A base class for HTML render. Engine - Edge.
    '''

    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._basepath = None
        self.canOpenUrl = set()
        self._navigate_id = 1
        self._history_href = []

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
        render = wx.html2.WebView.New(self, backend=wx.html2.WebViewBackendEdge)
        render.AddScriptMessageHandler('wx_msg')
        render.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self._handleMessage)

        js_code = """
        document 
            .addEventListener("keydown", 
                function (event) { 
                    let key = event.key;
                    if (key.startsWith("Arrow")) {
                        key = key.replace("Arrow", "");
                    }

                    if (key == "Control" || key == "Shift" || key == "Alt") {
                        return;
                    }

                    let eventBody = { "key": key, "ctrl": false, "shift": false, "alt": false };

                    if (event.shiftKey) {
                        eventBody.shift = true;
                    }
                    if (event.altKey) {
                        eventBody.alt = true;
                    }
                    if (event.ctrlKey) {
                        eventBody.ctrl = true;
                    }

                   window.wx_msg.postMessage(JSON.stringify(eventBody));
                }); 
"""
        render.AddUserScript(js_code, wx.html2.WEBVIEW_INJECT_AT_DOCUMENT_START)

        return render

    def _handleMessage(self, event):
        obj = json.loads(event.GetString())
        print(obj)
        # key_event = wx.KeyEvent()
        # key_event.SetUnicodeKey(ord(obj["key"]))
        # key_event.SetAltDown(obj["alt"])
        # key_event.SetShiftDown(obj["shift"])
        # key_event.SetControlDown(obj["ctrl"])
        # key_event.ResumePropagation(50)
        # key_event.SetEventType(wx.wxEVT_KEY_DOWN)

        # wx.PostEvent(self.GetParent(), key_event)

    def getBasePath(self) -> str:
        return self._basepath

    def Print(self):
        self.render.Print()

    def SetPage(self, htmltext, basepath, anchor=None):
        logger.debug('SetPage({nav_id}). basepath={basepath}'.format(nav_id=self._navigate_id, basepath=basepath))
        self._basepath = basepath
        path = basepath
        if anchor:
            path += anchor

        self.canOpenUrl.add(path)
        self.render.SetPage(htmltext, path)

    def Sleep(self):
        import wx.html2 as webview
        self.render.Unbind(webview.EVT_WEBVIEW_NAVIGATING,
                           handler=self._onNavigating)
        self.Unbind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_COPY)
        self.Unbind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_CUT)

    def Awake(self):
        self.canOpenUrl = set()
        self._navigate_id = 1

        import wx.html2 as webview
        self.Bind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, handler=self._onCopyFromHtml, id=wx.ID_CUT)
        self.render.Bind(webview.EVT_WEBVIEW_NAVIGATING,
                         handler=self._onNavigating)

    def _remove_file_prefix(self, path: str) -> str:
        prefix = 'file:///'
        if path.startswith(prefix):
            path = path[len(prefix):]

        return path

    def _decode_href(self, href: str) -> str:
        return self._remove_file_prefix(urllib.parse.unquote(href))

    def _onClose(self, event):
        import wx.html2 as webview
        self.render.Unbind(webview.EVT_WEBVIEW_NAVIGATING,
                           handler=self._onNavigating)
        self.render.Stop()
        event.Skip()

    def _onCopyFromHtml(self, event):
        self.render.Copy()
        event.Skip()

    def _onNavigating(self, event):
        nav_id = self._navigate_id
        self._navigate_id += 1

        logger.debug('_onNavigating ({nav_id}) begin. canOpenUrl = {can_open_url}'.format(
            nav_id=nav_id,
            can_open_url=self.canOpenUrl))

        # Проверка на то, что мы не пытаемся открыть вложенный фрейм
        frame = event.GetTarget()
        if frame:
            logger.debug('_onNavigating ({nav_id}) frame={frame}'.format(
                nav_id=nav_id, frame=frame))
            logger.debug('_onNavigating ({nav_id}) end'.format(nav_id=nav_id))
            return

        href = event.GetURL()
        href_decoded = self._decode_href(href)
        curr_href = self.render.GetCurrentURL()
        logger.debug('_onNavigating ({nav_id}). href={href}; curr_href={curr_href}; href_decoded={href_decoded}; canOpenUrl={canOpenUrl}'.format(
            nav_id=nav_id, href=href, curr_href=curr_href, href_decoded=href_decoded, canOpenUrl=self.canOpenUrl))

        # Open empty page
        if href == 'about:blank' or href == '':
            logger.debug('_onNavigating. Skip about:blank')
            event.Veto()
            return

        # Link clicked
        if href_decoded not in self.canOpenUrl:
            # Disable the Back button
            # if len(self._history_href) >= 2 and href_decoded == self._history_href[-2]:
            #     logger.debug('_onNavigating ({nav_id}). Cancel return back.'.format(nav_id=nav_id))
            #     event.Veto()
            #     return

            logger.debug(
                '_onNavigating ({nav_id}). Link clicked.'.format(nav_id=nav_id))
            processed = self._onLinkClicked(href_decoded)
            if processed:
                event.Veto()
                logger.debug(
                    '_onNavigating ({nav_id}) end. Veto'.format(nav_id=nav_id))
            else:
                logger.debug('_onNavigating ({nav_id}) end. Allow href processing. href={href}'.format(
                    nav_id=nav_id, href=href))
        else:
            self.canOpenUrl.remove(href_decoded)
            logger.debug('_onNavigating ({nav_id}) end. canOpenUrl={canOpenUrl}'.format(
                nav_id=nav_id, canOpenUrl=self.canOpenUrl))


class HtmlRenderEdgeForPage(HtmlRenderEdgeBase, HTMLRenderForPageMixin):
    '''
    HTML render for using as note page render. Engine - Edge.
    '''

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
        fname = fname.replace('\\', '/')
        logger.debug('LoadPage({nav_id}). fname={fname}'.format(nav_id=self._navigate_id, fname=fname))
        self.render.Stop()
        self._basepath = fname

        # Add anchor for references
        anchor = None
        if APP_DATA_KEY_ANCHOR in self._application.sharedData:
            anchor = self._application.sharedData[APP_DATA_KEY_ANCHOR]
            del self._application.sharedData[APP_DATA_KEY_ANCHOR]

        self.canOpenUrl.add(fname)
        if anchor is not None:
            fname += anchor

        self._history_href.append(fname)
        if len(self._history_href) > 2:
            del self._history_href[0]

        self.render.LoadURL(fname)

    def _identifyUri(self, href):
        """
        Recognize href type and return tuple (url, page, filename, anchor).
        Every tuple item may be None.
        """
        uri = self.render.GetCurrentURL()

        logger.debug('_identifyUri. href={href}'.format(href=href))
        logger.debug('_identifyUri. current URI={uri}'.format(uri=uri))

        if uri is not None:
            basepath = self.getBasePath()

            url = URLRecognizer(basepath).recognize(href)
            page = PageRecognizerEdge(basepath, self._application).recognize(href)
            filename = FileRecognizerEdge(basepath).recognize(href)
            anchor = AnchorRecognizerEdge(basepath).recognize(href)

            logger.debug('_identifyUri. url={url}'.format(url=url))
            logger.debug('_identifyUri. page={page}'.format(page=page))
            logger.debug(
                '_identifyUri. filename={filename}'.format(filename=filename))
            logger.debug(
                '_identifyUri. anchor={anchor}'.format(anchor=anchor))

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

        logger.debug('_onLinkClicked. href_src={source_href}'.format(
            source_href=source_href)
        )

        (url, page, filename, anchor) = self._identifyUri(href)

        params = self.getClickParams(source_href,
                                     mouse_button,
                                     modifier,
                                     url,
                                     page,
                                     filename,
                                     anchor)

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


class HtmlRenderEdgeGeneral(HtmlRenderEdgeBase):
    '''
    HTML render for common using. Engine - Edge.
    '''

    def __init__(self, parent, application):
        super().__init__(parent, application)

    def LoadPage(self, fname):
        logger.debug('LoadPage({nav_id}). fname={fname}'.format(nav_id=self._navigate_id, fname=fname))
        self.render.Stop()

        try:
            html = readTextFile(fname)
        except IOError:
            text = _(u"Can't read file %s") % (fname)
            self.canOpenUrl.add(fname)
            self.SetPage(text, os.path.dirname(fname))

        basepath = os.path.dirname(fname)

        if not basepath.endswith('/'):
            basepath += '/'

        self.SetPage(html, basepath, anchor=None)

    def _identifyUri(self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, filename, anchor)
        """
        uri = self.render.GetCurrentURL()

        logger.debug('_identifyUri. href={href}'.format(href=href))
        logger.debug('_identifyUri. current URI={uri}'.format(uri=uri))

        if uri is not None:
            basepath = self.getBasePath()

            url = URLRecognizer(basepath).recognize(href)
            filename = FileRecognizerEdge(basepath).recognize(href)
            anchor = AnchorRecognizerEdge(basepath).recognize(href)

            logger.debug('_identifyUri. url={url}'.format(url=url))
            logger.debug(
                '_identifyUri. filename={filename}'.format(filename=filename))
            logger.debug(
                '_identifyUri. anchor={anchor}'.format(anchor=anchor))

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

        logger.debug('_onLinkClicked. href_src={source_href}'.format(
            source_href=source_href)
        )

        (url, filename, anchor) = self._identifyUri(href)

        if url is not None:
            self.openUrl(url)
        elif filename is not None:
            try:
                outwiker.core.system.getOS().startFile(filename)
            except OSError:
                text = _(u"Can't execute file '%s'") % filename
                showError(self._application.mainWindow, text)
        elif anchor is not None:
            return False

        return True
