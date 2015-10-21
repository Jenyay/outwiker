# -*- coding: UTF-8 -*-

from outwiker.gui.pagedialogpanels.basepanel import BasePageDialogPanel


class NewPageDialogPanel (BasePageDialogPanel):
    def __init__ (self, parent, application):
        super (NewPageDialogPanel, self).__init__ (parent, application)
        self.SetBackgroundColour ("blue")


    @property
    def title (self):
        return u'Debug'


    def setPageProperties (self, page):
        """
        Return True if success and False otherwise
        """
        return True
