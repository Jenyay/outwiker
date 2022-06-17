# -*- coding: utf-8 -*-

import logging
import os
import sys
from abc import ABCMeta, abstractmethod, abstractproperty

from outwiker.core.i18n import getLanguageFromConfig, loadLanguage


class Plugin(metaclass=ABCMeta):
    """
    Base class for plugins.
    The class defines minimal plugin's interface.
    Properties and settings under "Abstract properties and methods"
    should be redefined in real class.
    """

    def __init__(self, application):
        self._application = application

        self._pluginPath = os.path.dirname(os.path.abspath(
            sys.modules[self.__class__.__module__].__file__)
        )

        # Load plugin's information
        self._version = '0.0'

        self.logger = logging.getLogger(self.name)
        self.gettext = self._init_i18n()

    def _init_i18n(self):
        """
        init localization settings
        domain - domain in localization files
        langdir - путь до папки с переводами
        """
        domain = self.name.lower()
        langdir = os.path.join(self._pluginPath, "locale")

        language = getLanguageFromConfig(self._application.config)
        lang = loadLanguage(language, langdir, domain)

        if lang is not None:
            return lang.gettext
        else:
            self.logger.debug('Localization not found.')
            return lambda text: text

    @property
    def version(self):
        """
        Property should return the plugin version
        as a formatted string: "x.y.z".
        """
        return self._version

    @version.setter
    def version(self, value):
        self._version = value

    @property
    def pluginPath(self):
        '''
        Return path to plugin's directory.
        '''
        return self._pluginPath

    ###################################
    # Abstract properties and methods #
    ###################################

    @abstractproperty
    def name(self):
        """
        The property should return the plugin's name
        """
        pass

    @abstractproperty
    def description(self):
        """
        The property should return the plugin's description
        """
        pass

    @property
    def url(self):
        return None

    @abstractmethod
    def initialize(self):
        """
        The method is called if plugin has been successfully loaded
        Generally the plugin starts to work with an application here.
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        The method is called if plugin is disabled.
        """
        pass
