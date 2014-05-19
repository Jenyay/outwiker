#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os.path

from outwiker.core.application import Application
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.commands import openWiki
from outwiker.core.commandline import CommandLine, CommandLineException


class Starter (object):
    """
    Класс для выполнения команд из командной строки (не для разбора параметров) и начального открытия вики
    """
    def __init__ (self):
        pass

    def process (self):
        self.generalConfig = GeneralGuiConfig (Application.config)

        if len (sys.argv) > 1:
            self.__parseCommandLine (sys.argv[1:])
        else:
            # Открыть последний открытый файл 
            # (если установлена соответствующая опция)
            self.__openRecentWiki ()


    def __parseCommandLine (self, args):
        cl = CommandLine ()
        try:
            cl.parseParams (args)
        except CommandLineException:
            print cl.format_help()
            exit (1)

        # Вывод справки
        if cl.help:
            print cl.format_help()
            exit (1)

        # Открытие дерева с заметками
        if cl.wikipath != None:
            openWiki (cl.wikipath, cl.readonly)


    def __openRecentWiki (self):
        """
        Открыть последнюю вики, если установлена соответствующая опция
        """
        openRecent = self.generalConfig.autoopen.value

        if openRecent and len (Application.recentWiki) > 0:
            openWiki (Application.recentWiki[0])
