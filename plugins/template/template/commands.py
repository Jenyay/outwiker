# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.wikiparser import Command


class CommandPlugin(Command):
    """ """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        super().__init__(parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "PluginCommand"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды
        в вики-нотации
        """
        params_dict = Command.parseParams(params)

        return "Plugin Command Result"
