#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class PluginsLoader (object):
	"""
	Класс для загрузки плагинов
	"""
	def __init__ (self):
		self.__plugins = []

		# Пути, где ищутся плагины
		self.__dirlist = []


	def load (self, dirlist):
		pass


	def __len__ (self):
		return len (self.__plugins)


	def __item__ (self, index):
		return self.__plugins[index]
