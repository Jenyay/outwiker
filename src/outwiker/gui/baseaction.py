# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class BaseAction (metaclass=ABCMeta):
    @abstractproperty
    def title(self):
        """
        Надпись, отображаемая в меню и на всплывающих подсказках на кнопках
        """

    @abstractproperty
    def description(self):
        """
        Короткое описание, показываемое в настройках горячих клавиш
        """

    @abstractmethod
    def run(self, params):
        """
        Метод, выполняемый при активации действия
        params - параметры, зависящие от типа кнопки/меню.
        Для обычной кнопки всегда равно None, для зажимаемой кнопки указывает,
        кнопка нажата или отжата
        """
