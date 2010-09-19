#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

	
	def _load (self):
		try:
			self._maxlen = self._config.getint (self._sectionName, "maxcount")
		except:
			self._maxlen = 5

		# Сохраненные пути
		self._pathes = []

		try:
			for n in range (self._maxlen):
				param = self._paramTemplate % (n + 1)
				path = self._config.get (self._sectionName, param)

				self._pathes.append (path)
		except:
			pass


	def _save (self):
		#self._config.remove_section (self._sectionName)
		self._config.set (self._sectionName, "maxcount", self._maxlen)

		for n in range (len (self._pathes) ):
			param = self._paramTemplate % (n + 1)
			self._config.set (self._sectionName, param, self._pathes[n])


	def add (self, path):
		if path in self._pathes:
			self._pathes.remove (path)

		self._pathes.insert (0, path)

		if len (self._pathes) > self._maxlen:
			del self._pathes[self._maxlen:]
			#print self._pathes


		self._save()

	
	def __len__ (self):
		return len (self._pathes)


	def __getitem__ (self, index):
		return self._pathes[index]


	@property
	def maxlen (self):
		return self._maxlen




