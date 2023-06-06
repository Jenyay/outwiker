# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction

from .i18n import get_
from .tocwikimaker import TocWikiMaker


class GenerateTOC(BaseAction):
    """
    Создать и вставить оглавление
    """

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = "TableOfContents_GenerateToC"

    @property
    def title(self):
        return _("Generate")

    @property
    def description(self):
        return _("TableOfContents. Generate table of contents")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.selectedPage is not None

        result = TocWikiMaker(self._application.config).make(
            self._application.selectedPage.content
        )
        self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(result)


class InsertTOCCommand(BaseAction):
    """
    Создать и вставить оглавление
    """

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = "TableOfContents_InsertToCCommand"

    @property
    def title(self):
        return _("Insert wiki command (:toc:)")

    @property
    def description(self):
        return _(
            "TableOfContents. Insert the wiki command (:toc:) for dynamic generation of the table of content"
        )

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.selectedPage is not None

        self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(
            "(:toc:)"
        )
