# -*- coding: UTF-8 -*-

from abc import ABCMeta


class BasePageDialogController (object):
    __metaclass__ = ABCMeta

    def __init__ (self, application):
        self._application = application


    def setPageProperties (self, page):
        """
        Return True if success and False otherwise
        """
        return True


    def initBeforeCreation (self, parentPage):
        """
        Initialize the panel before new page creation
        parentPage - the parent page for new page
        """
        pass


    def initBeforeEditing (self, currentPage):
        """
        Initialize the panel before new page editing.
        page - page for editing
        """
        pass


    def validateBeforeCreation (self, parentPage):
        return True


    def validateBeforeEditing (self, currentPage):
        return True


    def saveParams (self):
        pass


    def clear (self):
        pass
