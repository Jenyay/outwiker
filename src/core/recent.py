#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core.application import Application


class RecentWiki (object):
	"""
	Класс для хранения списка последних открытых вики
	"""
	def __init__ (self, config):
		"""
		config -- эксемпляр класса core.config. Туда сохраняем список файлов
		"""
		self._config = config
		self._sectionName = u"RecentWiki"
		self._paramTemplate = u"Path_%d"

		self._load()

		#Application.onWikiOpen += self.onWikiOpen


	def onWikiOpen (self, wikiroot):
		if wikiroot != None and not wikiroot.readonly:
			self.add (wikiroot.path)

	
	def _load (self):
		# Сохраненные пути
		self._recentes = []

		try:
			for n in range (self.maxlen):
				param = self._paramTemplate % (n + 1)
				path = self._config.get (self._sectionName, param)

				self._recentes.append (path)
		except:
			pass


	def _save (self):
		for n in range (len (self._recentes) ):
			param = self._paramTemplate % (n + 1)
			self._config.set (self._sectionName, param, self._recentes[n])


	def add (self, path):
		if path in self._recentes:
			self._recentes.remove (path)

		self._recentes.insert (0, path)

		if len (self._recentes) > self.maxlen:
			del self._recentes[self.maxlen:]

		self._save()

	
	def __len__ (self):
		return len (self._recentes)


	def __getitem__ (self, index):
		return self._recentes[index]


	@property
	def maxlen (self):
		try:
			_maxlen = self._config.getint (self._sectionName, "maxcount")
		except:
			_maxlen = 5

		return _maxlen




