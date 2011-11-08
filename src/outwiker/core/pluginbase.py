#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty
import gettext

from outwiker.core.i18n import getLanguageFromConfig, loadLanguage


class Plugin (object):
	"""
	Базовый класс для плагинов
	"""
	__metaclass__ = ABCMeta

	def __init__ (self, application):
		self._application = application


	def _init_i18n (self, domain, langdir):
		"""
		Инициализация интернационализации
		domain - домен в файлах перевода
		langdir - путь до папки с переводами
		"""
		language = getLanguageFromConfig (self._application.config)
		lang = loadLanguage (language, langdir, domain)
		return lang.ugettext


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
