#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os.path

from .application import Application
from outwiker.gui.guiconfig import GeneralGuiConfig
from .commands import openWiki
from .system import getOS


class Starter (object):
    """
    Класс для выполнения команд из командной строки (не для разбора параметров) и начального открытия вики
    """
    def __init__ (self):
        pass

    def process (self):
        self.generalConfig = GeneralGuiConfig (Application.config)

        if len (sys.argv) > 1:
            self.__openFromCommandLine()
        else:
            # Открыть последний открытый файл 
            # (если установлена соответствующая опция)
            self.__openRecentWiki ()


    def __openRecentWiki (self):
        """
        Открыть последнюю вики, если установлена соответствующая опция
        """
        openRecent = self.generalConfig.autoopen.value

        if openRecent and len (Application.recentWiki) > 0:
            openWiki (Application.recentWiki[0])


    def __openFromCommandLine (self):
        """
        Открыть вики, путь до которой передан в командной строке
        """
        fname = unicode (sys.argv[1], getOS().filesEncoding)

        if len (fname) > 0:
            if not os.path.isdir (fname):
                fname = os.path.split (fname)[0]
            openWiki (fname)
        else:
            self.__openRecentWiki ()
