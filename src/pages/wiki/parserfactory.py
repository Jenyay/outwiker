#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from parser.wikiparser import Parser
from parser.commandinclude import IncludeCommand
from parser.commandchildlist import ChildListCommand
from parser.commandattachlist import AttachListCommand
from parser.commandbloggers import LjUserCommand, LjCommunityCommand
from core.application import Application


class ParserFactory (object):
	"""
	Класс, создающий википарсер и добавляющий в него нужные команды
	"""
	def __init__ (self):
		# Список типов команд. Экземпляры команд создаются при заполнении командами парсера
		self.__commands = [IncludeCommand, ChildListCommand, LjUserCommand, LjCommunityCommand, AttachListCommand]


	def make (self, page, config):
		"""
		Создать парсер
		page - страница, для которой создается парсер,
		config - экземпляр класса, хранящий настройки
		"""
		parser = Parser (page, config)
		self._addCommands (parser)
		Application.onWikiParserPrepare (parser)

		return parser


	def appendCommand (self, commandType):
		"""
		Добавить тип команды
		"""
		self.__commands.append (commandType)


	def _addCommands (self, parser):
		"""
		Добавить команды из self.__commands в парсер
		"""
		for command in self.__commands:
			parser.addCommand (command (parser))
