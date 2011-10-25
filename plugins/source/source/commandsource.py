#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command

class CommandSource (Command):
	"""
	Команда source для оформления исходных текстов программ
	Использование:

	(:source params)
	Текст программы
	(:sourceend:)

	Параметры:
	tabwidth - размер табуляции
	lang - язык программирования (пока не используется)
	"""
	def __init__ (self, parser):
		"""
		parser - экземпляр парсера
		"""
		Command.__init__ (self, parser)

	
	@property
	def name (self):
		"""
		Возвращает имя команды, которую обрабатывает класс
		"""
		return u"source"


	def execute (self, params, content):
		"""
		Запустить команду на выполнение. 
		Оформление исходных текстов
		"""
		params_dict = Command.parseParams (params)

		DEFAULT_TABWIDTH = 4
		PARAM_TABWIDTH = "tabwidth"

		try:
			tabwidth = int (params_dict[PARAM_TABWIDTH]) if PARAM_TABWIDTH in params_dict else DEFAULT_TABWIDTH
		except ValueError:
			tabwidth = DEFAULT_TABWIDTH

		newcontent = content.replace ("\t", " " * tabwidth)

		result = u"<CODE><PRE>{content}</PRE></CODE>".format (content=newcontent)

		return result
