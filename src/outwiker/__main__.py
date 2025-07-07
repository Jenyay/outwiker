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
from outwiker.core.defines import APP_DATA_DEBUG, OUTWIKER_PATH_ENV_VAR
from outwiker.core.system import getOS, getConfigPath, getMainModulePath
from outwiker.core.system import getSpecialDirList


logger = logging.getLogger("outwiker")


def print_info():
    logger.debug(
        "Current OutWiker API version: {}.{}".format(
            outwiker.__api_version__[0], outwiker.__api_version__[1]
        )
    )
    logger.debug("Python version: %s", sys.version)
    logger.debug("wxPython version: %s", wx.__version__)
    logger.debug("Current locale: %s", locale.setlocale(locale.LC_ALL, None))
    logger.debug('Decimal point: "%s"', locale.localeconv()["decimal_point"])
    logger.debug("Current working directory: %s", os.getcwd())
    logger.debug("Main module directory: %s", getMainModulePath())
    logger.debug("%s=%s", OUTWIKER_PATH_ENV_VAR, os.environ.get(OUTWIKER_PATH_ENV_VAR))
    for n, dirname in enumerate(getSpecialDirList("")):
        logger.debug("Special directory [%d]: %s", n, dirname)


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
