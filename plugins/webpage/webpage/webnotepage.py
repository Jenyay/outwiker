# -*- coding: utf-8 -*-

"""WebPage page class"""

import logging
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
STATIC_DIR_NAME = '__download'

logger = logging.getLogger('webpage')


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

        self.PARAMS_SECTION = 'WebPage'

        self.SOURCE_PARAM = 'source'
        self.SOURCE_DEFAULT = None

        self.LOG_PARAM = 'log'
        self.LOG_DEFAULT = ''

        self.DISABLE_SCRIPTS_PARAM = 'disable_scripts'
        self.DISABLE_SCRIPTS_DEFAULT = True

    @staticmethod
    def getTypeString():
        """Return page string identifier."""
        return "web"

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

    def getPageView(self, parent, application):
        """Return page view for the page."""
        return WebPageView(parent, application)

    def createWebPage(self,
                      parentPage,
                      title,
                      favicon,
                      tags,
                      content,
                      url,
                      tmpStaticDir,
                      logContent=''):
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
        title_correct = self._getTitle(parentPage, title)
        page = self.create(parentPage, title_correct, [])
        page.tags = tags
        page.content = content
        page.source = url
        page.log = logContent
        if favicon is not None:
            page.icon = favicon

        if title != title_correct:
            page.alias = title

        staticDir = os.path.join(page.path, STATIC_DIR_NAME)
        try:
            copytree(tmpStaticDir, staticDir)
        except shutil.Error as e:
            logger.error(str(e))

        return page

    def _getTitle(self, parentPage, title):
        defaultTitle = _('Web page')

        if title is None or len(title.strip()) == 0:
            title = defaultTitle
        else:
            title = WindowsPageTitleTester().replaceDangerousSymbols(title, '_')

        index = 1
        newTitle = title
        while parentPage[newTitle] is not None:
            newTitle = '{title}({index})'.format(title=title,
                                                  index=index)
            index += 1

        return newTitle
