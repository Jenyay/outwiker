#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class Plugin (object):
	"""
	Базовый класс для плагинов
	"""
	__metaclass__ = ABCMeta

	def __init__ (self, application):
		self._application = application


	###################################################
	# Свойства и методы, которые необходимо определить
	###################################################

	@abstractproperty
	def name (self):
		pass

	
	@abstractproperty
	def description (self):
		pass


	@abstractproperty
	def version (self):
		pass


	@abstractmethod
	def initialize (self):
		"""
		Этот метод вызывается, когда плагин прошел все проверки.
		Именно здесь плагин может начинать влиять на программу
		"""
		pass


	@abstractmethod
	def destroy (self):
		pass

	#############################################
