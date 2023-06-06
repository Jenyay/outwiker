# -*- coding: utf-8 -*-

from outwiker.gui.pagedialogpanels.basecontroller import BasePageDialogController


class DebugPageDialogController(BasePageDialogController):
    def __init__(self, application):
        super().__init__(application)

    def setPageProperties(self, page):
        print("DebugPageDialogController.setPageProperties()")
        return True

    def initBeforeCreation(self, parentPage):
        print("DebugPageDialogController.initBeforeCreation()")

    def initBeforeEditing(self, currentPage):
        print("DebugPageDialogController.initBeforeEditing()")

    def validateBeforeCreation(self, parentPage):
        print("DebugPageDialogController.validateBeforeCreation()")
        return True

    def validateBeforeEditing(self, currentPage):
        print("DebugPageDialogController.validateBeforeEditing()")
        return True

    def saveParams(self):
        print("DebugPageDialogController.saveParams()")

    def clear(self):
        print("DebugPageDialogController.clear()")
