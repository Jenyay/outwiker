# -*- coding: utf-8 -*-

import logging
import sys

import outwiker
from outwiker.app.services.tree import openWiki
from outwiker.core.commandline import CommandLine, CommandLineException
from outwiker.core.treetools import findPage
from outwiker.gui.guiconfig import GeneralGuiConfig


logger = logging.getLogger('outwiker.app.core.starter')


class StarterExit(Exception):
    """
    Исключение бросается, если нужно прервать выполнение программы
    """
    pass


class Starter:
    """
    Класс для выполнения команд из командной строки (не для разбора параметров)
    и начального открытия вики
    """
    def __init__(self, application):
        self._application = application
        self._commandLine = self.__parseCommandLine(sys.argv[1:])
        self._config = GeneralGuiConfig(self._application.config)

    @property
    def isDebugMode(self):
        debug_config = self._config.debug.value
        debug_cl = self._commandLine.debug
        return debug_cl or debug_config

    @property
    def pluginsEnabled(self):
        return not self._commandLine.disablePlugins

    @property
    def allowMinimizingMainWindow(self):
        return not self._commandLine.disableMinimizing

    def processGUI(self):
        """
        Выполнить команды после создания GUI
        """
        # Открытие дерева с заметками
        if self._commandLine is None or self._commandLine.wikipath is None:
            self.__openRecentWiki()
        else:
            logger.debug('Open wiki "%s"', self._commandLine.wikipath)
            openWiki(self._commandLine.wikipath, self._application, self._commandLine.readonly)

        if self._commandLine is not None:
            page = findPage(self._application, self._commandLine.page_id)
            if self._application.wikiroot is not None and page is not None:
                self._application.selectedPage = page

    def __parseCommandLine(self, args):
        cl = CommandLine()
        try:
            cl.parseParams(args)
        except CommandLineException:
            print(cl.format_help())
            raise StarterExit

        return cl

    def processConsole(self):
        """
        Выполнить команды командной строки до создания интерфейса
        """
        # Вывод справки
        if self._commandLine.help:
            print(self._commandLine.format_help())
            raise StarterExit

        # Вывод информации о версии
        if self._commandLine.version:
            print(r"""OutWiker {ver}""".format(ver=outwiker.getVersionStr()))
            raise StarterExit

    def __openRecentWiki(self):
        """
        Открыть последнюю вики, если установлена соответствующая опция
        """
        openRecent = self._config.autoopen.value

        if openRecent and len(self._application.recentWiki) > 0:
            logger.debug('Open recently used wiki')
            openWiki(self._application.recentWiki[0], self._application)
