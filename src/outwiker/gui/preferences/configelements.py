#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Классы для взаимодействия конфига и GUI
"""
import wx

class StringElement (object):
    def __init__ (self, option, control):
        """
        Элемент для строковой настрйоки.
        Элемент управления - TextCtrl
        option - опция из core.config
        defaultValue - значение по умолчанию
        """
        self.option = option
        self.control = control
        self._updateGUI()


    def isValueChanged (self):
        """
        Изменилось ли значение в интерфейсном элементе
        """
        return self._getGuiValue() != self.option.value


    def save (self):
        self.option.value = self._getGuiValue()


    def _getGuiValue (self):
        """
        Получить значение из интерфейстного элемента
        В производных классах этот метод переопределяется
        """
        return self.control.GetValue()


    def _updateGUI (self):
        """
        Обновить интерфейсный элемент. В производных классах этот метод переопределяется
        """
        self.control.SetValue (self.option.value)

    

class BooleanElement (StringElement):
    """
    Булевская настройка.
    Элемент управления - wx.CheckBox
    """
    def __init__ (self, option, control):
        StringElement.__init__ (self, option, control)


    def _getGuiValue (self):
        """
        Получить значение из интерфейстного элемента
        В производных классах этот метод переопределяется
        """
        return self.control.IsChecked()



class IntegerElement (StringElement):
    """
    Настройка для целых чисел.
    Элемент управления - wx.SpinCtrl
    """
    def __init__ (self, option, control, minValue, maxValue):
        StringElement.__init__ (self, option, control)
        self.control.SetRange (minValue, maxValue)


class FontElement (object):
    """
    Настройка для выбра шрифта
    Элемент управления - wx.FontPickerCtrl
    """
    def __init__ (self, option, control):
        self.option = option
        self.control = control
        self._updateGUI()


    def isValueChanged (self):
        """
        Изменилось ли значение в интерфейсном элементе
        """
        # Будем считать, что значение изменяется всегда. Если что, потом доделаю честную проверку
        return True


    def save (self):
        newFont = self.control.GetSelectedFont()
        self.option.size.value = newFont.GetPointSize()
        self.option.faceName.value = newFont.GetFaceName()
        self.option.bold.value = newFont.GetWeight() == wx.FONTWEIGHT_BOLD
        self.option.italic.value = newFont.GetStyle() == wx.FONTSTYLE_ITALIC


    def _updateGUI (self):
        """
        Обновить интерфейсный элемент. В производных классах этот метод переопределяется
        """
        fontSize = self.option.size.value
        fontFaceName = self.option.faceName.value
        fontIsBold = self.option.bold.value
        fontIsItalic = self.option.italic.value

        font = wx.Font (fontSize, wx.FONTFAMILY_DEFAULT, 
                wx.FONTSTYLE_ITALIC if fontIsItalic else wx.FONTSTYLE_NORMAL, 
                wx.FONTWEIGHT_BOLD if fontIsBold else wx.FONTWEIGHT_NORMAL, 
                False,
                fontFaceName,
                wx.FONTENCODING_DEFAULT)

        self.control.SetSelectedFont (font)
