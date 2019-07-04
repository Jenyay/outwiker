# -*- coding: utf-8 -*-
'''
Classes to recognize href URI for HtmlRenders
'''

from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Union


def _recognizeAnchor(href: str, basepath: str) -> Union[str, None]:
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


def _recognizeFile(href: str, basepath: str) -> Union[str, None]:
    href_path_abs = Path(href)
    if href_path_abs.exists():
        return str(href_path_abs.resolve())

    href_path_relative = Path(basepath, href)
    if href_path_relative.exists():
        return str(href_path_relative.resolve())


class Recognizer(metaclass=ABCMeta):
    def recognize(self, href: Union[str, None]) -> Union[str, None]:
        if href is None:
            return None

        href = self._prepareHref(href)
        return self._recognize(href)

    @abstractmethod
    def _prepareHref(self, href: str) -> str:
        pass

    @abstractmethod
    def _recognize(self, href: str) -> str:
        pass


class URLRecognizer(Recognizer):
    '''
    Recognize internet URL
    '''

    def _prepareHref(self, href: str) -> str:
        return href

    def _recognize(self, href: str) -> str:
        isUrl = (href.lower().startswith("http:") or
                 href.lower().startswith("https:") or
                 href.lower().startswith("ftp:") or
                 href.lower().startswith("mailto:"))

        return href if isUrl else None


class RecognizerIE(Recognizer, metaclass=ABCMeta):
    '''
    Base class for Recognizers for Internet Explorer
    '''

    def _prepareHref(self, href: str) -> str:
        return href


class RecognizerWebKit(Recognizer, metaclass=ABCMeta):
    '''
    Base class for Recognizers for WebKit
    '''

    def _prepareHref(self, href: str) -> str:
        # WebKit appends 'file://' string to end of URI without protocol.
        href = self._removeFileProtokol(href)
        return href

    def _removeFileProtokol(self, href):
        """
        Remove 'file://' protocol
        """
        fileprotocol = u"file://"
        if href.startswith(fileprotocol):
            return href[len(fileprotocol):]

        return href


class AnchorRecognizerIE(RecognizerIE):
    '''
    Recognize an anchor in href.
    For Internet Explorer engine.
    '''

    def __init__(self, basepath: str):
        '''
        basepath - path to directory with current HTML file for HTML render.
        '''
        self._basepath = basepath

    def _recognize(self, href: str) -> str:
        basepath = self._basepath
        return _recognizeAnchor(href, basepath)


class AnchorRecognizerWebKit(RecognizerWebKit):
    '''
    Recognize an anchor in href.
    For WebKit engine.
    '''

    def __init__(self, basepath: str):
        '''
        basepath - path to directory with current HTML file for HTML render.
        '''
        self._basepath = basepath

    def _recognize(self, href: str) -> Union[str, None]:
        basepath = self._basepath
        if not basepath.endswith('/'):
            basepath += '/'

        return _recognizeAnchor(href, basepath)


class FileRecognizerIE(RecognizerIE):
    def __init__(self, basepath: str):
        '''
        basepath - path to directory with current HTML file for HTML render.
        '''
        self._basepath = basepath

    def _recognize(self, href: str) -> Union[str, None]:
        return _recognizeFile(href, self._basepath)


class FileRecognizerWebKit(RecognizerWebKit):
    def __init__(self, basepath: str):
        '''
        basepath - path to directory with current HTML file for HTML render.
        '''
        self._basepath = basepath

    def _recognize(self, href: str) -> Union[str, None]:
        return _recognizeFile(href, self._basepath)

