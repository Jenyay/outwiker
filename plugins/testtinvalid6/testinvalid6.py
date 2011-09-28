#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class PluginTestInvalid6 (object):
	"""
	Плагин с ошибкой - нет метода destroy
	"""
	def __init__ (self, application):
		"""
		application - экземпляр класса core.application.ApplicationParams
		"""
		self.application = application


	#############################################
	# Свойства, которые необходимо определить
	#############################################

	@property
	def name (self):
		return u"TestEmpty1"

	
	@property
	def description (self):
		return _(u"This plugin is empty")


	@property
	def version (self):
		return u"0.1"

	#############################################
