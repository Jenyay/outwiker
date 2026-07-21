# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import datetime
from typing import Any

from outwiker.app.services.messages import showError
from outwiker.core.tree import WikiPage
from outwiker.core.treetools import testreadonly
from outwiker.gui.baseaction import BaseAction


class SortSibingsPagesBaseAction(BaseAction, metaclass=ABCMeta):
    def __init__(self, application):
        self._application = application

    @abstractmethod
    def sort_func(self, page: WikiPage) -> Any: ...

    def reverse(self) -> bool:
        return False

    def run(self, params):
        self.sortChildren()

    @testreadonly
    def sortChildren(self):
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _("Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            self._application.wikiroot.selectedPage.parent.sortChildren(
                self.sort_func, self.reverse()
            )


class SortSiblingsAlphabeticalAction(SortSibingsPagesBaseAction):
    """
    Sort sibling pages alphabetically
    """

    stringId = "SortSiblingsAlphabetically"

    @property
    def title(self):
        return _("Sibling pages alphabetically")

    @property
    def description(self):
        return _("Sort the sibling pages alphabetically")

    def sort_func(self, page: WikiPage) -> Any:
        return page.display_title.lower()


class SortSiblingsByCreationDateAscAction(SortSibingsPagesBaseAction):
    """
    Sort sibling pages by creation date (oldest first)
    """

    stringId = "SortSiblingsCreationDateAsc"

    @property
    def title(self):
        return _("Sibling pages by creation date (oldest first)")

    @property
    def description(self):
        return _("Sort the sibling pages by creation date (oldest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.creationdatetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return False


class SortSiblingsByCreationDateDescAction(SortSibingsPagesBaseAction):
    """
    Sort sibling pages by creation date (newest first)
    """

    stringId = "SortSiblingsCreationDateDesc"

    @property
    def title(self):
        return _("Sibling pages by creation date (newest first)")

    @property
    def description(self):
        return _("Sort the sibling pages by creation date (newest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.creationdatetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return True


class SortSiblingsByModifiedDateAscAction(SortSibingsPagesBaseAction):
    """
    Sort sibling pages by modified date (oldest first)
    """

    stringId = "SortSiblingsModifiedDateAsc"

    @property
    def title(self):
        return _("Sibling pages by modified date (oldest first)")

    @property
    def description(self):
        return _("Sort the sibling pages by modified date (oldest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.datetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return False


class SortSiblingsByModifiedDateDescAction(SortSibingsPagesBaseAction):
    """
    Sort sibling pages by modified date (newest first)
    """

    stringId = "SortSiblingsModifiedDateDesc"

    @property
    def title(self):
        return _("Sibling pages by modified date (newest first)")

    @property
    def description(self):
        return _("Sort the sibling pages by modified date (newest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.datetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return True
