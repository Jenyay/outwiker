# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

from outwiker.api.gui.actions import BaseAction

from webpage.i18n import get_


class BaseWebPageAction(BaseAction, metaclass=ABCMeta):
    def __init__(self, application):
        super().__init__()
        self._application = application
        global _
        _ = get_()

    def run(self, params):
        from webpage.gui.downloaddialog import DownloadDialog, DownloadDialogController

        with DownloadDialog(self._application.mainWindow) as dlg:
            controller = DownloadDialogController(
                dlg, self._application, self._getParentPage()
            )
            controller.showDialog()

    @abstractmethod
    def _getParentPage(self):
        pass


class CreateChildWebPageAction(BaseWebPageAction):
    """Download content and create child web page."""

    stringId = "webpage_create_child_page"

    @property
    def title(self):
        return _("Create child web page")

    @property
    def description(self):
        return _("Download content from the Internet and create child web page")

    def _getParentPage(self):
        assert self._application.wikiroot is not None

        if self._application.selectedPage is None:
            return self._application.wikiroot

        return self._application.selectedPage


class CreateSiblingWebPageAction(BaseWebPageAction):
    """Download content and create sibling web page."""

    stringId = "webpage_create_sibling_page"

    @property
    def title(self):
        return _("Create sibling web page")

    @property
    def description(self):
        return _("Download content from the Internet and create sibling web page")

    def _getParentPage(self):
        assert self._application.wikiroot is not None

        if self._application.selectedPage is None:
            return self._application.wikiroot

        return self._application.selectedPage.parent
