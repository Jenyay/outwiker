# -*- coding: utf-8 -*-

import os.path

from outwiker.api.gui.actions import BaseAction
from outwiker.api.services.application import openInNewWindow

from .i18n import get_


class PlotAction(BaseAction):
    """
    Insert(:plot:) command action
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = "DataGraph_Plot"

    @property
    def title(self):
        return _("Plot graph (:plot:)")

    @property
    def description(self):
        return _("[DataGraph] Insert (:plot:) command for graph plotting")

    def run(self, params):
        startCommand = '(:plot:)'
        endCommand = '(:plotend:)'

        pageView = self._getPageView()
        pageView.codeEditor.turnText(startCommand, endCommand)

    def _getPageView(self):
        """
        Return the page view from current apge panel
        """
        return self._application.mainWindow.pagePanel.pageView


class OpenHelpAction(BaseAction):
    """
    Open DataGraph help action
    """
    stringId = "DataGraph_Help"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Open help")

    @property
    def description(self):
        return _(u"[DataGraph] Open help in the new OutWiker window")

    def run(self, params):
        helpDirName = "help"

        currentdir = os.path.dirname(__file__)
        helpPath = os.path.join(currentdir, helpDirName, _("datagraph_eng"))

        args = ['--normal', '--readonly']
        openInNewWindow(helpPath, args)
