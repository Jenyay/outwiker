# -*- coding: UTF-8 -*-
"""
Необходимые классы для создания страниц с HTML
"""

import os

from outwiker.core.application import Application
from outwiker.core.config import BooleanOption
from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.core.events import (PreprocessingParams,
                                  PreHtmlImprovingParams,
                                  PostprocessingParams,
                                  PAGE_UPDATE_CONTENT
                                  )
from outwiker.core.factory import PageFactory
from outwiker.core.htmlimproverfactory import HtmlImproverFactory
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.style import Style
from outwiker.core.tree import WikiPage
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.gui.hotkey import HotKey
from outwiker.pages.html.htmlpageview import HtmlPageView
from outwiker.utilites.textfile import writeTextFile, readTextFile

from actions.autolinewrap import HtmlAutoLineWrap
from actions.switchcoderesult import SwitchCodeResultAction

_actions = [
    (HtmlAutoLineWrap, None),
    (SwitchCodeResultAction, HotKey ("F4")),
]


class HtmlWikiPage (WikiPage):
    """
    Класс HTML-страниц
    """
    def __init__ (self, path, title, parent, readonly=False):
        WikiPage.__init__ (self, path, title, parent, readonly)

        self.__autoLineWrapSection = u"General"
        self.__autoLineWrapParam = u"LineWrap"


    @property
    def autoLineWrap (self):
        """
        Добавлять ли теги <br> и <p> вместо разрывов строк?
        """
        option = BooleanOption (self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True)
        return option.value


    @autoLineWrap.setter
    def autoLineWrap (self, value):
        """
        Добавлять ли теги <br> и <p> вместо разрывов строк?
        """
        option = BooleanOption (self.params, self.__autoLineWrapSection, self.__autoLineWrapParam, True)
        option.value = value
        self.root.onPageUpdate (self, change=PAGE_UPDATE_CONTENT)


    @staticmethod
    def getTypeString ():
        return u"html"

    def getHtmlPath(self):
        """
        Получить путь до результирующего файла HTML
        """
        return os.path.join (self.path, PAGE_RESULT_HTML)

    def update(self):
        if self.readonly:
            return

        path = self.getHtmlPath()
        html = self._makeHtml()
        writeTextFile(path, html)

    def _makeHtml(self):
        style = Style()
        stylepath = style.getPageStyle(self)

        try:
            tpl = HtmlTemplate(readTextFile(stylepath))
        except EnvironmentError:
            tpl = HtmlTemplate(readTextFile(style.getDefaultStyle()))

        content = self._changeContentByEvent(
            self,
            PreprocessingParams(self.content),
            Application.onPreprocessing)

        if self.autoLineWrap:
            content = self._changeContentByEvent(
                self,
                PreHtmlImprovingParams(content),
                Application.onPreHtmlImproving)

            config = HtmlRenderConfig(Application.config)
            improverFactory = HtmlImproverFactory(Application)
            text = improverFactory[config.HTMLImprover.value].run(content)
        else:
            text = content

        userhead = u"<title>{}</title>".format(self.title)
        result = tpl.substitute(content=text,
                                userhead=userhead)

        result = self._changeContentByEvent(self,
                                            PostprocessingParams(result),
                                            Application.onPostprocessing)
        return result

    def _changeContentByEvent(self, page, params, event):
        event(page, params)
        return params.result


class HtmlPageFactory (PageFactory):
    """
    Фабрика для создания HTML-страниц и их представлений
    """
    @staticmethod
    def registerActions (application):
        """
        Зарегистрировать все действия, связанные с HTML-страницей
        """
        map (lambda actionTuple: application.actionController.register (actionTuple[0](application), actionTuple[1]), _actions)


    @staticmethod
    def removeActions (application):
        map (lambda actionTuple: application.actionController.removeAction (actionTuple[0].stringId), _actions)


    def getPageType(self):
        return HtmlWikiPage


    @property
    def title (self):
        """
        Название страницы, показываемое пользователю
        """
        return _(u"HTML Page")


    def getPageView (self, parent):
        """
        Вернуть контрол, который будет отображать и редактировать страницу
        """
        return HtmlPageView (parent)
