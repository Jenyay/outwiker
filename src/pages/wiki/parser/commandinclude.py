#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from command import Command
from core.tree import RootWikiPage

class IncludeCommand (Command):
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
		return u"include"


	def execute (self, params, content):
		"""
		Запустить команду на выполнение. 
		Метод возвращает текст, который будет вставлен на место команды в вики-нотации
		"""
		path = self._getAttach (params)
		if path == None:
			return u""

		try:
			with open (path) as fp:
				text = unicode (fp.read (), "utf8")
		except IOError:
			return _(u"<B>Can't open file %s</B>" % path)
		except UnicodeDecodeError:
			return _(u"<B>UnicodeDecodeError in file %s</B>" % os.path.basename (path) )

		return text


	def _getAttach (self, params):
		"""
		Возвращает имя прикрепленного файла, который хотим вставить на страницу
		"""
		attach_begin = "Attach:"
		params_end = None

		# Выделим конец строки после Attach:
		if params.startswith (attach_begin):
			params_end = params[len (attach_begin) :]
		else:
			return None

		attaches = self.parser.page.attachment
		attaches.sort (IncludeCommand.sortByLength, reverse=True)

		path = None

		for fname in attaches:
			if params_end.startswith (os.path.basename (fname)):
				path = fname
				break

		return path

	
	# TODO: Вынести в отдельный модуль
	@staticmethod
	def sortByLength (fname1, fname2):
		"""
		Функция для сортировки имен по длине имени
		"""
		if len (fname1) > len (fname2):
			return 1
		elif len (fname1) < len (fname2):
			return -1

		return 0
