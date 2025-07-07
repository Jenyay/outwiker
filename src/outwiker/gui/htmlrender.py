# -*- coding: utf-8 -*-

import idna

import wx

import outwiker.core
from outwiker.app.services.messages import showError
from outwiker.core.events import LinkClickParams
from outwiker.core.system import getOS
from outwiker.gui.controls.searchreplacepanel import SearchReplacePanel
from outwiker.gui.defines import ID_KEY_CTRL, ID_KEY_SHIFT


class HtmlRenderBase(wx.Panel):
    """
    Базовый класс для HTML-рендеров
    """

    def __init__(self, parent, application):
        super().__init__(parent)

        self._parent = parent
        self._application = application
        self._render = self._createRender()
        self._searchPanel = SearchReplacePanel(self)
        self._searchPanelController = getOS().getHtmlRenderSearchController(self._searchPanel, self)
        sizer = wx.FlexGridSizer(cols=1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._render, flag=wx.EXPAND | wx.ALL, border=2)
        sizer.Add(self._searchPanel, flag=wx.EXPAND | wx.ALL, border=2)
        self.SetSizer(sizer)

    def LoadPage(self, fname):
        """
        Загрузить страницу из файла
        """

    def SetPage(self, htmltext, basepath):
        """
        Загрузить страницу из строки
        htmltext - текст страницы
        basepath - путь до папки, относительно которой будут искаться
            локальные ресурсы (картинки)
        """

    def Sleep(self):
        pass

    def Awake(self):
        pass

    def _createRender(self):
        '''
        Must return instance of HTML render engine
        '''

    def Find(self, text):
        if self._render:
            return self._render.Find(text)

    @property
    def render(self):
        return self._render

    @property
    def searchPanel(self):
        """
        Возвращает контроллер панели поиска
        """
        return self._searchPanelController

    def openUrl(self, href):
        """
        Открыть ссылку в браузере (или почтовый адрес в почтовике)
        """
        try:
            outwiker.core.system.getOS().startFile(href)
        except OSError:
            text = _("Can't execute file '%s'") % (href)
            showError(self._parent, text)

    def _getLinkProtocol(self, link):
        """
        Return protocol for link or None if link contains not protocol
        """
        if link is None:
            return None

        endProtocol = u"://"
        pos = link.find(endProtocol)
        if pos == -1:
            return None

        return link[:pos + len(endProtocol)]

    def decodeIDNA(self, link):
        """
        Decode link like protocol://xn--80afndtacjikc
        """
        if link is None:
            return None

        protocol = self._getLinkProtocol(link)
        if protocol is not None:
            url = link[len(protocol):]
            try:
                link = u"{}{}".format(
                    protocol,
                    idna.decode(url))
            except UnicodeError:
                # Под IE ссылки не преобразуются в кодировку IDNA
                pass

        return link

    def Reload(self):
        self._render.Reload()


class HTMLRenderForPageMixin:
    def getClickParams(self,
                       href,
                       button,
                       modifier,
                       isurl,
                       ispage,
                       isfilename,
                       isanchor):
        linktype = None

        if isanchor:
            linktype = u"anchor"

        if isurl:
            linktype = u"url"
        elif ispage:
            linktype = u"page"
        elif isfilename:
            linktype = u"filename"

        return LinkClickParams(
            link=href,
            button=button,
            modifier=modifier,
            linktype=linktype,
        )

    def getKeyCode(self):
        modifier = 0

        if wx.GetKeyState(wx.WXK_SHIFT):
            modifier |= ID_KEY_SHIFT

        if wx.GetKeyState(wx.WXK_CONTROL):
            modifier |= ID_KEY_CTRL

        return modifier
