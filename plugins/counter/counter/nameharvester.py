# -*- coding: utf-8 -*-

from typing import Set

from outwiker.api.pages.wiki.parser.command import Command
from .params import NAME_PARAM_NAME


class NameHarvester(Command):
    """
    Команда, используется для сбора имен счетчиков на странице.
    Эта команда единственная, на которую будет настроен парсер при
    создании диалога плагина.
    """

    # Счетчики на странице.
    counters: Set[str] = set()

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

        NameHarvester.counters = set()

    @property
    def name(self) -> str:
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "counter"

    def execute(self, params, content) -> str:
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        params_dict = Command.parseParams(params)

        name = self._getNameParam(params_dict)
        if len(name) != 0:
            NameHarvester.counters.add(name)

        return ""

    def _getNameParam(self, params_dict) -> str:
        name = (
            params_dict[NAME_PARAM_NAME].strip()
            if NAME_PARAM_NAME in params_dict
            else ""
        )
        return name
