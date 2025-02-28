#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import logging
import os
import sys

import wx

import outwiker
from outwiker.app.owapplication import OutWikerApplication
from outwiker.app.core.starter import Starter, StarterExit
from outwiker.core.application import Application
from outwiker.core.defines import APP_DATA_DEBUG
from outwiker.core.system import getOS, getConfigPath
from outwiker.core.system import getSpecialDirList


logger = logging.getLogger("outwiker")


def print_info():
    logger.debug(
        "Current OutWiker API version: {}.{}".format(
            outwiker.__api_version__[0], outwiker.__api_version__[1]
        )
    )
    logger.debug("Python version: {}".format(sys.version))
    logger.debug("wxPython version: {}".format(wx.__version__))
    logger.debug("Current locale: {}".format(locale.setlocale(locale.LC_ALL, None)))
    logger.debug('Decimal point: "{}"'.format(locale.localeconv()["decimal_point"]))
    logger.debug("Current working directory: {}".format(os.getcwd()))
    for n, dirname in enumerate(getSpecialDirList("")):
        logger.debug("Special directory [{}]: {}".format(n, dirname))


def main():
    getOS().migrateConfig()

    config_path = getConfigPath()
    application = Application()
    application.init(config_path)

    try:
        starter = Starter(application)
    except StarterExit:
        sys.exit(1)

    application.sharedData[APP_DATA_DEBUG] = starter.isDebugMode

    outwiker_app = OutWikerApplication(application)
    outwiker_app.initLogger(starter.isDebugMode)
    print_info()

    try:
        starter.processConsole()
    except StarterExit:
        sys.exit(0)

    logger.debug("Run GUI mode")

    outwiker_app.initMainWindow()

    if starter.pluginsEnabled:
        outwiker_app.loadPlugins()

    outwiker_app.bindActivateApp()
    starter.processGUI()
    outwiker_app.showMainWindow(starter.allowMinimizingMainWindow)
    outwiker_app.MainLoop()

    logger.debug("Exit")


if __name__ == "__main__":
    main()
