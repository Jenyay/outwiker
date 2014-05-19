# -*- coding: UTF-8 -*-

import argparse

from outwiker.core.system import getOS


class CommandLineException (BaseException):
    pass


class _SilentParser (argparse.ArgumentParser):
    """
    Создаем производный класс от ArgumentParser, чтобы отключить автоматический показ справки в случае ошибок в параметрах
    """
    def error (self, message):
        raise CommandLineException


class CommandLine (object):
    """
    Класс для хранения разобранных параметров командной строки
    """
    def __init__ (self):
        self._parser = self._createParser()
        self._namespace = None


    def parseParams (self, args):
        """
        args - параметры командной строки (исключая outwiker.py или outwiker.exe), т.е. это argv[1:]
        """
        try:
            self._namespace = self._parser.parse_args (args)
        except SystemExit:
            raise CommandLineException


    def _createParser (self):
        parser = _SilentParser(prog = 'OutWiker',
                add_help = False)

        parser.add_argument ('wikipath', 
                nargs='?', 
                metavar = _(u"Path"),
                help=u"Path to wiki")

        parser.add_argument ('--help', '-h',
                action='store_const', 
                const=True, 
                default=False,
                help=u"Help")

        parser.add_argument ('--readonly', '-r',
                action='store_const', 
                const=True, 
                default=False,
                help=u"Read only")

        return parser


    @property
    def wikipath (self):
        result = None

        if self._namespace.wikipath != None:
            result = unicode (self._namespace.wikipath, getOS().filesEncoding)

        return result


    @property
    def help (self):
        return self._namespace.help


    @property
    def readonly (self):
        return self._namespace.readonly


    def format_help (self):
        """
        Возвращает строку справки
        """
        return self._parser.format_help()
