#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class BaseAction (object):
    __metaclass__ = ABCMeta
    
    @abstractproperty
    def title (self):
        """
        Надпись, отображаемая в меню и на всплывающих подсказках на кнопках
        """
        pass


    @abstractproperty
    def description (self):
        """
        Короткое описание, показываемое в настройках горячих клавиш
        """
        pass


    @abstractproperty
    def strid (self):
        """
        Уникальный строковый идентификатор действия. Используется для задания горчячих клавиш через файл настроек и для идентификации действий
        """
        pass


    @abstractmethod
    def run (self, params):
        """
        Метод, выполняемый при активации действия
        params - параметры, зависящие от типа кнопки/меню. Для обычной кнопки всегда равно None, для зажимаемой кнпоки указывает, кнопка нажата или отжата
        """
        pass
