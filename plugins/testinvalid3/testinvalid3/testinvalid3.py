#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class PluginTestInvalid3 (object):
	"""
	Плагин с ошибкой - нет свойства version
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
		return u"TestInvalid3"

	
	@property
	def description (self):
		return _(u"This plugin is empty")


	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		pass

	#############################################
