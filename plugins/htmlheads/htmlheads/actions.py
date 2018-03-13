# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class BaseHeadAction(BaseAction):
    """
    Базовый класс действий для вставки команд
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    def _getEditor(self):
        """
        Возвращает указатель на редактор
        """
        return self._application.mainWindow.pagePanel.pageView.codeEditor


class TitleAction(BaseHeadAction):
    """
    Вставить команду (:title:)
    """
    stringId = u"HtmlHeads_InsertTitle"

    @property
    def title(self):
        return _(u"Title (:title ...:)")

    @property
    def description(self):
        return _(u"HtmlHeads plugin. Insert (:title... :) command to add <title> tag in the page head.")

    def run(self, params):
        self._getEditor().turnText(u"(:title ", u":)")


class DescriptionAction(BaseHeadAction):
    """
    Вставить команду (:description:)
    """
    stringId = u"HtmlHeads_InsertDescription"

    @property
    def title(self):
        return _(u"Description (:description ...:)")

    @property
    def description(self):
        return _(u"HtmlHeads plugin. Insert (:description... :) command to add description in the page head.")

    def run(self, params):
        self._getEditor().turnText(u"(:description ", u":)")


class KeywordsAction(BaseHeadAction):
    """
    Вставить команду (:keywords:)
    """
    stringId = u"HtmlHeads_InsertKeywords"

    @property
    def title(self):
        return _(u"Keywords (:keywords ...:)")

    @property
    def description(self):
        return _(u"HtmlHeads plugin. Insert (:keywords... :) command to add keywords in the page head.")

    def run(self, params):
        self._getEditor().turnText(u"(:keywords ", u":)")


class CustomHeadsAction(BaseHeadAction):
    """
    Вставить команду (:htmlhead:)
    """
    stringId = u"HtmlHeads_InsertHtmlHead"

    @property
    def title(self):
        return _(u"Custom head (:htmlhead:)")

    @property
    def description(self):
        return _(u"HtmlHeads plugin. Insert (:htmlhead:) command to add custom tags in the page head.")

    def run(self, params):
        self._getEditor().turnText(u"(:htmlhead:)\n", u"\n(:htmlheadend:)")


class StyleAction(BaseHeadAction):
    """
    Вставить команду (:style:)
    """
    stringId = u"HtmlHeads_InsertStyle"

    @property
    def title(self):
        return _(u"CSS Style (:style:)")

    @property
    def description(self):
        return _(u"HtmlHeads plugin. Insert (:style:) command to add custom CSS style to page.")

    def run(self, params):
        self._getEditor().turnText(u"(:style:)\n", u"\n(:styleend:)")
