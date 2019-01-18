#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os

from outwiker.core.application import Application
from outwiker.core.defines import APP_DATA_DEBUG
from outwiker.core.system import getOS, getConfigPath
from outwiker.core.i18n import initLocale
from outwiker.core.starter import Starter, StarterExit
from outwiker.core.system import getSpecialDirList
from outwiker.gui.owapplication import OutWikerApplication


logger = logging.getLogger('outwiker')


def print_info():
    logger.debug(u'Current working directory: {}'.format(os.getcwd()))
    for n, dirname in enumerate(getSpecialDirList(u'')):
        logger.debug(u'Special directory [{}]: {}'.format(n, dirname))


if __name__ == "__main__":
    getOS().migrateConfig()

    config_path = getConfigPath()
    application = Application
    application.init(config_path)

    outwiker = OutWikerApplication(application)
    locale = initLocale(outwiker.application.config)
    starter = Starter(application)

    application.sharedData[APP_DATA_DEBUG] = starter.isDebugMode
    outwiker.initLogger(starter.isDebugMode)
    print_info()

    try:
        starter.processConsole()
    except StarterExit:
        outwiker.destroyMainWindow()
    else:
        logger.debug('Run GUI mode')

        outwiker.initMainWindow()

        if starter.pluginsEnabled:
            outwiker.loadPlugins()

        outwiker.showMainWindow(starter.allowMinimizingMainWindow)
        outwiker.bindActivateApp()
        starter.processGUI()
        outwiker.MainLoop()

    logger.debug('Exit')
