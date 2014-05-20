# -*- coding: UTF-8 -*-

import argparse

from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion


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
        self._description = ur"""OutWiker {ver}. Crossplatform programm for keeping your notes in a tree.""".format (ver = str (getCurrentVersion()) )

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
        parser = _SilentParser(prog = 'outwiker',
                description = self._description,
                epilog = "(c) Eugeniy Ilin (aka Jenyay), 2014. Released under the GNU GPL.",
                add_help = False)

        parser.add_argument ('wikipath', 
                nargs='?', 
                metavar = u"Path",
                help=u"Path to wiki")

        parser.add_argument ('--help', '-h',
                action='store_const', 
                const=True, 
                default=False,
                help=u"Help")

        parser.add_argument ('--version', '-v',
                action='store_const', 
                const=True, 
                default=False,
                help=u"Version info")

        parser.add_argument ('--readonly', '-r',
                action='store_const', 
                const=True, 
                default=False,
                help=u" Open wiki as read only")

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


    @property
    def version (self):
        return self._namespace.version


    def format_help (self):
        """
        Возвращает строку справки
        """
        return self._parser.format_help()
