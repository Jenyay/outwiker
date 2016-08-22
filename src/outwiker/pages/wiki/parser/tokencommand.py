# -*- coding: UTF-8 -*-

import re

from outwiker.libs.pyparsing import Regex


class CommandFactory (object):
    @staticmethod
    def make (parser):
        return CommandToken(parser).getToken()


class CommandToken (object):
    """
    Токен для обработки команд вида (:commandname params... :) content (:commandnameend:)
    Команда может состоять только из первой скобки (:commandname params... :)
    Параметры (params...) необязательны

    Этот токен находит в тексте команду, а затем в парсере ищет обработчика данной команды.
    Если обработчика нет, возвращается исходный текст команды
    """
    regex = r"""\(:\s*(?P<name>[\w][-\w<>]+)          # Имя команды "(:name"
            (?:\s+(?P<params>.*?)\s*)?:\)             # Параметры команды "params... :)"
            ((?P<content>.*?)                         # Контент между (:name:) и (:nameend:)
            \(:\s*(?P=name)end(?P<hasend>)\s*:\))?    # Конец команды "(:nameend:)"
            """

    def __init__ (self, parser):
        self.parser = parser

    def getToken (self):
        return Regex (self.regex, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE | re.VERBOSE).setParseAction (self.execute)("command")


    def execute (self, s, l, t):
        """
        Найти нужную команду и выполнить ее
        """
        name = t["name"]
        params = t["params"]
        content = t["content"]
        hasCmdend = False if t["hasend"] is None else True

        try:
            command = self.parser.commands[name]
        except KeyError:
            return t[0]

        if params is None:
            params = u""

        if content is None:
            content = u""

        argcount = command.execute.func_code.co_argcount

        if argcount != 4:
            return command.execute (params, content)
        else:
            return command.execute (params, content, {"hasCmdend": hasCmdend})
