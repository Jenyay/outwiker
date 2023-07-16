# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction
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

    stringId = "HtmlHeads_InsertTitle"

    @property
    def title(self):
        return _("Title (:title ...:)")

    @property
    def description(self):
        return _(
            "HtmlHeads plugin. Insert (:title... :) command to add <title> tag in the page head."
        )

    def run(self, params):
        self._getEditor().turnText("(:title ", ":)")


class DescriptionAction(BaseHeadAction):
    """
    Вставить команду (:description:)
    """

    stringId = "HtmlHeads_InsertDescription"

    @property
    def title(self):
        return _("Description (:description ...:)")

    @property
    def description(self):
        return _(
            "HtmlHeads plugin. Insert (:description... :) command to add description in the page head."
        )

    def run(self, params):
        self._getEditor().turnText("(:description ", ":)")


class KeywordsAction(BaseHeadAction):
    """
    Вставить команду (:keywords:)
    """

    stringId = "HtmlHeads_InsertKeywords"

    @property
    def title(self):
        return _("Keywords (:keywords ...:)")

    @property
    def description(self):
        return _(
            "HtmlHeads plugin. Insert (:keywords... :) command to add keywords in the page head."
        )

    def run(self, params):
        self._getEditor().turnText("(:keywords ", ":)")


class CustomHeadsAction(BaseHeadAction):
    """
    Вставить команду (:htmlhead:)
    """

    stringId = "HtmlHeads_InsertHtmlHead"

    @property
    def title(self):
        return _("Custom head (:htmlhead:)")

    @property
    def description(self):
        return _(
            "HtmlHeads plugin. Insert (:htmlhead:) command to add custom tags in the page head."
        )

    def run(self, params):
        self._getEditor().turnText("(:htmlhead:)\n", "\n(:htmlheadend:)")


class StyleAction(BaseHeadAction):
    """
    Вставить команду (:style:)
    """

    stringId = "HtmlHeads_InsertStyle"

    @property
    def title(self):
        return _("CSS Style (:style:)")

    @property
    def description(self):
        return _(
            "HtmlHeads plugin. Insert (:style:) command to add custom CSS style to page."
        )

    def run(self, params):
        self._getEditor().turnText("(:style:)\n", "\n(:styleend:)")
