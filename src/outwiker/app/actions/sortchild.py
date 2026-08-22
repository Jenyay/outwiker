# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import datetime
from typing import Any

from outwiker.app.services.messages import showError
from outwiker.core.tree import WikiPage
from outwiker.core.treetools import testreadonly
from outwiker.gui.baseaction import BaseAction


class SortChildPagesBaseAction(BaseAction, metaclass=ABCMeta):
    def __init__(self, application):
        self._application = application

    def reverse(self) -> bool:
        return False

    @abstractmethod
    def sort_func(self, page: WikiPage) -> Any: ...

    def run(self, params):
        self.sortChildren()

    @testreadonly
    def sortChildren(self):
        if self._application.wikiroot is None:
            showError(self._application.mainWindow, _("Wiki is not open"))
            return

        if self._application.wikiroot.selectedPage is not None:
            self._application.wikiroot.selectedPage.sortChildren(
                self.sort_func, self.reverse()
            )
        else:
            self._application.wikiroot.sortChildren(self.sort_func, self.reverse())


class SortChildAlphabeticalAction(SortChildPagesBaseAction):
    """
    Sort child pages alphabetically
    """

    stringId = "SortChildAlphabetically"

    @property
    def title(self):
        return _("Child pages alphabetically")

    @property
    def description(self):
        return _("Sort the child pages alphabetically")

    def sort_func(self, page: WikiPage) -> Any:
        return page.display_title.lower()


class SortChildByCreationDateAscAction(SortChildPagesBaseAction):
    """
    Sort child pages by creation date (oldest first)
    """

    stringId = "SortChildCreationDateAsc"

    @property
    def title(self):
        return _("Child pages by creation date (oldest first)")

    @property
    def description(self):
        return _("Sort the child pages by creation date (oldest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.creationdatetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return False


class SortChildByCreationDateDescAction(SortChildPagesBaseAction):
    """
    Sort child pages by creation date (newest first)
    """

    stringId = "SortChildCreationDateDesc"

    @property
    def title(self):
        return _("Child pages by creation date (newest first)")

    @property
    def description(self):
        return _("Sort the child pages by creation date (newest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.creationdatetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return True


class SortChildByModifiedDateAscAction(SortChildPagesBaseAction):
    """
    Sort child pages by modified date (oldest first)
    """

    stringId = "SortChildModifiedDateAscc"

    @property
    def title(self):
        return _("Child pages by modified date (oldest first)")

    @property
    def description(self):
        return _("Sort the child pages by modified date (oldest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.datetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return False


class SortChildByModifiedDateDescAction(SortChildPagesBaseAction):
    """
    Sort child pages by modified date (newest first)
    """

    stringId = "SortChildModifiedDateDesc"

    @property
    def title(self):
        return _("Child pages by modified date (newest first)")

    @property
    def description(self):
        return _("Sort the child pages by modified date (newest first)")

    def sort_func(self, page: WikiPage) -> Any:
        date = page.datetime
        if date is None:
            date = datetime.datetime(1980, 1, 1)

        return date

    def reverse(self) -> bool:
        return True
