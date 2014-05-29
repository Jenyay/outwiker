#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command
from .params import *


class CommandCounter (Command):
    """
    Викикоманда, которая вместо себя вставляет последовательное число 1, 2,...
    Параметры команды:
    
    name - имя счетчика. Счетчики с разными именами считают независимо друг от друга

    start - значение, с которого нужно начинать новый отсчет. Это значение не обязательно должно быть в самом первом упоминании счетчика. С помощью этого параметра можно "сбрасывать" счетчикк нужному значению даже в середине страницы.

    step - приращение для значения счетчика

    parent - имя родительского счетчика для создания нумерации вроде 1.1, 1.2.3 и т.п.

    hide - счетчик нужно скрыть, но при этом увеличить его значение
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
        step = self._getStepParam (params_dict)
        parent = self._getParentParam (params_dict)
        hide = self._getHideParam (params_dict)

        if name not in self._counters:
            self._counters[name] = _Counter()

        counter = self._counters[name]

        if start != None:
            counter.reset (start, parent)
        else:
            counter.next(step, parent)

        return u"" if hide else counter.toString() 


    def _getNameParam (self, params_dict):
        name = params_dict[NAME_PARAM_NAME].strip() if NAME_PARAM_NAME in params_dict else u""
        return name


    def _getStartParam (self, params_dict):
        """
        Возвращает значение параметра start (в виде целого числа) или None, если он не задан
        """
        return self._getIntParam (params_dict, START_PARAM_NAME)


    def _getStepParam (self, params_dict):
        """
        Возвращает значение параметра step (в виде целого числа) или None, если он не задан
        """
        step = self._getIntParam (params_dict, STEP_PARAM_NAME)
        if step == None:
            step = 1

        return step


    def _getIntParam (self, params_dict, param_name):
        """
        Метод, возвращающий целочисленное значение параметра с именем param_name или None, если он не задан
        """
        if param_name not in params_dict:
            return None

        try:
            value = int (params_dict[param_name].strip())
        except ValueError:
            value = None

        return value


    def _getParentParam (self, params_dict):
        """
        Возвращает родительский счетчик (экземпляр класса _Counter), если установлен соответствующий параметр, или None, если параметр не установлен или желаемого счетчика нет.
        """
        parent = None

        parent_name = params_dict[PARENT_PARAM_NAME].strip() if PARENT_PARAM_NAME in params_dict else None

        if parent_name != None:
            parent = self._counters[parent_name] if parent_name in self._counters else None

        return parent


    def _getHideParam (self, params_dict):
        return HIDE_PARAM_NAME in params_dict


class _Counter (object):
    """
    Хранит информацию об одном счетчике (с определенным именем)
    """
    def __init__ (self):
        self._counter = 0
        self._string = None
        self._separator = u"."

        # Используется для определения, нужно ли сбрасывать свое значение, 
        # если изменился родительские значения
        self._oldParentString = None

        self._createString (None)


    def toString (self):
        return self._string


    def next (self, step, parent=None):
        """
        Установить следующее значение счетчика
        """
        self._counter += step
        self._createString (parent, startval=step)


    def reset (self, startval, parent=None):
        """
        Установить счетчик в значение startval
        """
        self._counter = startval
        self._createString (parent, startval)


    def _getMyString (self):
        return unicode (str (self._counter), "utf8")


    def _createString (self, parent, startval=1):
        myString = self._getMyString()

        if parent == None:
            self._string = myString
        else:
            parentString = parent.toString()

            if parentString != self._oldParentString:
                self._counter = startval
                self._oldParentString = parentString
                myString = self._getMyString()

            self._string = self._separator.join ([parentString, myString])
