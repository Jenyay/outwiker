# -*- coding: utf-8 -*-

import os.path

from outwiker.gui.baseaction import BaseAction
from outwiker.core.system import openInNewWindow, getMainModuleDataPath


class OpenHelpParams:
    def __init__(self, pagelink):
        self.pagelink = pagelink


class OpenHelpAction(BaseAction):
    """
    Open the OutWiker help
    """
    stringId = "Help"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Help")

    @property
    def description(self):
        return _("Open help")

    def run(self, params):
        help_dir = "help"
        current_help = _("help_en")
        path = os.path.join(getMainModuleDataPath(),
                            help_dir,
                            current_help)

        args = ['--normal', '--readonly']
        if params is not None:
            args.append('-p')
            args.append(params.pagelink)

        openInNewWindow(path, args)
