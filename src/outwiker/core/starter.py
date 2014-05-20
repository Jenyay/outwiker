#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
import os.path

from outwiker.core.application import Application
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.commands import openWiki
from outwiker.core.commandline import CommandLine, CommandLineException
from outwiker.core.commands import getCurrentVersion


class Starter (object):
    """
    Класс для выполнения команд из командной строки (не для разбора параметров) и начального открытия вики
    """
    def __init__ (self):
        self._commandLine = self.__parseCommandLine (sys.argv[1:])
    

    def processGUI (self):
        """
        Выполнить команды после создания GUI
        """
        if self._commandLine != None:
            self.__processGUICommands ()
        else:
            # Открыть последний открытый файл 
            # (если установлена соответствующая опция)
            self.__openRecentWiki ()


    def processConsole (self):
        """
        Выполнить команды командной строки до создания интерфейса
        """
        if self._commandLine != None:
            self.__processConsoleCommands()


    def __parseCommandLine (self, args):
        cl = None

        if len (args) > 0:
            cl = CommandLine ()
            try:
                cl.parseParams (args)
            except CommandLineException:
                print cl.format_help()
                exit (1)

        return cl


    def __processConsoleCommands (self):
        # Вывод справки
        if self._commandLine.help:
            print self._commandLine.format_help()
            exit (0)

        # Вывод информации о версии
        if self._commandLine.version:
            print ur"""OutWiker {ver}""".format (ver = str (getCurrentVersion()) )
            exit (0)
        

    def __processGUICommands (self):
        # Открытие дерева с заметками
        if self._commandLine.wikipath != None:
            openWiki (self._commandLine.wikipath, self._commandLine.readonly)


    def __openRecentWiki (self):
        """
        Открыть последнюю вики, если установлена соответствующая опция
        """
        openRecent = GeneralGuiConfig (Application.config).autoopen.value

        if openRecent and len (Application.recentWiki) > 0:
            openWiki (Application.recentWiki[0])
