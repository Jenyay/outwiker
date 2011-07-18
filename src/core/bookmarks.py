#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ConfigParser

from core.application import Application

class Bookmarks (object):
	"""
	Класс, хранящий избранные страницы внутри вики
	"""
	def __init__ (self, wikiroot, config):
		"""
		wikiroot -- корень вики
		config -- экземпляр класса Config, который будет хранить настройки
		"""
		self._config = config
		self.root = wikiroot
		self.configSection = u"Bookmarks"
		self.configOptionTemplate = u"bookmark_%d"

		# Страницы в закладках
		self.__pages = self._load()

		Application.onPageRemove += self.onPageRemove
		wikiroot.onPageRename += self.onPageRename

	
	def onPageRemove (self, page):
		"""
		Обработчик события при удалении страниц
		"""
		# Если удаляемая страница в закладках, то уберем ее оттуда
		if self.pageMarked (page):
			self.remove (page)
	

	def onPageRename (self, page, oldSubpath):
		#if oldSubpath in self.__pages:
			#self.__pages[self.__pages.index (oldSubpath)] = page.subpath

		for n in range (len (self.__pages)):
			subpath = self.__pages[n]
			if subpath.startswith (oldSubpath):
				self.__pages[n] = subpath.replace (oldSubpath, page.subpath, 1)


	def _load (self):
		if not self._config.has_section (self.configSection):
			return []

		result = []
		index = 0
		try:
			while (1):
				option = self.configOptionTemplate % index
				subpath = self._config.get (self.configSection, option)
				result.append (subpath)
				index += 1
		except ConfigParser.NoOptionError:
			pass

		return result

	
	def __len__ (self):
		return len (self.__pages)


	def __getitem__ (self, index):
		subpath = self.__pages[index]
		return self.root[subpath]


	def add (self, page):
		if page.subpath in self.__pages:
			return

		self.__pages.append (page.subpath)
		self.save()
		Application.onBookmarksChanged (self)
	

	def save (self):
		self._config.remove_section (self.configSection)

		for n in range (len (self.__pages)):
			option = self.configOptionTemplate % n
			self._config.set (self.configSection, option, self.__pages[n])


	def remove (self, page):
		self.__pages.remove (page.subpath)
		Application.onBookmarksChanged (self)
		self.save()
	

	def pageMarked (self, page):
		"""
		Узнать находится ли страница в избранном
		"""
		return page.subpath in self.__pages
