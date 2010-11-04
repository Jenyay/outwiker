#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Классы для взаимодействия конфига и GUI
"""

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
