# -*- coding: UTF-8 -*-

"""WebPage page class."""

import os.path
from shutil import copytree


from outwiker.core.factory import PageFactory
from outwiker.core.tree import WikiPage
from outwiker.core.config import StringOption
from outwiker.core.pagetitletester import (WindowsPageTitleTester,
                                           PageTitleError,
                                           PageTitleWarning)

from .webpageview import WebPageView

# Directory for images, scripts, css etc.
STATIC_DIR_NAME = u'__download'


class WebNotePage (WikiPage):

    """Class of WebPage."""

    def __init__ (self, path, title, parent, readonly = False):
        """
        Constructor.

        path - where will be created page.
        title - page title.
        parent - parent page.
        """
        super (WebNotePage, self).__init__ (path, title, parent, readonly)

        self.PARAMS_SECTION = u'WebPage'

        self.SOURCE_PARAM = u'source'
        self.SOURCE_DEFAULT = None

        self.LOG_PARAM = u'log'
        self.LOG_DEFAULT = u''


    @staticmethod
    def getTypeString ():
        """Return page string identifier."""
        return u"web"


    @property
    def source (self):
        """Return string of URL of source for the page."""
        return self._getSourceOption().value


    @source.setter
    def source (self, value):
        self._getSourceOption().value = value


    @property
    def log (self):
        return self._getLogOption().value


    @log.setter
    def log (self, value):
        self._getLogOption().value = value


    def _getSourceOption (self):
        return StringOption (self.params,
                             self.PARAMS_SECTION,
                             self.SOURCE_PARAM,
                             self.SOURCE_DEFAULT
                             )


    def _getLogOption (self):
        return StringOption (self.params,
                             self.PARAMS_SECTION,
                             self.LOG_PARAM,
                             self.LOG_DEFAULT
                             )


class WebPageFactory (PageFactory):

    """Factory for WebNotePage creation."""

    def getPageType(self):
        """Return type of the page."""
        return WebNotePage


    @property
    def title (self):
        """Return page title for the page dialog."""
        return _(u"Web Page")


    def getPageView (self, parent):
        """Return page view for the page."""
        return WebPageView (parent)


    def createWebPage (self,
                       parentPage,
                       title,
                       tags,
                       content,
                       url,
                       tmpStaticDir,
                       logContent = u''):
        """
        Create WebNotePage instance.

        parentPage - parent page for creating page.
        title - offered title for the page. The title may be changed.
        tags - tags for page.
        content - HTML code for the page.
        tmpStaticDir - path to downloaded static files.
        logContent - log of downloading.
        """
        title = self._getTitle (parentPage, title)
        page = self.create (parentPage, title, [])
        page.tags = tags
        page.content = content
        page.source = url
        page.log = logContent

        staticDir = os.path.join (page.path, STATIC_DIR_NAME)
        copytree (tmpStaticDir, staticDir)

        return page


    def _getTitle (self, parentPage, title):
        try:
            WindowsPageTitleTester().test (title)
        except (PageTitleError, PageTitleWarning):
            title = _(u'Web page')

        index = 1
        newTitle = title
        while parentPage[newTitle] is not None:
            newTitle = u'{title} ({index})'.format (title=title,
                                                    index=index)
            index += 1

        return newTitle
