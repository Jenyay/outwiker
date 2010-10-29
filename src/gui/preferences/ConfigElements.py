#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Классы для взаимодействия конфига и Гуя
"""

class StringOptions (object):
	def __init__ (self, section, param, config, control, defaultValue):
		"""
		section - секция для параметра конфига
		param - имя параметра конфига
		config - экземпляр класса core.Config
		control - экземпляр интерфейсного элемента. Для текстовых параметров - wx.TextCtrl
		defaultValue - значение по умолчанию
		"""
		self.section = section
		self.param = param
		self.defaultValue = defaultValue
		self.config = config
		self.control = control

		# Указатель на последнее возникшее исключение
		# Т.к. как правило исключения игнорируются, то это поле используется для отладкиы
		self.error = None

		self.loadParam (config)


	def loadParam (self, config):
		try:
			self.value = self._getValue()
		except Exception as e:
			self.error = e
			self.value = self.defaultValue

		self._updateGUI()


	def isValueChanged (self):
		"""
		Изменилось ли значение в интерфейсном элементе
		"""
		return self._getGuiValue() != self.value


	def save (self):
		if self.isValueChanged():
			self._saveValue()


	def _getGuiValue (self):
		"""
		Получить значение из интерфейстного элемента
		В производных классах этот метод переопределяется
		"""
		return self.control.GetValue()


	def _getValue (self):
		"""
		Получить значение. В производных классах этот метод переопределяется
		"""
		return self.config.get (self.section, self.param)


	def _updateGUI (self):
		"""
		Обновить интерфейсный элемент. В производных классах этот метод переопределяется
		"""
		self.control.SetValue (self.value)

	
	def _saveValue (self):
		self.config.set (self.section, self.param, self._getGuiValue() )
	

class BooleanOptions (StringOptions):
	"""
	Булевская настройка.
	Элемент управления - wx.CheckBox
	"""
	def __init__ (self, section, param, config, control, defaultValue):
		StringOptions.__init__ (self, section, param, config, control, defaultValue)


	def _getGuiValue (self):
		"""
		Получить значение из интерфейстного элемента
		В производных классах этот метод переопределяется
		"""
		return self.control.IsChecked()


	def _getValue (self):
		"""
		Получить значение. В производных классах этот метод переопределяется
		"""
		return self.config.getbool (self.section, self.param)


class IntegerOptions (StringOptions):
	"""
	Настройка для целых чисел.
	Элемент управления - wx.SpinCtrl
	"""
	def __init__ (self, section, param, config, control, defaultValue, minValue, maxValue):
		StringOptions.__init__ (self, section, param, config, control, defaultValue)
		self.control.SetRange (minValue, maxValue)


	def _getValue (self):
		"""
		Получить значение. В производных классах этот метод переопределяется
		"""
		return self.config.getint (self.section, self.param)
