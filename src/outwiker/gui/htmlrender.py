# -*- coding: utf-8 -*-

import idna

import wx

import outwiker.core
from outwiker.core.application import Application
from outwiker.core.events import LinkClickParams
from outwiker.gui.defines import ID_KEY_CTRL, ID_KEY_SHIFT


class HtmlRenderBase(wx.Panel):
    """
    Базовый класс для HTML-рендеров
    """

    def __init__(self, parent):
        super().__init__(parent)

        self._render = self._createRender()
        sizer = wx.FlexGridSizer(1)
        sizer.AddGrowableCol(0)
        sizer.AddGrowableRow(0)
        sizer.Add(self._render, 0, wx.EXPAND)
        self.SetSizer(sizer)

    def LoadPage(self, fname):
        """
        Загрузить страницу из файла
        """
        pass

    def SetPage(self, htmltext, basepath):
        """
        Загрузить страницу из строки
        htmltext - текст страницы
        basepath - путь до папки, относительно которой будут искаться
            локальные ресурсы (картинки)
        """
        pass

    def Sleep(self):
        pass

    def Awake(self):
        pass

    def _createRender(self):
        '''
        Must return instance of HTML render engine
        '''
        pass

    @property
    def render(self):
        return self._render

    def openUrl(self, href):
        """
        Открыть ссылку в браузере (или почтовый адрес в почтовике)
        """
        try:
            outwiker.core.system.getOS().startFile(href)
        except OSError:
            text = _(u"Can't execute file '%s'") % (href)
            outwiker.core.commands.showError(Application.mainWindow, text)

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
