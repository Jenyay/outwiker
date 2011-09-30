#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import re

class Command (object):
	"""
	Абстрактный базовый класс для команд.
	"""
	__metaclass__ = ABCMeta

	def __init__ (self, parser):
		"""
		parser - экземпляр парсера
		"""
		self.parser = parser

	
	@abstractproperty
	def name (self):
		"""
		Возвращает имя команды, которую обрабатывает класс
		"""
		pass


	@abstractmethod
	def execute (self, params, content):
		"""
		Запустить команду на выполнение. 
		Метод возвращает текст, который будет вставлен на место команды в вики-нотации
		"""
		pass


	@staticmethod
	def parseParams (params):
		"""
		Разобрать строку params на составные части ключ - значение.
		Пример строки param:
			Параметр1 Параметр2 = 111 Параметр3 = " бла бла бла" Параметр4 Параметр5="111" Параметр5=' 222 ' Параметр7 = " проверка 'бла бла бла' проверка" Параметр8 = ' проверка "bla-bla-bla" тест '
		"""
		pattern = ur"""((?P<name>\w+)
(\s*=\s*(?P<param>(\w+)|((?P<quote>["']).*?(?P=quote)) ) )?\s*)"""
		
		result = {}

		regex = re.compile (pattern, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE | re.UNICODE)
		matches = regex.finditer (params)

		for match in matches:
			name = match.group ("name")
			param = match.group ("param")
			if param == None:
				param = u""

			result[name] = Command.removeQuotes (param)

		return result


	@staticmethod
	def removeQuotes (text):
		"""
		Удалить начальные и конечные кавычки, которые остались после разбора параметров
		"""
		if (len (text) > 0 and
				(text[0] == text[-1] == "'" or
				text[0] == text[-1] == '"') ):
				return text[1:-1]

		return text

