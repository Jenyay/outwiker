#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin


class PluginTestEmpty2 (Plugin):
	def __init__ (self, application):
		"""
		application - экземпляр класса core.application.ApplicationParams
		"""
		Plugin.__init__ (self, application)


	###################################################
	# Свойства и методы, которые необходимо определить
	###################################################

	@property
	def name (self):
		return u"TestEmpty2"

	
	@property
	def description (self):
		return _(u"This plugin is empty")


	@property
	def version (self):
		return u"0.1"


	def initialize(self):
		pass



	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		pass

	#############################################
