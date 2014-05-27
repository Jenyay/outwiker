#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command
from .params import *


class CommandCounter (Command):
    """
    Викикоманда, которая вместо себя вставляет последовательное число 1, 2,...
    Параметры команды:
    name - имя счетчика. Счетчики с разными именами считают независимо друг от друга
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)

        # Счетчики на странице.
        # Ключ - имя счетчика, значение - экземпляр класса _Counter
        self._counters = {}

    
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"counter"


    def execute (self, params, content):
        """
        Запустить команду на выполнение. 
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        params_dict = Command.parseParams (params)

        name = self._getNameParam (params_dict)
        start = self._getStartParam (params_dict)

        if name not in self._counters:
            self._counters[name] = _Counter()

        counter = self._counters[name]

        if start != None:
            counter.reset (start)

        result = counter.toString()
        counter.increment()

        return result


    def _getNameParam (self, params_dict):
        name = params_dict[NAME_PARAM_NAME].strip() if NAME_PARAM_NAME in params_dict else u""
        return name


    def _getStartParam (self, params_dict):
        """
        Возвращает значение параметра start (в виде целого числа) или None, если он не задан
        """
        if START_PARAM_NAME not in params_dict:
            return None

        try:
            start = int (params_dict[START_PARAM_NAME].strip())
        except ValueError:
            start = None

        return start


class _Counter (object):
    """
    Хранит информацию об одном счетчике (с определенным именем)
    """
    def __init__ (self):
        self._counter = 1


    def toString (self):
        return unicode (str (self._counter), "utf8")


    def increment (self):
        self._counter += 1


    def reset (self, startval):
        """
        Установить счетчик в значение startval
        """
        self._counter = startval
