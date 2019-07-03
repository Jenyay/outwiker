# -*- coding: utf-8 -*-
'''
Classes to recognize href URI for HtmlRenders
'''

from abc import ABCMeta, abstractmethod


class Recognizer(metaclass=ABCMeta):
    @abstractmethod
    def recognize(self, href: str) -> str:
        pass


class URLRecognizer(Recognizer):
    '''
    Recognize internet URL
    '''

    def recognize(self, href: str) -> bool:
        isUrl = (href.lower().startswith("http:") or
                 href.lower().startswith("https:") or
                 href.lower().startswith("ftp:") or
                 href.lower().startswith("mailto:"))

        return href if isUrl else None
