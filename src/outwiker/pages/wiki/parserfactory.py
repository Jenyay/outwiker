# -*- coding: utf-8 -*-

from .parser.wikiparser import Parser
from .parser.commands.include import IncludeCommand
from .parser.commands.childlist import ChildListCommand
from .parser.commands.attachlist import AttachListCommand
from .parser.commands.dates import CommandDateCreation, CommandDateEdition
from .parser.commands.table import TableCommand


class ParserFactory:
    """
    Класс, создающий википарсер и добавляющий в него нужные команды
    """
    def __init__(self):
        # Список типов команд.
        # Экземпляры команд создаются при заполнении командами парсера
        self.__commands = [IncludeCommand,
                           ChildListCommand,
                           AttachListCommand,
                           CommandDateCreation,
                           CommandDateEdition,
                           ]


    def make(self, page, application):
        """
        Создать парсер
        page - страница, для которой создается парсер,
        config - экземпляр класса, хранящий настройки
        """
        parser = Parser(page, application)
        self._addCommands(parser)
        application.onWikiParserPrepare(parser)
        return parser


    def _addCommands(self, parser):
        """
        Добавить команды из self.__commands в парсер
        """
        for command in self.__commands:
            parser.addCommand(command(parser))

        parser.addCommand(TableCommand(parser))
        for n in range(1, 6):
            parser.addCommand(TableCommand(parser, str(n)))
