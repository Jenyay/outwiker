#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys

import wx

import outwiker
from outwiker.core.application import Application
from outwiker.core.defines import APP_DATA_DEBUG
from outwiker.core.system import getOS, getConfigPath, getSpellDirList
from outwiker.core.i18n import initLocale
from outwiker.core.starter import Starter, StarterExit
from outwiker.core.system import getSpecialDirList
from outwiker.gui.owapplication import OutWikerApplication


logger = logging.getLogger('outwiker')


def print_info():
    logger.debug('Python version: {}'.format(sys.version))
    logger.debug('wxPython version: {}'.format(wx.__version__))
    logger.debug('Current OutWiker API version: {}.{}'.format(
        outwiker.__api_version__[0], outwiker.__api_version__[1]))
    logger.debug(u'Current working directory: {}'.format(os.getcwd()))
    for n, dirname in enumerate(getSpecialDirList(u'')):
        logger.debug(u'Special directory [{}]: {}'.format(n, dirname))


if __name__ == "__main__":
    getOS().migrateConfig()

    DICPATH = ':'.join(getSpellDirList())
    os.environ['DICPATH'] = DICPATH

    config_path = getConfigPath()
    application = Application
    application.init(config_path)

    outwiker_app = OutWikerApplication(application)
    locale = initLocale(outwiker_app.application.config)

    try:
        starter = Starter(application)
    except StarterExit:
        sys.exit(1)

    application.sharedData[APP_DATA_DEBUG] = starter.isDebugMode
    outwiker_app.initLogger(starter.isDebugMode)
    print_info()

    try:
        starter.processConsole()
    except StarterExit:
        sys.exit(0)

    logger.debug('Run GUI mode')

    outwiker_app.initMainWindow()

    if starter.pluginsEnabled:
        outwiker_app.loadPlugins()

    outwiker_app.showMainWindow(starter.allowMinimizingMainWindow)
    outwiker_app.bindActivateApp()
    starter.processGUI()
    outwiker_app.MainLoop()

    logger.debug('Exit')
