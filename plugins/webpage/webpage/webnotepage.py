# -*- coding: UTF-8 -*-

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage

from .webpageview import WebPageView


class WebNotePage (WikiPage):
    def __init__(self, path, title, parent, readonly = False):
        super (WebNotePage, self).__init__ (path, title, parent, readonly)
        self._source = None


    @staticmethod
    def getTypeString ():
        return u"web"


    @property
    def source (self):
        return self._source


    @source.setter
    def source (self, value):
        self._source = value


class WebPageFactory (PageFactory):
    def getPageType(self):
        return WebNotePage


    @property
    def title (self):
        return _(u"Web Page")


    def getPageView (self, parent):
        return WebPageView (parent)
