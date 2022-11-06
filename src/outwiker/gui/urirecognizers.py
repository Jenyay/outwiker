# -*- coding: utf-8 -*-
'''
Classes to recognize href URI for HtmlRenders
'''

from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Optional
from urllib.parse import unquote
import os

import idna


class Recognizer(metaclass=ABCMeta):
    '''
    Base class for all recognizers
    '''

    def __init__(self, basepath: str):
        '''
        basepath - path to directory with current HTML file for HTML render.
        '''
        self._basepath = basepath.replace('\\', '/')
        self._basepath = self._removeAnchor(self._basepath)

    def _removeAnchor(self, basepath: str) -> str:
        last_slash_pos = basepath.rfind('/')
        if last_slash_pos == -1:
            return basepath

        sharp_pos = basepath.rfind('#')
        if sharp_pos > last_slash_pos:
            return basepath[:sharp_pos]

        return basepath

    def recognize(self, href: Optional[str]) -> Optional[str]:
        if href is None:
            return None

        href = self._prepareHref(href)
        return self._recognize(href)

    def _prepareHref(self, href: str) -> str:
        # WebKit appends 'file://' string to end of URI without protocol.
        href = self._removeFileProtokol(href)
        href = href.replace('\\', '/')
        return href

    def _removeFileProtokol(self, href):
        """
        Remove 'file://' protocol
        """
        fileprotocol = u"file://"
        if href.startswith(fileprotocol):
            return href[len(fileprotocol):]

        return href

    @abstractmethod
    def _recognize(self, href: str) -> Optional[str]:
        pass


# URL recognizer
class URLRecognizer(Recognizer):
    '''
    Recognize internet URL
    '''

    def _prepareHref(self, href: str) -> str:
        return href

    def _recognize(self, href: str) -> Optional[str]:
        isUrl = (href.lower().startswith("http:") or
                 href.lower().startswith("https:") or
                 href.lower().startswith("ftp:") or
                 href.lower().startswith("mailto:"))

        return href if isUrl else None


# Anchor recognizers

class AnchorRecognizerBase(Recognizer, metaclass=ABCMeta):
    def _recognizeAnchor(self, href: str, basepath: str) -> Optional[str]:
        anchor = None
        if (href.startswith(basepath) and
                len(href) > len(basepath) and
                href[len(basepath)] == "#"):
            anchor = href[len(basepath):]
        else:
            pos = href.rfind("/#")
            if pos != -1:
                anchor = href[pos + 1:]

        return anchor


class AnchorRecognizerIE(AnchorRecognizerBase):
    '''
    Recognize an anchor in href.
    For Internet Explorer engine.
    '''

    def _recognize(self, href: str) -> Optional[str]:
        if href.startswith('/'):
            href = href[1:]

        return self._recognizeAnchor(href, self._basepath)


class AnchorRecognizerEdge(AnchorRecognizerIE):
    '''
    Recognize an anchor in href.
    For Edge engine.
    '''
    pass



class AnchorRecognizerWebKit(AnchorRecognizerBase):
    '''
    Recognize an anchor in href.
    For WebKit engine.
    '''

    def _recognize(self, href: str) -> Optional[str]:
        basepath = self._basepath
        if not basepath.endswith('/'):
            basepath += '/'

        return self._recognizeAnchor(href, basepath)


# File recognizers

class FileRecognizerBase(Recognizer):
    def _recognize(self, href: str) -> Optional[str]:
        return self._recognizeFile(href, self._basepath)

    def _recognizeFile(self, href: str, basepath_str: str) -> Optional[str]:
        try:
            href_path_abs = Path(href)
            # Check absolute path
            if href_path_abs.exists():
                return str(href_path_abs.resolve())

            # Check relative path
            basepath = Path(basepath_str)
            if basepath.is_file():
                basepath = basepath.parent

            href_path_relative = Path(basepath, href)
            if href_path_relative.exists():
                return str(href_path_relative.resolve())
        except OSError:
            return None

        return None


class FileRecognizerIE(FileRecognizerBase):
    pass


class FileRecognizerEdge(FileRecognizerBase):
    pass


class FileRecognizerWebKit(FileRecognizerBase):
    pass


# Page recognizers

