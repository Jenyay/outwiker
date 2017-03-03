# -*- coding: UTF-8 -*-

import os.path

from outwiker.gui.baseaction import BaseAction
from outwiker.core.system import getOS, openInNewWindow
from .i18n import get_


class PlotAction(BaseAction):
    """
    Insert(:plot:) command action
    """
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"DataGraph_Plot"

    @property
    def title(self):
        return _(u"Plot graph (:plot:)")

    @property
    def description(self):
        return _(u"[DataGraph] Insert (:plot:) command for graph plotting")

    def run(self, params):
        startCommand = u'(:plot:)'
        endCommand = u'(:plotend:)'

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
    stringId = u"DataGraph_Help"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Open help")

    @property
    def description(self):
        return _(u"[DataGraph] Open help in the new OutWiker window")

    def run(self, params):
        encoding = getOS().filesEncoding
        helpDirName = u"help"
        currentdir = unicode(os.path.dirname(__file__), encoding)

        helpPath = os.path.join(currentdir, helpDirName, _("datagraph_eng"))

        args = [u'--normal', u'--readonly']
        openInNewWindow(helpPath, args)
