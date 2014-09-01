# -*- coding: UTF-8 -*-

import sys

from outwiker.core.application import Application
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.commands import openWiki
from outwiker.core.commandline import CommandLine, CommandLineException
from outwiker.core.commands import getCurrentVersion


class StarterExit (BaseException):
    """
    Исключение бросается, если нужно прервать выполнение программы
    """
    pass


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
        # Открытие дерева с заметками
        if self._commandLine is None or self._commandLine.wikipath is None:
            self.__openRecentWiki ()
        else:
            openWiki (self._commandLine.wikipath, self._commandLine.readonly)


    def processConsole (self):
        """
        Выполнить команды командной строки до создания интерфейса
        """
        if self._commandLine is not None:
            self.__processConsoleCommands()


    def __parseCommandLine (self, args):
        cl = None

        if len (args) > 0:
            cl = CommandLine ()
            try:
                cl.parseParams (args)
            except CommandLineException:
                print cl.format_help()
                raise StarterExit

        return cl


    def __processConsoleCommands (self):
        # Вывод справки
        if self._commandLine.help:
            print self._commandLine.format_help()
            raise StarterExit

        # Вывод информации о версии
        if self._commandLine.version:
            print ur"""OutWiker {ver}""".format (ver = str (getCurrentVersion()))
            raise StarterExit


    def __openRecentWiki (self):
        """
        Открыть последнюю вики, если установлена соответствующая опция
        """
        openRecent = GeneralGuiConfig (Application.config).autoopen.value

        if openRecent and len (Application.recentWiki) > 0:
            openWiki (Application.recentWiki[0])
