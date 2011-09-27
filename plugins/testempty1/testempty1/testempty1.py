#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class PluginTestEmpty1 (object):
	def __init__ (self, application):
		"""
		application - экземпляр класса core.application.ApplicationParams
		"""
		self.__application = application


	@property
	def application (self):
		return self.__application


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
