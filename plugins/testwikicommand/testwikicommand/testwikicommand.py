#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .commandtest import TestCommand

class PluginTestWikiCommand (object):
	"""
	Плагин, добавляющий обработку команды TestCommand в википарсер
	"""
	def __init__ (self, application):
		"""
		application - экземпляр класса core.application.ApplicationParams
		"""
		self.__application = application

		self.__application.onWikiParserPrepare += self.__onWikiParserPrepare


	def __onWikiParserPrepare (self, parser):
		parser.addCommand (TestCommand (parser))


	#############################################
	# Свойства, которые необходимо определить
	#############################################

	@property
	def name (self):
		return u"TestWikiCommand"

	
	@property
	def description (self):
		return _(u"Add command (:test:) in wiki parser")


	@property
	def version (self):
		return u"0.1"


	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		self.__application.onWikiParserPrepare -= self.__onWikiParserPrepare

	#############################################
