#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin



class PluginTestInvalid2 (Plugin):
	"""
	Плагин с ошибкой - нет свойства description
	"""
	def __init__ (self, application):
		"""
		application - экземпляр класса core.application.ApplicationParams
		"""
		Plugin.__init__ (self, application)


	#############################################
	# Свойства, которые необходимо определить
	#############################################

	def initialize(self):
		pass


	@property
	def name (self):
		return u"TestInvalid2"

	
	@property
	def version (self):
		return u"0.1"


	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		pass

	#############################################
