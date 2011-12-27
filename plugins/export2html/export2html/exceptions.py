#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Export2HtmlException (BaseException):
    def __init__ (self, message):
        BaseException.__init__ (self, message)


class HtmlNotFoundError (Export2HtmlException):
    """
    Срабатывает, если нет файла со сформированным HTML-ом
    """
    pass


class FileExistsAlready (Export2HtmlException):
    """
    Срабатывает, если сохраняемый файл уже существует
    """
    pass


