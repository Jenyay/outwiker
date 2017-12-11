# -*- coding: UTF-8 -*-

from outwiker.gui.pagedialogpanels.appearancepanel import(
    AppearancePanel,
    AppearanceController)

from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.event import pagetype
from outwiker.core.events import (PreprocessingParams,
                                  PreHtmlImprovingParams,
                                  PostprocessingParams,
                                  )
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.style import Style
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.gui.simplespellcontroller import SimpleSpellController
from outwiker.utilites.textfile import writeTextFile, readTextFile

from .htmlpage import HtmlWikiPage, HtmlPageFactory


class HtmlPageController(object):
    """GUI controller for HTML page"""

    def __init__(self, application):
        self._application = application
        self._appearancePanel = None
        self._appearanceController = None
        self._spellController = SimpleSpellController(
            self._application,
            HtmlWikiPage.getTypeString())

    def initialize(self):
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy += self.__onPageDialogDestroy
        self._application.onPageViewCreate += self.__onPageViewCreate
        self._application.onPageViewDestroy += self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded += self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded += self.__onPageUpdateNeeded

    def clear(self):
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged
        self._application.onPageDialogDestroy -= self.__onPageDialogDestroy
        self._application.onPageViewCreate -= self.__onPageViewCreate
        self._application.onPageViewDestroy -= self.__onPageViewDestroy
        self._application.onPageDialogPageFactoriesNeeded -= self.__onPageDialogPageFactoriesNeeded
        self._application.onPageUpdateNeeded -= self.__onPageUpdateNeeded

        self._spellController.clear()

    def _addTab(self, dialog):
        if self._appearancePanel is None:
            self._appearancePanel = AppearancePanel(dialog.getPanelsParent())
            dialog.addPanel(self._appearancePanel, _(u'Appearance'))

            self._appearanceController = AppearanceController(
                self._appearancePanel,
                self._application,
                dialog)

            dialog.addController(self._appearanceController)

    def __onPageDialogPageTypeChanged(self, page, params):
        if params.pageType == HtmlWikiPage.getTypeString():
            self._addTab(params.dialog)
        elif self._appearancePanel is not None:
            params.dialog.removeController(self._appearanceController)
            params.dialog.removePanel(self._appearancePanel)
            self._appearancePanel = None
            self._appearanceController = None

    def __onPageDialogDestroy(self, page, params):
        self._appearancePanel = None
        self._appearanceController = None

    @pagetype(HtmlWikiPage)
    def __onPageViewCreate(self, page):
        assert page is not None
        self._spellController.initialize(page)

    @pagetype(HtmlWikiPage)
    def __onPageViewDestroy(self, page):
        assert page is not None
        self._spellController.clear()

    def __onPageDialogPageFactoriesNeeded(self, page, params):
        params.addPageFactory(HtmlPageFactory())

    @pagetype(HtmlWikiPage)
    def __onPageUpdateNeeded(self, page, params):
        if page.readonly:
            return
        self._updatePage(page)

    def _updatePage(self, page):
        path = page.getHtmlPath()
        html = self._makeHtml(page)
        writeTextFile(path, html)

    def _makeHtml(self, page):
        style = Style()
        stylepath = style.getPageStyle(page)

        try:
            tpl = HtmlTemplate(readTextFile(stylepath))
        except EnvironmentError:
            tpl = HtmlTemplate(readTextFile(style.getDefaultStyle()))

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

        result = tpl.substitute(content=text,
                                title=page.display_title)

        result = self._changeContentByEvent(page,
                                            PostprocessingParams(result),
                                            self._application.onPostprocessing)
        return result

    def _changeContentByEvent(self, page, params, event):
        event(page, params)
        return params.result
