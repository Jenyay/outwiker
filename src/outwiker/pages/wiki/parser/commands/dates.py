# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from datetime import datetime

from outwiker.pages.wiki.parser.command import Command
from outwiker.gui.guiconfig import GeneralGuiConfig


class CommandDateBase(Command, metaclass=ABCMeta):
    """
    Базовый класс для вставки дат
    Параметры:
        format - формат представления даты. Если этот параметр не задан, используется формат из настроек программы
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        super(CommandDateBase, self).__init__(parser)
        self.FORMAT_PARAM = "format"

    @abstractmethod
    def _getDate(self) -> datetime:
        """
        Метод должен возвращать дату (datetime), которую нужно вставить на страницу
        """
        pass

    def execute(self, params: str, content: str) -> str:
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        paramsDict = self.parseParams(params)

        if self.FORMAT_PARAM in paramsDict:
            formatStr = paramsDict[self.FORMAT_PARAM]
        else:
            formatStr = GeneralGuiConfig(
                self.parser.application.config
            ).dateTimeFormat.value

        date = self._getDate()
        result = date.strftime(formatStr)

        return result


class CommandDateCreation(CommandDateBase):
    """
    Команда для отображения даты создания страницы.
    Параметры:
        format - формат представления даты. Если этот параметр не задан, используется формат из настроек программы
    """

    @property
    def name(self) -> str:
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "crdate"

    def _getDate(self) -> datetime:
        return self.parser.page.creationdatetime


class CommandDateEdition(CommandDateBase):
    """
    Команда для отображения даты изменения страницы.
    Параметры:
        format - формат представления даты. Если этот параметр не задан, используется формат из настроек программы
    """

    @property
    def name(self) -> str:
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "eddate"

    def _getDate(self) -> datetime:
        return self.parser.page.datetime
