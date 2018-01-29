# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import sys
import os

from outwiker.core.i18n import getLanguageFromConfig, loadLanguage


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
        self.gettext = self.lang.gettext
        return self.gettext

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
    def __init__(self, name, description, version=u'', url=None):
        self.name = name
        self.description = description
        self.version = version if version is not None else u''
        self.url = url
