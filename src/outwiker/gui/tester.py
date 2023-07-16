# -*- coding: utf-8 -*-

import wx


class DialogTester:
    """
    Класс, используемый для тестирования GUI (диалогов)
    """
    def __init__(self):
        # Список кортежей: (функция, *args, **kwargs),
        # Функции нужно вызывать при попытке вызова
        # метода ShowModal() при использовании класса TestedDialog
        # Если список пуст, вызывается обычный ShowModal() для пользователя
        # Функция должна принимать один параметр - ссылку на диалог,
        # для которого вызывается ShowModal()
        # Функция должна возвращать значение, взвращаемое методом ShowModal()
        self._dialogActions = []

    def append(self, func, *args, **kwargs):
        '''
        Append function to queue.
        Function signature:
            def func(dialog, *args, **kwags):
        '''
        self._dialogActions.append((func, args, kwargs))

    def clear(self):
        self._dialogActions = []

    def appendOk(self):
        """
        Метод добавляет в _dialogActions функцию,
        которая только возвращает wx.ID_OK
        """
        self.append(returnResult, wx.ID_OK)

    def appendCancel(self):
        """
        Метод добавляет в _dialogActions функцию,
        которая только возвращает wx.ID_CANCEL
        """
        self.append(returnResult, wx.ID_CANCEL)

    def appendYes(self):
        """
        Метод добавляет в _dialogActions функцию,
        которая только возвращает wx.YES
        """
        self.append(returnResult, wx.YES)

    def appendNo(self):
        """
        Метод добавляет в _dialogActions функцию,
        которая только возвращает wx.NO
        """
        self.append(returnResult, wx.NO)

    def appendError(self):
        self.append(error)

    def pop(self):
        """
        Возвращает None, если список функций пуст или первый элемент в списке,
        если он есть
        """
        if len(self._dialogActions) == 0:
            return (None, None, None)

        return self._dialogActions.pop(0)

    @property
    def count(self):
        return len(self._dialogActions)

    def runNext(self, dialog):
        result = None
        while result is None and self.count != 0:
            func, args, kwargs = self.pop()
            result = func(dialog, *args, **kwargs)

        return result


def returnResult(dialog, result):
    return result


def error(dialog):
    assert False


def getButtonId(dialog, button_name: str):
    """
    Returns button id for clicking in the dialog
    button_name - button member name in dialog
    """
    return getattr(dialog, button_name).GetId()


class TesterInterface:
    def __init__(self):
        self.dialogTester = DialogTester()


# TestedDialog использует эту переменную
Tester = TesterInterface()
