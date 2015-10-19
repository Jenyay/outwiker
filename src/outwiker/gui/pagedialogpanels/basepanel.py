# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractproperty

import wx


class BasePageDialogPanel (wx.Panel):
    __metaclass__ = ABCMeta

    def __init__ (self, parent, application):
        super (BasePageDialogPanel, self).__init__ (parent)
        self._application = application


    @abstractproperty
    def title (self):
        pass


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
