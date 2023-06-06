# -*- coding: utf-8 -*-


class Export2HtmlException(Exception):
    def __init__(self, message):
        super().__init__(message)


class HtmlNotFoundError(Export2HtmlException):
    """
    Срабатывает, если нет файла со сформированным HTML-ом
    """

    pass


class FileAlreadyExists(Export2HtmlException):
    """
    Срабатывает, если сохраняемый файл уже существует
    """

    pass


class InvalidPageFormat(Export2HtmlException):
    """
    Срабатывает, если данную страницу невозможно преобразовать в HTML
    """

    pass


class FolderNotExists(Export2HtmlException):
    """
    Срабатывает, если нет папки, куда надо сохранить страницу
    """

    pass
