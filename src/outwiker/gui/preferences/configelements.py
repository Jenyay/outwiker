# -*- coding: utf-8 -*-
"""
Классы для взаимодействия конфига и GUI
"""

from abc import ABCMeta, abstractmethod

import wx


class BaseElement(metaclass=ABCMeta):
    def __init__(self,
                 option,
                 control: wx.Control):
        """
        option - опция из core.config
        """
        self.option = option
        self.control = control
        self._setGUIValue()

    def isValueChanged(self):
        """
        Изменилось ли значение в интерфейсном элементе
        """
        return self._getGUIValue() != self.option.value

    def save(self):
        self.option.value = self._getGUIValue()

    @abstractmethod
    def _getGUIValue(self):
        """
        Получить значение из интерфейстного элемента
        В производных классах этот метод переопределяется
        """
        pass

    @abstractmethod
    def _setGUIValue(self):
        """
        Обновить интерфейсный элемент.
        В производных классах этот метод переопределяется
        """
        pass


class StringElement (BaseElement):
    def _getGUIValue(self):
        """
        Получить значение из интерфейстного элемента
        В производных классах этот метод переопределяется
        """
        return self.control.GetValue()

    def _setGUIValue(self):
        """
        Обновить интерфейсный элемент.
        В производных классах этот метод переопределяется
        """
        self.control.SetValue(self.option.value)


class BooleanElement (BaseElement):
    """
    Булевская настройка.
    Элемент управления - wx.CheckBox
    """
    def _getGUIValue(self):
        """
        Получить значение из интерфейстного элемента
        В производных классах этот метод переопределяется
        """
        return self.control.IsChecked()

    def _setGUIValue(self):
        """
        Обновить интерфейсный элемент.
        В производных классах этот метод переопределяется
        """
        self.control.SetValue(self.option.value)


class ColourElement (BaseElement):
    """
    Настройка цвета.
    Элемент управления - wx.ColourPickerCtrl
    """
    def _getGUIValue(self):
        """
        Получить значение из интерфейстного элемента
        В производных классах этот метод переопределяется
        """
        return self.control.GetColour().GetAsString(wx.C2S_HTML_SYNTAX)

    def _setGUIValue(self):
        """
        Обновить интерфейсный элемент.
        В производных классах этот метод переопределяется
        """
        self.control.SetColour(self.option.value)


class IntegerElement (BaseElement):
    """
    Настройка для целых чисел.
    Элемент управления - wx.SpinCtrl
    """

    def __init__(self, option, control, minValue, maxValue):
        super().__init__(option, control)
        self.control.SetRange(minValue, maxValue)
        self._setGUIValue()

    def _getGUIValue(self):
        """
        Получить значение из интерфейстного элемента
        В производных классах этот метод переопределяется
        """
        return self.control.GetValue()

    def _setGUIValue(self):
        """
        Обновить интерфейсный элемент.
        В производных классах этот метод переопределяется
        """
        self.control.SetValue(self.option.value)


class FontElement (object):
    """
    Настройка для выбора шрифта
    Элемент управления - wx.FontPickerCtrl
    """

    def __init__(self, option, control):
        self.option = option
        self.control = control
        self._setGUIValue()

    def isValueChanged(self):
        """
        Изменилось ли значение в интерфейсном элементе
        """
        # Будем считать, что значение изменяется всегда.
        # Если что, потом доделаю честную проверку
        return True

    def save(self):
        newFont = self.control.GetSelectedFont()
        self.option.size.value = newFont.GetPointSize()
        self.option.faceName.value = newFont.GetFaceName()
        self.option.bold.value = newFont.GetWeight() == wx.FONTWEIGHT_BOLD
        self.option.italic.value = newFont.GetStyle() == wx.FONTSTYLE_ITALIC

    def _setGUIValue(self):
        """
        Обновить интерфейсный элемент.
        В производных классах этот метод переопределяется
        """
        fontSize = self.option.size.value
        fontFaceName = self.option.faceName.value
        fontIsBold = self.option.bold.value
        fontIsItalic = self.option.italic.value

        font = wx.Font(
            fontSize, wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_ITALIC if fontIsItalic else wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD if fontIsBold else wx.FONTWEIGHT_NORMAL,
            False,
            fontFaceName,
            wx.FONTENCODING_DEFAULT)

        self.control.SetSelectedFont(font)
