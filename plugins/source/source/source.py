#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin
from .commandsource import CommandSource


class PluginSourceCommand (Plugin):
	"""
	Плагин, добавляющий обработку команды (:source:) в википарсер
	"""
	def __init__ (self, application):
		"""
		application - экземпляр класса core.application.ApplicationParams
		"""
		Plugin.__init__ (self, application)

		self._application.onWikiParserPrepare += self.__onWikiParserPrepare


	def __onWikiParserPrepare (self, parser):
		parser.addCommand (CommandSource (parser))


	#############################################
	# Свойства, которые необходимо определить
	#############################################

	@property
	def name (self):
		return u"Source"

	
	@property
	def description (self):
		return _(u"Add command (:source:) in wiki parser")


	@property
	def version (self):
		return u"0.1"


	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

	#############################################
