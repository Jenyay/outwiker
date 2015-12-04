# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class DownloadAction (BaseAction):
    """
    Download content and create web page
    """
    stringId = u"download_webpage_action"

    def __init__ (self, application):
        super (DownloadAction, self).__init__()
        self._application = application

    @property
    def title (self):
        return _(u"Create web page")


    @property
    def description (self):
        return _(u'Download content from the Internet and create a web page')


    def run (self, params):
        from webpage.downloaddialog import (DownloadDialog,
                                            DownloadDialogController)

        with DownloadDialog (self._application.mainWindow) as dlg:
            controller = DownloadDialogController (dlg, self._application)
            controller.showDialog()
