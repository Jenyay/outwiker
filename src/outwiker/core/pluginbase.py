# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

from outwiker.core.i18n import getLanguageFromConfig, loadLanguage


class Plugin (object):
    """
    Базовый класс для плагинов
    """
    __metaclass__ = ABCMeta

    def __init__ (self, application):
        self._application = application


    def _init_i18n (self, domain, langdir):
        """
        Инициализация интернационализации
        domain - домен в файлах перевода
        langdir - путь до папки с переводами
        """
        language = getLanguageFromConfig (self._application.config)
        lang = loadLanguage (language, langdir, domain)
        return lang.ugettext


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


    @abstractproperty
    def version (self):
        """
        Свойство должно возвращать строку, описывающую версию плагина в формате "x.y.z"
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
