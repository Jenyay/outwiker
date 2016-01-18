# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction

from webpage.i18n import get_


class ShowPageInfoAction (BaseAction):
    stringId = u"webpage_show_page_info"

    def __init__ (self, application):
        super (ShowPageInfoAction, self).__init__()
        self._application = application
        global _
        _ = get_()


    def run (self, params):
        from webpage.infodialog import InfoDialog, InfoDialogController

        page = self._application.selectedPage
        assert page is not None

        with InfoDialog (self._application.mainWindow) as dlg:
            controller = InfoDialogController (dlg, self._application, page)
            controller.showDialog()


    @property
    def title (self):
        return _(u"Show web page information")


    @property
    def description (self):
        return _(u'WebPage. Show current web page information.')
