# -*- coding: UTF-8 -*-

import os.path
import subprocess

from outwiker.gui.baseaction import BaseAction
from outwiker.core.system import getCurrentDir, getExeFile


class OpenHelpAction (BaseAction):
    """
    Открыть справку
    """
    stringId = u"Help"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Help")


    @property
    def description (self):
        return _(u"Open help")
    

    def run (self, params):
        help_dir = u"help"
        current_help = _("help_en")
        path = os.path.join (getCurrentDir(), 
                help_dir, 
                current_help)

        exeFile = getExeFile()
        if exeFile.endswith (".exe"):
            DETACHED_PROCESS = 0x00000008
            subprocess.Popen ([exeFile, path, "--readonly"], creationflags=DETACHED_PROCESS)
        else:
            subprocess.Popen (["python", exeFile, path, "--readonly"])
