#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys

from outwiker.core.application import Application
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

    outwiker.initLogger()
    print_info()

    locale = initLocale(outwiker.application.config)
    outwiker.initMainWindow()

    outwiker.loadPlugins()
    try:
        starter = Starter()
        starter.processConsole()
    except StarterExit:
        sys.exit()

    outwiker.showMainWindow()
    outwiker.bindActivateApp()

    starter.processGUI()

    outwiker.MainLoop()
    logger.debug('Exit')
