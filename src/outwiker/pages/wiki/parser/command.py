# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import re


class Command (object, metaclass=ABCMeta):
    """
    Абстрактный базовый класс для команд.
    """

    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        self.parser = parser


    @abstractproperty
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        pass


    @abstractmethod
    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        pass


    @staticmethod
    def parseParams (params):
        """
        Parse params string into parts: key - value. Key may contain a dot.
        Sample params:
            param1 Параметр2.subparam = 111 Параметр3 = " bla bla bla" param4.sub.param2 = "111" param5 =' 222 ' param7 = " sample 'bla bla bla' example" param8 = ' test "bla-bla-bla" test '

            Changes in 1.9.0.761: name may contain a dot.
        """
        pattern = r"""((?P<name>[\w.]+)
    (\s*=\s*(?P<param>([-_\w.]+)|((?P<quote>["']).*?(?P=quote)) ) )?\s*)"""

        result = {}

        regex = re.compile (pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)
        matches = regex.finditer (params)

        for match in matches:
            name = match.group ("name")
            param = match.group ("param")
            if param is None:
                param = u""

            result[name] = Command.removeQuotes (param)

        return result


    @staticmethod
    def removeQuotes (text):
        """
        Удалить начальные и конечные кавычки, которые остались после разбора параметров
        """
        if (len (text) > 0 and
                (text[0] == text[-1] == "'" or
                    text[0] == text[-1] == '"')):
            return text[1:-1]

        return text
