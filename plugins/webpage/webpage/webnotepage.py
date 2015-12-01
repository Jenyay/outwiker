# -*- coding: UTF-8 -*-

from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage

from .webpageview import WebPageView


class WebNotePage (WikiPage):
    def __init__(self, path, title, parent, readonly = False):
        super (WebNotePage, self).__init__ (path, title, parent, readonly)


    @staticmethod
    def getTypeString ():
        return u"web"


class WebPageFactory (PageFactory):
    def getPageType(self):
        return WebNotePage


    @property
    def title (self):
        return _(u"Web Page")


    def getPageView (self, parent):
        return WebPageView (parent)
