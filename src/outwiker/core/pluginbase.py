# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import sys
import os

from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME, VERSIONS_LANG
from outwiker.core.i18n import getLanguageFromConfig, loadLanguage
from outwiker.core.system import getOS
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.utilites.textfile import readTextFile


class Plugin (object):
    """
    Базовый класс для плагинов
    """
    __metaclass__ = ABCMeta

    def __init__ (self, application):
        self._application = application

        self._pluginPath = os.path.dirname(os.path.abspath(
            sys.modules[self.__class__.__module__].__file__)
        )

        # Added in OutWiker 2.0.0.801
        self._pluginPath = unicode(self._pluginPath, getOS().filesEncoding)

        # Load plugin's information
        self._version = u'0.0'
        path = os.path.join (self._pluginPath, PLUGIN_VERSION_FILE_NAME)
        try:
            text = readTextFile(path)
            versionInfo = XmlVersionParser([_(VERSIONS_LANG), u'en']).parse(text)
            self._version = unicode(versionInfo.currentVersion)
        except (EnvironmentError, ValueError):
            pass


    def _init_i18n (self, domain, langdir):
        """
        Инициализация интернационализации
        domain - домен в файлах перевода
        langdir - путь до папки с переводами
        """
        language = getLanguageFromConfig (self._application.config)
        lang = loadLanguage (language, langdir, domain)
        return lang.ugettext

    @property
    def version (self):
        """
        Свойство должно возвращать строку, описывающую версию плагина в формате "x.y.z"
        Will be reloaded for Outwiker version before 2.0.0.801
        """
        return self._version


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @abstractproperty
    def name (self):
        """
        Свойство должно возвращать имя плагина
        """
        pass


    @abstractproperty
    def description (self):
        """
        Свойство должно возвращать описание плагина
        """
        pass


    @property
    def url (self):
        return None


    @abstractmethod
    def initialize (self):
        """
        Этот метод вызывается, когда плагин прошел все проверки.
        Именно здесь плагин может начинать взаимодействовать с программой
        """
        pass


    @abstractmethod
    def destroy (self):
        """
        Этот метод вызывается при отключении плагина
        """
        pass

    #############################################
