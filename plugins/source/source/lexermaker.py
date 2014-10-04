# -*- coding: UTF-8 -*-

from pygments.lexers import get_lexer_by_name, get_lexer_for_filename
from pygments.lexers import ClassNotFound

from .params import FILE_PARAM_NAME, LANGUAGE_PARAM_NAME, LANGUAGE_DEFAULT
from .misc import getFileName


class LexerMaker (object):
    """
    Класс для создания нужного лексера
    """
    def getLexer (self, params_dict):
        if LANGUAGE_PARAM_NAME in params_dict:
            lexer = self.__getLexerByName (params_dict)
        elif FILE_PARAM_NAME in params_dict:
            lexer = self.__getLexerByFileName (params_dict)
        else:
            lexer = self.__getDefaultLexer()

        return lexer


    def __getLexerByName (self, params_dict):
        """
        Возвращает лексер для нужного языка программирования в зависимости от параметров
        """
        lang = params_dict[LANGUAGE_PARAM_NAME] if LANGUAGE_PARAM_NAME in params_dict else LANGUAGE_DEFAULT

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
        except ClassNotFound:
            lexer = self.__getDefaultLexer ()

        return lexer


    def __getLexerByFileName (self, params_dict):
        fname = getFileName (params_dict[FILE_PARAM_NAME])

        try:
            lexer = get_lexer_for_filename (fname, stripall=True)
        except ClassNotFound:
            lexer = self.__getDefaultLexer ()

        return lexer


    @staticmethod
    def __getDefaultLexer ():
        """
        Создать лексер по умолчанию
        """
        return get_lexer_by_name(LANGUAGE_DEFAULT, stripall=True)
