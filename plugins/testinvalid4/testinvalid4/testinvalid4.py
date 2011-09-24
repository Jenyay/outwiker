#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class PluginTestInvalid4 (object):
	"""
	Плагин с ошибкой. В конструкторе возникает исключение
	"""
	def __init__ (self, application, plugindir):
		"""
		application - экземпляр класса core.application.ApplicationParams
		plugindir - путь, откуда загружен плагин
		"""
		self.application = application
		raise IOError


	#############################################
	# Свойства, которые необходимо определить
	#############################################

	@property
	def name (self):
		return u"TestInvalid4"

	
	@property
	def description (self):
		return _(u"This plugin is empty")


	@property
	def version (self):
		return u"0.1"

	#############################################
