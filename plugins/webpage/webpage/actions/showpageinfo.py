# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import BaseAction

from webpage.i18n import get_


class ShowPageInfoAction(BaseAction):
    stringId = "webpage_show_page_info"

    def __init__(self, application):
        super().__init__()
        self._application = application
        global _
        _ = get_()

    def run(self, params):
        from webpage.gui.infodialog import InfoDialog, InfoDialogController

        page = self._application.selectedPage
        assert page is not None

        with InfoDialog(self._application.mainWindow) as dlg:
            controller = InfoDialogController(dlg, self._application, page)
            controller.showDialog()

    @property
    def title(self):
        return _("Show web page information")

    @property
    def description(self):
        return _("WebPage. Show current web page information.")
