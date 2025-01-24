# -*- coding: utf-8 -*-


from outwiker.core.event import pagetype
from outwiker.core.events import (
    PostprocessingParams,
    PreHtmlImprovingParams,
    PreprocessingParams,
)
from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.style import Style
from outwiker.core.treetools import getPageHtmlPath
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.gui.simplespellcontroller import SimpleSpellController
from outwiker.utilites.textfile import readTextFile, writeTextFile

from .defines import PAGE_TYPE_STRING
from .htmlpage import HtmlPageFactory


class HtmlPageController:
    """GUI controller for HTML page"""

    def __init__(self, application):
        self._application = application
        self._spellController = SimpleSpellController(
            self._application,
            PAGE_TYPE_STRING)

    def initialize(self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded += self.__onPageUpdateNeeded

    def clear(self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded -= self.__onPageUpdateNeeded

        if not self._application.testMode:
            self._spellController.clear()

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == PAGE_TYPE_STRING:
            params.dialog.showAppearancePanel()

    @pagetype(PAGE_TYPE_STRING)
    def __onPageViewCreate(self, page):
        assert page is not None
        if not self._application.testMode:
            self._spellController.initialize(page)

    @pagetype(PAGE_TYPE_STRING)
    def __onPageViewDestroy(self, page):
        assert page is not None
        if not self._application.testMode:
            self._spellController.clear()

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(HtmlPageFactory())

    @pagetype(PAGE_TYPE_STRING)
    def __onPageUpdateNeeded(self, page, params):
        if page.readonly:
            return
        self._updatePage(page)

    def _updatePage(self, page):
        path = getPageHtmlPath(page)
        html = self._makeHtml(page)
        writeTextFile(path, html)

    def _makeHtml(self, page):
        style = Style()
        stylepath = style.getPageStyle(page)

        try:
            tpl = HtmlTemplate(self._application, readTextFile(stylepath))
        except EnvironmentError:
            tpl = HtmlTemplate(self._application, readTextFile(style.getDefaultStyle()))

        content = self._changeContentByEvent(
            page,
            PreprocessingParams(page.content),
            self._application.onPreprocessing)

        if page.autoLineWrap:
            content = self._changeContentByEvent(
                page,
                PreHtmlImprovingParams(content),
                self._application.onPreHtmlImproving)

            config = HtmlRenderConfig(self._application.config)
            improverFactory = HtmlImproverFactory(self._application)
            text = improverFactory[config.HTMLImprover.value].run(content)
        else:
            text = content

        result = tpl.substitute(content=text, title=page.display_title)

        result = self._changeContentByEvent(page,
                                            PostprocessingParams(result),
                                            self._application.onPostprocessing)
        return result

    def _changeContentByEvent(self, page, params, event):
        event(page, params)
        return params.result
