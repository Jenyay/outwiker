#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class PluginTestInvalid2 (object):
	"""
	Плагин с ошибкой - нет свойства description
	"""
	def __init__ (self, application, plugindir):
		"""
		application - экземпляр класса core.application.ApplicationParams
		plugindir - путь, откуда загружен плагин	
		"""
		self.application = application


	#############################################
	# Свойства, которые необходимо определить
	#############################################

	@property
	def name (self):
		return u"TestInvalid2"

	
	@property
	def version (self):
		return u"0.1"

	#############################################
