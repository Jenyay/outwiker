# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import sys
import os
import logging

from outwiker.core.i18n import getLanguageFromConfig, loadLanguage


class Plugin (object, metaclass=ABCMeta):
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
        self._version = u'0.0'

        self.logger = logging.getLogger(self.name)

        domain = self.name.lower()
        langdir = os.path.join(self.pluginPath, "locale")
        self._init_i18n(domain, langdir)

    def _init_i18n(self, domain, langdir):
        """
        init localisation settings
        domain - domain in localisation files
        langdir - путь до папки с переводами
        """
        language = getLanguageFromConfig(self._application.config)
        self.lang = loadLanguage(language, langdir, domain)

        if self.lang is not None:
            self.gettext = self.lang.gettext
        else:
            self.logger.debug('Localization not found.')
            self.gettext = self._no_translate
        return self.gettext

    def _no_translate(self, text):
        return text

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


class InvalidPlugin(object):
    """
    Class with the information about plugin with errors
    """
    def __init__(self, name, description, version=u'', url=None):
        self.name = name
        self.description = description
        self.version = version if version is not None else u''
        self.url = url
