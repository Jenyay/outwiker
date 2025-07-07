# -*- coding: utf-8 -*-

from abc import ABCMeta

from outwiker.core.tree import WikiPage


class BasePageDialogController(metaclass=ABCMeta):
    def __init__(self, application):
        self._application = application

    def setPageProperties(self, page: WikiPage):
        """
        Return True if success and False otherwise
        """
        return True

    def initBeforeCreation(self, parentPage):
        """
        Initialize the panel before new page creation
        parentPage - the parent page for new page
        """
        pass

    def initBeforeEditing(self, currentPage: WikiPage):
        """
        Initialize the panel before new page editing.
        page - page for editing
        """
        pass

    def validateBeforeCreation(self, parentPage):
        return True

    def validateBeforeEditing(self, currentPage: WikiPage):
        return True

    def saveParams(self):
        pass

    def clear(self):
        pass