class PageRecognizerBase(Recognizer, metaclass=ABCMeta):
    def __init__(self, basepath: str, application):
        super().__init__(basepath)
        self._application = application

    @abstractmethod
    def _findPageByPath(self, href: str):
        pass

    def _findPageByProtocol(self, href: str):
        """
        Find page by href like page://..
        """
        protocol = u"page://"
        page = None

        # Если есть якорь, то отсечем его
        anchorpos = href.rfind("/#")
        if anchorpos != -1:
            href = href[:anchorpos]

        if href.startswith(protocol):
            uid = href[len(protocol):]

            try:
                uid = idna.decode(uid)
            except UnicodeError:
                # With Internet Explorer will be thrown UnicodeError exception
                pass

            if uid.endswith("/"):
                uid = uid[:-1]

            page = (self._application.pageUidDepot[uid] or
                    self._application.selectedPage[uid] or
                    self._application.wikiroot[uid])

        return page

    def _recognize(self, href: str) -> str:
        page = (self._findPageByProtocol(href) or
                self._findPageByPath(href))
        return page


class PageRecognizerWebKit(PageRecognizerBase):
    def _findPageByPath(self, href: str):
        currentPage = self._application.selectedPage

        if currentPage is None:
            return None

        if os.path.abspath(currentPage.path) == os.path.abspath(href):
            return currentPage

        if href.startswith(self._basepath):
            href = href[len(self._basepath):]
            if href.startswith('/'):
                href = href[1:]

        if len(href) == 0:
            return None

        newSelectedPage = None

        if href[0] == "/":
            if href.startswith(currentPage.root.path):
                href = href[len(currentPage.root.path):]

            if len(href) > 1 and href.endswith("/"):
                href = href[:-1]

        if href[0] == "/":
            # Поиск страниц осуществляем только с корня
            newSelectedPage = currentPage.root[href[1:]]
        else:
            # Сначала попробуем найти вложенные страницы с таким href
            newSelectedPage = currentPage[href]

            if newSelectedPage is None:
                # Если страница не найдена, попробуем поискать, начиная с корня
                newSelectedPage = currentPage.root[href]

        return newSelectedPage


class PageRecognizerIE(PageRecognizerBase):
    def _findPageByPath(self, href: str):
        currentPage = self._application.selectedPage

        if currentPage is None:
            return None

        newSelectedPage = None

        # Проверим, вдруг IE посчитал, что это не ссылка, а якорь
        # В этом случае ссылка будет выглядеть, как x:\...\{contentfile}#link
        anchor = self._findAnchor(href)
        if anchor is not None and currentPage[anchor.replace("\\", "/")] is not None:
            return currentPage[anchor.replace("\\", "/")]

        if href.startswith('/'):
            href = href[1:]

        href = unquote(href)

        if len(href) > 1 and href[1] == ":":
            if href.startswith(currentPage.path.replace("\\", "/")):
                href = href[len(currentPage.path) + 1:]
            elif href.startswith(currentPage.root.path.replace("\\", "/")):
                href = href[len(currentPage.root.path):]
            else:
                href = href[2:]

            if len(href) > 1 and href.endswith("/"):
                href = href[:-1]

        if href.startswith("about:"):
            href = self._removeAboutBlank(href).replace("\\", "/")

        if len(href) > 0 and href[0] == "/":
            # Поиск страниц осуществляем только с корня
            newSelectedPage = currentPage.root[href[1:]]
        elif len(href) > 0:
            # Сначала попробуем найти вложенные страницы с таким href
            newSelectedPage = currentPage[href]

            if newSelectedPage is None:
                # Если страница не найдена, попробуем поискать, начиная с корня
                newSelectedPage = currentPage.root[href]

        return newSelectedPage

    def _removeAboutBlank(self, href):
        """
        Удалить about: и about:blank из начала адреса
        """
        about_full = u"about:blank"
        about_short = u"about:"

        result = href
        if result.startswith(about_full):
            result = result[len(about_full):]

        elif result.startswith(about_short):
            result = result[len(about_short):]

        return result

    def _findAnchor(self, href):
        """
        Проверить, а не указывает ли href на якорь
        """
        anchor = None
        if (href.startswith(self._basepath) and
                len(href) > len(self._basepath) and
                href[len(self._basepath)] == "#"):
            anchor = href[len(self._basepath):]

        return anchor


class PageRecognizerEdge(PageRecognizerIE):
    pass
