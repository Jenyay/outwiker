# -*- coding: utf-8 -*-


from .params import FILE_PARAM_NAME, LANGUAGE_PARAM_NAME, LANGUAGE_DEFAULT
from .misc import getFileName


class LexerMaker:
    """
    Class for creating the required lexer
    """

    def getLexer(self, params_dict):
        if LANGUAGE_PARAM_NAME in params_dict:
            lexer = self.__getLexerByName(params_dict)
        elif FILE_PARAM_NAME in params_dict:
            lexer = self.__getLexerByFileName(params_dict)
        else:
            lexer = self.__getDefaultLexer()

        return lexer

    def __getLexerByName(self, params_dict):
        """
        Returns lexer for the specified programming language
        based on parameters
        """
        from pygments.lexers import ClassNotFound
        from pygments.lexers import get_lexer_by_name

        lang = (
            params_dict[LANGUAGE_PARAM_NAME]
            if LANGUAGE_PARAM_NAME in params_dict
            else LANGUAGE_DEFAULT
        )

        try:
            lexer = get_lexer_by_name(lang)
        except ClassNotFound:
            lexer = self.__getDefaultLexer()

        return lexer

    def __getLexerByFileName(self, params_dict):
        from pygments.lexers import ClassNotFound
        from pygments.lexers import get_lexer_for_filename

        fname = getFileName(params_dict[FILE_PARAM_NAME])

        try:
            lexer = get_lexer_for_filename(fname, stripall=True)
        except ClassNotFound:
            lexer = self.__getDefaultLexer()

        return lexer

    @staticmethod
    def __getDefaultLexer():
        """
        Create default lexer
        """
        from pygments.lexers import get_lexer_by_name

        return get_lexer_by_name(LANGUAGE_DEFAULT, stripall=True)
