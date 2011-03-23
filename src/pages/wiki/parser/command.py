#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

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
