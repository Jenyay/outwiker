#!/usr/bin/env python
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
    def __init__ (self, parser):
        self.parser = parser

    def getToken (self):
        reg = r"""\(:\s*(?P<name>\w+)    # Имя команды "(:name"
            \s*(?P<params>.*?)\s*:\)     # Параметры команды "params... :)"
        ((?P<content>.*?)                # Контент между (:name:) и (:nameend:)
        \(:\s*(?P=name)end\s*:\))?       # Конец команды "(:nameend:)" """

        return Regex (reg, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE | re.VERBOSE).setParseAction (self.execute)


    def execute (self, s, l, t):
        """
        Найти нужную команду и выполнить ее
        """
        name = t["name"]
        params = t["params"]
        content = t["content"]

        if params == None:
            params = u""

        if content == None:
            content = u""

        try:
            command = self.parser.commands[name]
        except KeyError:
            return t[0]

        return command.execute (params, content)
