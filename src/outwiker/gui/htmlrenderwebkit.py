# -*- coding: utf-8 -*-

import logging
import os
import urllib.request
import urllib.parse
import urllib.error

import wx

import outwiker.core.system
import outwiker.core.commands
from outwiker.core.application import Application
from outwiker.core.defines import APP_DATA_KEY_ANCHOR
from outwiker.gui.htmlcontrollerwebkit import UriIdentifierWebKit
from outwiker.gui.defines import (ID_MOUSE_LEFT,
                                  ID_MOUSE_MIDDLE,
                                  ID_MOUSE_RIGHT,
                                  ID_KEY_CTRL,
                                  ID_KEY_SHIFT)


from .htmlrender import HtmlRender

logger = logging.getLogger('outwiker.gui.htmlrenderwebkit')


class HtmlRenderWebKit(HtmlRender):
    def __init__(self, parent):
        HtmlRender.__init__(self, parent)

        import wx.html2 as webview
        self.ctrl = webview.WebView.New(self)

        sizer = wx.FlexGridSizer(1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self.ctrl, 0, wx.EXPAND)
        self.SetSizer(sizer)

        self.canOpenUrl = False                # Можно ли открывать ссылки
        self._navigate_id = 1

        self.Bind(wx.EVT_MENU, self.__onCopyFromHtml, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.__onCopyFromHtml, id=wx.ID_CUT)
        self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.__onNavigating)

        self._path = None

    def Print(self):
        self.ctrl.Print()

    def LoadPage(self, fname):
        url = u'file://' + urllib.parse.quote(fname.encode("utf8"))
        if APP_DATA_KEY_ANCHOR in Application.sharedData:
            url += Application.sharedData[APP_DATA_KEY_ANCHOR]
            del Application.sharedData[APP_DATA_KEY_ANCHOR]

        if os.path.exists(fname) and os.path.isfile(fname):
            self.canOpenUrl = True
            self.ctrl.LoadURL(url)
        else:
            text = _(u"Can't read file %s") % (fname)
            self.SetPage(text, os.path.dirname(fname))

    def SetPage(self, htmltext, basepath):
        self._path = "file://" + urllib.parse.quote(basepath) + "/"

        self.canOpenUrl = True
        self.ctrl.SetPage(htmltext, self._path)

    def __onCopyFromHtml(self, event):
        self.ctrl.Copy()
        event.Skip()

    def __identifyUri(self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename, anchor)
        """
        uri = self.ctrl.GetCurrentURL()

        if uri is not None:
            basepath = urllib.parse.unquote(uri)
            identifier = UriIdentifierWebKit(self._currentPage, basepath)

            return identifier.identify(href)

        return (None, None, None, None)

    def __onNavigating(self, event):
        nav_id = self._navigate_id
        self._navigate_id += 1

        # from pudb import set_trace; set_trace()
        logger.debug('__onNavigating ({nav_id}) begin'.format(nav_id=nav_id))

        # Проверка на то, что мы не пытаемся открыть вложенный фрейм
        frame = event.GetTarget()
        if frame:
            logger.debug('__onNavigating ({nav_id}) frame={frame}'.format(nav_id=nav_id, frame=frame))
            logger.debug('__onNavigating ({nav_id}) end'.format(nav_id=nav_id))
            return

        href = event.GetURL()
        curr_href = self.ctrl.GetCurrentURL()
        logger.debug('__onNavigating ({nav_id}). href={href}; curr_href={curr_href}; canOpenUrl={canOpenUrl}'.format(
            nav_id=nav_id, href=href, curr_href=curr_href, canOpenUrl=self.canOpenUrl))

        if href == 'about:blank':
            logger.debug('__onNavigating. Skip about:blank')
            event.Veto()
            return

        if not self.canOpenUrl and href != curr_href:
            button = 1
            modifier = 0
            manual_process = self.__onLinkClicked(href, button, modifier)
            if manual_process:
                logger.debug('__onNavigating ({nav_id}). Veto'.format(nav_id=nav_id))
                event.Veto()
            else:
                self.canOpenUrl = True

        else:
            self.canOpenUrl = False

        logger.debug('__onNavigating ({nav_id}) end'.format(nav_id=nav_id))

    def __gtk2OutWikerKeyCode(self, gtk_key_modifier):
        """
        Convert from GTK key modifier to const from gui.defines
        """
        # Consts in GTK
        gtk_shift_key = 1
        gtk_ctrl_key = 4

        modifier = 0
        if gtk_key_modifier & gtk_shift_key:
            modifier |= ID_KEY_SHIFT

        if gtk_key_modifier & gtk_ctrl_key:
            modifier |= ID_KEY_CTRL

        return modifier

    def __gtk2OutWikerMouseButtonCode(self, gtk_mouse_button):
        """
        Convert from GTK mouse key modifier to const from gui.defines
        """
        # Consts in GTK
        gtk_left_button = 1
        gtk_middle_button = 2
        gtk_right_button = 3

        mouse_button = -1

        if gtk_mouse_button == gtk_left_button:
            mouse_button = ID_MOUSE_LEFT
        elif gtk_mouse_button == gtk_middle_button:
            mouse_button = ID_MOUSE_MIDDLE
        elif gtk_middle_button == gtk_right_button:
            mouse_button = ID_MOUSE_RIGHT

        return mouse_button

    def __onLinkClicked(self, href, gtk_mouse_button, gtk_key_modifier):
        """
        Клик по ссылке
        Возвращает False, если обрабатывать ссылку разрешить компоненту,
        в противном случае - True (если обрабатываем сами)
        href - ссылка
        gtk_mouse_button - кнопка мыши, с помощью которой кликнули по ссылке
        (1 - левая, 2 - средняя, 3 - правая, -1 - не известно)
        gtk_key_modifier - зажатые клавиши (1 - Shift, 4 - Ctrl)
        """
        source_href = href
        href = urllib.parse.unquote(href)
        href = self._decodeIDNA(href)

        logger.debug('__onLinkClicked. href_src={source_href}; href_process={href}'.format(
            source_href=source_href, href=href)
        )

        (url, page, filename, anchor) = self.__identifyUri(href)
        logger.debug('__onLinkClicked. url={url}, page={page}, filename={filename}, anchor={anchor}'.format(
            url=url, page=page, filename=filename, anchor=anchor))

        modifier = self.__gtk2OutWikerKeyCode(gtk_key_modifier)
        mouse_button = self.__gtk2OutWikerMouseButtonCode(gtk_mouse_button)

        params = self._getClickParams(source_href,
                                      mouse_button,
                                      modifier,
                                      url,
                                      page,
                                      filename,
                                      anchor)

        Application.onLinkClick(self._currentPage, params)
        if params.process:
            return True

        if url is not None:
            self.openUrl(url)
        elif (page is not None and
              (mouse_button == ID_MOUSE_MIDDLE or modifier == ID_KEY_CTRL)):
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
            return False

        return True
