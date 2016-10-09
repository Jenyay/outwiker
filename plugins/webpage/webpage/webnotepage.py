# -*- coding: UTF-8 -*-

"""WebPage page class."""

import os.path
import shutil
from shutil import copytree


from outwiker.core.config import StringOption, BooleanOption
from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.core.factory import PageFactory
from outwiker.core.pagetitletester import WindowsPageTitleTester
from outwiker.core.tree import WikiPage

from .gui.webpageview import WebPageView

# Directory for images, scripts, css etc.
STATIC_DIR_NAME = u'__download'


class WebNotePage(WikiPage):

    """Class of WebPage."""

    def __init__(self, path, title, parent, readonly=False):
        """
        Constructor.

        path - where will be created page.
        title - page title.
        parent - parent page.
        """
        super(WebNotePage, self).__init__(path, title, parent, readonly)

        self.PARAMS_SECTION = u'WebPage'

        self.SOURCE_PARAM = u'source'
        self.SOURCE_DEFAULT = None

        self.LOG_PARAM = u'log'
        self.LOG_DEFAULT = u''

        self.DISABLE_SCRIPTS_PARAM = u'disable_scripts'
        self.DISABLE_SCRIPTS_DEFAULT = True

    @staticmethod
    def getTypeString():
        """Return page string identifier."""
        return u"web"

    def getHtmlPath(self):
        """
        Получить путь до результирующего файла HTML
        """
        return os.path.join(self.path, PAGE_RESULT_HTML)

    @property
    def source(self):
        """Return string of URL of source for the page."""
        return self._getSourceOption().value

    @source.setter
    def source(self, value):
        self._getSourceOption().value = value

    @property
    def log(self):
        return self._getLogOption().value

    @log.setter
    def log(self, value):
        self._getLogOption().value = value

    @property
    def disableScripts(self):
        return self._getDisableScriptOption().value

    @disableScripts.setter
    def disableScripts(self, value):
        self._getDisableScriptOption().value = value

    def _getSourceOption(self):
        return StringOption(self.params,
                            self.PARAMS_SECTION,
                            self.SOURCE_PARAM,
                            self.SOURCE_DEFAULT
                            )

    def _getLogOption(self):
        return StringOption(self.params,
                            self.PARAMS_SECTION,
                            self.LOG_PARAM,
                            self.LOG_DEFAULT
                            )

    def _getDisableScriptOption(self):
        return BooleanOption(self.params,
                             self.PARAMS_SECTION,
                             self.DISABLE_SCRIPTS_PARAM,
                             self.DISABLE_SCRIPTS_DEFAULT
                             )


class WebPageFactory(PageFactory):
    """Factory for WebNotePage creation."""
    def getPageType(self):
        """Return type of the page."""
        return WebNotePage

    @property
    def title(self):
        """Return page title for the page dialog."""
        return _(u"Web Page")

    def getPageView(self, parent):
        """Return page view for the page."""
        return WebPageView(parent)

    def createWebPage(self,
                      parentPage,
                      title,
                      favicon,
                      tags,
                      content,
                      url,
                      tmpStaticDir,
                      logContent=u''):
        """
        Create WebNotePage instance.

        parentPage - parent page for creating page.
        title - offered title for the page. The title may be changed.
        favicon - path to favicon or None.
        tags - tags for page.
        content - HTML code for the page.
        tmpStaticDir - path to downloaded static files.
        logContent - log of downloading.
        """
        title = self._getTitle(parentPage, title)
        page = self.create(parentPage, title, [])
        page.tags = tags
        page.content = content
        page.source = url
        page.log = logContent
        if favicon is not None:
            page.icon = favicon

        staticDir = os.path.join(page.path, STATIC_DIR_NAME)
        try:
            copytree(tmpStaticDir, staticDir)
        except shutil.Error as e:
            raise IOError(e.message)

        return page

    def _getTitle(self, parentPage, title):
        defaultTitle = _(u'Web page')

        if title is None or len(title.strip()) == 0:
            title = defaultTitle
        else:
            title = WindowsPageTitleTester().replaceDangerousSymbols(title,
                                                                     u'_')

        index = 1
        newTitle = title
        while parentPage[newTitle] is not None:
            newTitle = u'{title}({index})'.format(title=title,
                                                  index=index)
            index += 1

        return newTitle
