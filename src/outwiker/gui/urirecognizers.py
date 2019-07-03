# -*- coding: utf-8 -*-
'''
Classes to recognize href URI for HtmlRenders
'''

from abc import ABCMeta, abstractmethod
from typing import Union


def _removeFileProtokol(href):
    """
    Remove 'file://' protocol
    """
    fileprotocol = u"file://"
    if href.startswith(fileprotocol):
        return href[len(fileprotocol):]

    return href


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


class Recognizer(metaclass=ABCMeta):
    def recognize(self, href: Union[str, None]) -> Union[str, None]:
        if href is None:
            return None

        return self._recognize(href)

    @abstractmethod
    def _recognize(self, href: str) -> str:
        pass


class URLRecognizer(Recognizer):
    '''
    Recognize internet URL
    '''

    def _recognize(self, href: str) -> str:
        isUrl = (href.lower().startswith("http:") or
                 href.lower().startswith("https:") or
                 href.lower().startswith("ftp:") or
                 href.lower().startswith("mailto:"))

        return href if isUrl else None


class AnchorRecognizerIE(Recognizer):
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


class AnchorRecognizerWebKit(Recognizer):
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

        # WebKit appends 'file://' string to end of URI without protocol.
        href = _removeFileProtokol(href)
        return _recognizeAnchor(href, basepath)
