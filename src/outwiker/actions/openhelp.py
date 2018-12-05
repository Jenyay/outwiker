# -*- coding: utf-8 -*-

import os.path

from outwiker.gui.baseaction import BaseAction
from outwiker.core.system import getCurrentDir, openInNewWindow


class OpenHelpParams(object):
    def __init__(self, pagelink):
        self.pagelink = pagelink


class OpenHelpAction(BaseAction):
    """
    Open the OutWiker help
    """
    stringId = u"Help"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Help")

    @property
    def description(self):
        return _(u"Open help")

    def run(self, params):
        help_dir = u"help"
        current_help = _("help_en")
        path = os.path.join(getCurrentDir(),
                            help_dir,
                            current_help)

        args = [u'--normal', u'--readonly']
        if params is not None:
            args.append(u'-p')
            args.append(params.pagelink)

        openInNewWindow(path, args)
