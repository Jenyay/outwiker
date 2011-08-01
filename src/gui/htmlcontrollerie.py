#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path


class UriIdentifierIE (object):
	"""
	Класс для идентификации ссылок. На что ссылки
	"""
	def __init__ (self, currentpage):
		self._currentPage = currentpage


	def identify (self, href):
		"""
		Определить тип ссылки и вернуть кортеж (url, page, filename)
		"""
		#print href
		if self._isUrl (href):
			return (href, None, None)

		page = self.__findWikiPage (href)
		filename = self.__findFile (href)

		return (None, page, filename)


	def __findWikiPage (self, subpath):
		"""
		Попытка найти страницу вики, если ссылка, на которую щелкнули не интернетная (http, ftp, mailto)
		"""
		assert self._currentPage != None

		newSelectedPage = None

		if subpath.startswith (self._currentPage.path):
			subpath = subpath[len (self._currentPage.path) + 1: ].replace ("\\", "/")
		elif len (subpath) > 1 and subpath[1] == ":":
			subpath = subpath[2:].replace ("\\", "/")
			#print subpath

		if subpath.startswith ("about:"):
			subpath = self.__removeAboutBlank (subpath).replace ("\\", "/")
		
		if len (subpath) > 0 and subpath[0] == "/":
			# Поиск страниц осуществляем только с корня
			newSelectedPage = self._currentPage.root[subpath[1:] ]
		else:
			# Сначала попробуем найти вложенные страницы с таким subpath
			newSelectedPage = self._currentPage[subpath]

			if newSelectedPage == None:
				# Если страница не найдена, попробуем поискать, начиная с корня
				newSelectedPage = self._currentPage.root[subpath]

		return newSelectedPage


	def __findFile (self, href):
		if os.path.exists (href):
			return href


	def _isUrl (self, href):
		return href.lower().startswith ("http://") or \
				href.lower().startswith ("https://") or \
				href.lower().startswith ("ftp://") or \
				href.lower().startswith ("mailto:")


	def __removeAboutBlank (self, href):
		"""
		Удалить about: и about:blank из начала адреса
		"""
		about_full = u"about:blank"
		about_short = u"about:"

		result = href
		if result.startswith (about_full):
			result = result[len (about_full): ]

		elif result.startswith (about_short):
			result = result[len (about_short): ]

		return result

