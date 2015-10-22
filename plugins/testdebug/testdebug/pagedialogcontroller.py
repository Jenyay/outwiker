# -*- coding: UTF-8 -*-

from outwiker.gui.pagedialogpanels.basecontroller import BasePageDialogController


class DebugPageDialogController (BasePageDialogController):
    def __init__ (self, application):
        super (DebugPageDialogController, self).__init__ (application)


    def setPageProperties (self, page):
        print u'DebugPageDialogController.setPageProperties()'
        return True


    def initBeforeCreation (self, parentPage):
        print u'DebugPageDialogController.initBeforeCreation()'


    def initBeforeEditing (self, currentPage):
        print u'DebugPageDialogController.initBeforeEditing()'


    def validateBeforeCreation (self, parentPage):
        print u'DebugPageDialogController.validateBeforeCreation()'
        return True


    def validateBeforeEditing (self, currentPage):
        print u'DebugPageDialogController.validateBeforeEditing()'
        return True


    def saveParams (self):
        print u'DebugPageDialogController.saveParams()'


    def clear (self):
        print u'DebugPageDialogController.clear()'
