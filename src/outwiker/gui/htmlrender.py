# -*- coding: UTF-8 -*-

from abc import abstractmethod
from abc import ABCMeta

import wx

import outwiker.core
from outwiker.core.application import Application


class HtmlRender (wx.Panel):
    """
    Базовый класс для HTML-рендеров
    """
    __metaclass__ = ABCMeta

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Номер элемента статусной панели, куда выводится текст
        self._status_item = 0
        self._currentPage = None


    @abstractmethod
    def LoadPage (self, fname):
        """
        Загрузить страницу из файла
        """
        pass


    def SetPage (self, htmltext, basepath):
        """
        Загрузить страницу из строки
        htmltext - текст страницы
        basepath - путь до папки, относительно которой ищутся локальные ресурсы (картинки)
        """
        pass


    @property
    def page (self):
        return self._currentPage


    @page.setter
    def page (self, value):
        self._currentPage = value


    def openUrl (self, href):
        """
        Открыть ссылку в браузере (или почтовый адрес в почтовике)
        """
        try:
            outwiker.core.system.getOS().startFile (href)
        except OSError:
            text = _(u"Can't execute file '%s'") % (href)
            outwiker.core.commands.MessageBox (text, "Error", wx.ICON_ERROR | wx.OK)


    def _getLinkProtocol (self, link):
        """
        Return protocol for link or None if link contains not protocol
        """
        if link is None:
            return None

        endProtocol = u"://"
        pos = link.find (endProtocol)
        if pos == -1:
            return None

        return link[:pos + len (endProtocol)]


    def _decodeIDNA (self, link):
        """
        Decode link like protocol://xn--80afndtacjikc
        """
        if link is None:
            return None

        protocol = self._getLinkProtocol (link)
        if protocol is not None:
            url = link[len (protocol):]
            try:
                link = u"{}{}".format (
                    protocol,
                    unicode (url.decode ("idna")))
            except UnicodeError:
                # Под IE ссылки не преобразуются в кодировку IDNA
                pass

        return link


    def _getClickParams (self,
                         href,
                         button,
                         modifier,
                         isurl,
                         ispage,
                         isfilename,
                         isanchor):
        params = {
            u"link": href,
            u"button": button,
            u"modifier": modifier,
            u"process": False,
            u"linktype": None,
        }

        if isanchor:
            params["linktype"] = u"anchor"

        if isurl:
            params["linktype"] = u"url"
        elif ispage:
            params["linktype"] = u"page"
        elif isfilename:
            params["linktype"] = u"filename"

        return params


    def setStatusText (self, link, text):
        """
        Execute onHoverLink event and set status text
        """
        link_decoded = self._decodeIDNA (link)
        page = self._currentPage
        result = [text]
        Application.onHoverLink (page=page,
                                 link=link_decoded,
                                 title=result)

        outwiker.core.commands.setStatusText (result[0], self._status_item)
