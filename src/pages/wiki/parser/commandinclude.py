#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import cgi

from command import Command
from core.tree import RootWikiPage

class IncludeCommand (Command):
	"""
	Команда для вставки в текст страницы текста прикрепленного файла
	Синтаксис: (:include Attach:fname [params...] :)
	params - необязательные параметры:
		encoding="xxx" - указывает кодировку прикрепленного файла
		htmlescape - заменить символы <, > и т.п. на их HTML-аналоги (&lt;, &gt; и т.п.)
		wikiparse - содержимое прикрепленного файла предварительно нужно пропустить через википарсер
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
		return u"include"


	def execute (self, params, content):
		"""
		Запустить команду на выполнение. 
		Метод возвращает текст, который будет вставлен на место команды в вики-нотации
		"""
		(path, params_tail) = self._getAttach (params)
		if path == None:
			return u""

		params_dict = Command.parseParams (params_tail)
		encoding = self._getEncoding (params_dict)

		try:
			with open (path) as fp:
				# Почему-то в конце всегда оказывается перевод строки
				text = unicode (fp.read (), encoding).rstrip()
		except IOError:
			return _(u"<B>Can't open file %s</B>" % path)
		except ValueError:
			return _(u"<B>Encoding error in file %s</B>" % os.path.basename (path) )
		except TypeError:
			return _(u"<B>Encoding error in file %s</B>" % os.path.basename (path) )

		return self._postprocessText (text, params_dict)


	def _postprocessText (self, text, params_dict):
		"""
		Выполнить манипуляции согласно настройкам с прочитанным текстом
		"""
		result = text

		if "htmlescape" in params_dict:
			result = cgi.escape (text)

		if "wikiparse" in params_dict:
			result = self.parser.parseWikiMarkup (result)

		return result


	def _getEncoding (self, params_dict):
		encoding = u"utf8"
		if "encoding" in params_dict:
			encoding = params_dict["encoding"]

		return encoding



	def _getAttach (self, params):
		"""
		Возвращает имя прикрепленного файла, который хотим вставить на страницу и хвост параметров после имени файла
		"""
		attach_begin = "Attach:"
		params_end = None
		params_tail = params

		# Выделим конец строки после Attach:
		if params.startswith (attach_begin):
			params_end = params[len (attach_begin) :]
		else:
			return (None, params_tail)

		attaches = self.parser.page.attachment
		attaches.sort (IncludeCommand.sortByLength, reverse=True)

		path = None

		for fname in attaches:
			if params_end.startswith (os.path.basename (fname)):
				path = fname
				params_tail = params_end[len (os.path.basename (fname)) :]
				break

		return (path, params_tail)

	
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
