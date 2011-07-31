#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

class UriIdentifierWebKit (object):
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

		href_clear = self.__removeFileProtokol (href)

		page = self.__findWikiPage (href_clear)
		filename = self.__findFile (href_clear)

		return (None, page, filename)


	def __removeFileProtokol (self, href):
		"""
		Так как WebKit к адресу без протокола прибавляет file://, то избавимся от этой надписи
		"""
		fileprotocol = u"file://"
		if href.startswith (fileprotocol):
			return href[len (fileprotocol): ]

		return href


	def __findWikiPage (self, href):
		"""
		Попытка найти страницу вики, если ссылка, на которую щелкнули не интернетная (http, ftp, mailto)
		"""
		assert self._currentPage != None

		newSelectedPage = None

		if href.startswith (self._currentPage.path):
			href = href[len (self._currentPage.path) + 1: ]

		if href[0] == "/":
			# Поиск страниц осуществляем только с корня
			newSelectedPage = self._currentPage.root[href[1:] ]
		else:
			# Сначала попробуем найти вложенные страницы с таким href
			newSelectedPage = self._currentPage[href]

			if newSelectedPage == None:
				# Если страница не найдена, попробуем поискать, начиная с корня
				newSelectedPage = self._currentPage.root[href]

		return newSelectedPage


	def _isUrl (self, href):
		return href.lower().startswith ("http://") or \
				href.lower().startswith ("https://") or \
				href.lower().startswith ("ftp://") or \
				href.lower().startswith ("mailto:")


	def __findFile (self, href):
		if os.path.exists (href):
			return href
