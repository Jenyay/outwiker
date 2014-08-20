# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

from command import Command
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.system import getOS
from outwiker.core.application import Application


class CommandDateBase (Command):
    """
    Базовый класс для вставки дат
    Параметры:
        format - формат представления даты. Если этот параметр не задан, используется формат из настроек программы
    """
    __metaclass__ = ABCMeta

    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        super (CommandDateBase, self).__init__ (parser)

        self.FORMAT_PARAM = u"format"


    @abstractmethod
    def _getDate (self):
        """
        Метод должен возвращать дату (datetime), которую нужно вставить на страницу
        """
        pass


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        paramsDict = self.parseParams (params)

        if self.FORMAT_PARAM in paramsDict:
            formatStr = paramsDict[self.FORMAT_PARAM]
        else:
            formatStr = GeneralGuiConfig (Application.config).dateTimeFormat.value

        result = unicode (
            self._getDate().strftime (formatStr.encode ("utf8")),
            getOS().filesEncoding
        )

        return result


class CommandDateCreation (CommandDateBase):
    """
    Команда для отображения даты создания страницы.
    Параметры:
        format - формат представления даты. Если этот параметр не задан, используется формат из настроек программы
    """
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"crdate"


    def _getDate (self):
        return self.parser.page.creationdatetime


class CommandDateEdition (CommandDateBase):
    """
    Команда для отображения даты изменения страницы.
    Параметры:
        format - формат представления даты. Если этот параметр не задан, используется формат из настроек программы
    """
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"eddate"


    def _getDate (self):
        return self.parser.page.datetime
