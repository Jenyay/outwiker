# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import sys
import os
import logging
import urllib.request

from outwiker.core.i18n import getLanguageFromConfig, loadLanguage
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME
from outwiker.utilites.textfile import readTextFile


class Plugin (object, metaclass=ABCMeta):
    """
    Базовый класс для плагинов
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
        Инициализация интернационализации
        domain - домен в файлах перевода
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
        Свойство должно возвращать строку, описывающую версию плагина
        в формате "x.y.z".
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

    def isNewVersionAvailable(self):
        '''
            Check plugin's version by updatesUrl and return latest
            :return: latest version of the plugin
        '''
        join = os.path.join

        plugin_fname = join(self.pluginPath, PLUGIN_VERSION_FILE_NAME)
        if not os.path.exists(plugin_fname):
            return u''

        xml_content = readTextFile(plugin_fname)
        appinfo = XmlVersionParser().parse(xml_content)

        # get data from the updatesUrl
        try:
            fp = urllib.request.urlopen(appinfo.updatesUrl)
        except:
            self.logger.debug("The url %s cann't be opened" % appinfo.updatesUrl)
            return u''

        # read plugin.xml
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()

        # get currentVersion from internet
        repo_info = XmlVersionParser().parse(mystr)

        # return latest version
        return repo_info.currentVersion

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @abstractproperty
    def name(self):
        """
        Свойство должно возвращать имя плагина
        """
        pass

    @abstractproperty
    def description(self):
        """
        Свойство должно возвращать описание плагина
        """
        pass

    @property
    def url(self):
        return None

    @abstractmethod
    def initialize(self):
        """
        Этот метод вызывается, когда плагин прошел все проверки.
        Именно здесь плагин может начинать взаимодействовать с программой
        """
        pass

    @abstractmethod
    def destroy(self):
        """
        Этот метод вызывается при отключении плагина
        """
        pass


class InvalidPlugin(object):
    """
    Class with the information about plugin with errors
    """
    def __init__(self, name, description, version=u'', url=None, path=None):
        self.name = name
        self.description = description
        self.version = version if version is not None else u''
        self.url = url
        self._pluginPath = path

    @property
    def pluginPath(self):
        '''
        Return path to plugin's directory.
        '''
        return self._pluginPath