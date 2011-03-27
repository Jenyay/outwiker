#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from parser.wikiparser import Parser
from parser.commandinclude import IncludeCommand
from parser.commandchildlist import ChildListCommand
from parser.commandbloggers import LjUserCommand, LjCommunityCommand

class ParserFactory (object):
	"""
	Класс, создающий википарсер и добавляющий в него нужные команды
	"""
	def __init__ (self):
		# Список типов команд. Экземпляры команд создаются при заполнении командами парсера
		self.commands = [IncludeCommand, ChildListCommand, LjUserCommand, LjCommunityCommand]


	def make (self, page, config):
		"""
		Создать парсер
		page - страница, для которой создается парсер,
		config - экземпляр класса, хранящий настройки
		"""
		parser = Parser (page, config)
		self._addCommands (parser)
		return parser


	def appendCommand (self, commandType):
		"""
		Добавить тип команды
		"""
		self.commands.append (commandType)


	def _addCommands (self, parser):
		"""
		Добавить команды из self.commands в парсер
		"""
		for command in self.commands:
			parser.addCommand (command (parser))
