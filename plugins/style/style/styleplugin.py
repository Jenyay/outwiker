#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin

from .stylecommand import StyleCommand


class PluginStyle (Plugin):
	"""
	Плагин, добавляющий обработку команды (:style:) в википарсер
	"""
	def __init__ (self, application):
		"""
		application - экземпляр класса core.application.ApplicationParams
		"""
		Plugin.__init__ (self, application)


	def __onWikiParserPrepare (self, parser):
		parser.addCommand (StyleCommand (parser))


	###################################################
	# Свойства и методы, которые необходимо определить
	###################################################

	@property
	def name (self):
		return u"Style"

	
	@property
	def description (self):
		return u"""Add command (:style:) in wiki parser.
Usage:

(:style:)
styles
(:styleend:)
"""


	@property
	def version (self):
		return u"1.0"


	def initialize(self):
		self._application.onWikiParserPrepare += self.__onWikiParserPrepare


	def destroy (self):
		"""
		Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
		"""
		self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

	#############################################
