# -*- coding: utf-8 -*-
"""Classes for working with page open history."""


class HistoryEmptyException(Exception):
    """
    Raised when trying to go back if the back history is empty
    (and similarly for forward history)
    """


class History(object):
    """Class for working with page open history on a tab."""

    def __init__(self):
        # List of pages for going back (for "back" navigation)
        self._back = []

        # List of pages for going forward
        self._forward = []

        # Currently open page
        self._currentPage = None

    @property
    def backLength(self):
        return len(self._back)

    @property
    def forwardLength(self):
        return len(self._forward)

    def goto(self, newCurrentPage):
        """Transition to a new page."""
        if (
            self._currentPage is None
            and len(self._back) == 0
            and len(self._forward) == 0
        ):
            # First time opening a page
            self._currentPage = newCurrentPage
            return

        if self._currentPage == newCurrentPage:
            # If opening the same page again, do nothing
            return

        self._back.append(self._currentPage)
        self._forward = []

        self._currentPage = newCurrentPage

    def back(self):
        if self.backLength == 0:
            raise HistoryEmptyException()

        self._forward.append(self._currentPage)
        self._currentPage = self._back.pop()

        if self._currentPage is not None and self._currentPage.isRemoved:
            self._currentPage = None

        return self._currentPage

    def forward(self):
        if self.forwardLength == 0:
            raise HistoryEmptyException()

        self._back.append(self._currentPage)
        self._currentPage = self._forward.pop()

        if self._currentPage is not None and self._currentPage.isRemoved:
            self._currentPage = None

        return self._currentPage

    @property
    def currentPage(self):
        return self._currentPage
