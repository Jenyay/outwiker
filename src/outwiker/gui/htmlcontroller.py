# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os.path

from outwiker.core.application import Application


class UriIdentifier (object):
    """
    Базовый класс для обработчиков ссылок HTML-движков
    """

    __metaclass__ = ABCMeta

    def __init__ (self, currentpage, basepath):
        """
        currentpage - страница, которая в данный момент открыта
        basepath - базовый путь для HTML-рендера
        """
        self._currentPage = currentpage
        self._basepath = self._removeAnchor (basepath, self._currentPage)


    def identify (self, href):
        """
        Определить тип ссылки и вернуть кортеж (url, page, filename, anchor)
        """
        if self._isUrl (href):
            return (href, None, None, None)

        page = self._getPageByProtocol (href)

        if page is not None:
            anchor = self._getAnchorByProtocol (href)
            return (None, page, None, anchor)

        href_clear = self._prepareHref (href)

        page = self._findWikiPage (href_clear)
        filename = self._findFile (href_clear)
        anchor = self._findAnchor (href_clear)

        return (None, page, filename, anchor)


    def _getAnchorByProtocol (self, href):
        """
        Попытаться найти якорь, если используется ссылка вида page://...
        """
        pos = href.rfind ("/#")
        if pos != -1:
            return href[pos + 1:]

        return None


    def _getPageByProtocol (self, href):
        """
        Возвращает страницу, если href - протокол вида page://, и None в противном случае
        """
        protocol = u"page://"
        page = None

        # Если есть якорь, то отсечем его
        anchorpos = href.rfind ("/#")
        if anchorpos != -1:
            href = href[:anchorpos]

        if href.startswith (protocol):
            uid = href[len (protocol):]

            try:
                uid = unicode (uid.decode ("idna"))
            except UnicodeError:
                # Под IE ссылки не преобразуются в кодировку IDNA
                pass

            if uid.endswith ("/"):
                uid = uid[:-1]

            page = Application.pageUidDepot[uid]

        return page


    @abstractmethod
    def _prepareHref (self, href):
        """
        Подготовить ссылку к распознаванию, удалить file:// в начале
        """
        pass


    @abstractmethod
    def _findWikiPage (self, subpath):
        """
        Попытка найти страницу вики
        """
        pass


    def _findFile (self, href):
        """
        Проверить, не указывает ли ссылка на файл
        """
        if os.path.exists (href):
            return href


    @abstractmethod
    def _removeAnchor (self, href, currentpage):
        """
        Удалить якорь из адреса текущей загруженной страницы
        """
        pass


    def _findAnchor (self, href):
        """
        Проверить, а не указывает ли href на якорь
        """
        anchor = None
        if (href.startswith (self._basepath) and
                len (href) > len (self._basepath) and
                href[len (self._basepath)] == "#"):
            anchor = href[len (self._basepath):]

        return anchor


    def _isUrl (self, href):
        """
        Является ли href ссылкой на интернет?
        """
        return (href.lower().startswith ("http:") or
                href.lower().startswith ("https:") or
                href.lower().startswith ("ftp:") or
                href.lower().startswith ("mailto:"))
