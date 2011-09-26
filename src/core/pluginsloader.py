#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import sys

from core.application import Application


class PluginsLoader (object):
	"""
	Класс для загрузки плагинов
	"""
	def __init__ (self):
		self.__plugins = []

		# Пути, где ищутся плагины
		self.__dirlist = []

		# Имя классов плагинов должно начинаться с "Plugins"
		self.__pluginsStartName = "Plugin"


	def load (self, dirlist):
		assert dirlist != None

		for currentDir in dirlist:
			dirPackets = os.listdir (currentDir)

			# Добавить путь до currenddir в sys.path
			fullpath = os.path.abspath (currentDir)
			if fullpath not in sys.path:
				sys.path.insert (0, fullpath)

			# Все поддиректории попытаемся открыть как пакеты
			modules = self.__importModules (currentDir, dirPackets)

			# Загрузим классы плагинов из модулей
			self.__loadPlugins (modules)


	def __importModules (self, baseDir, dirPackagesList):
		"""
		Попытаться импортировать пакеты
		baseDir - директория, где расположены пакеты
		dirPackagesList - список директорий, возможно являющихся пакетами
		"""
		assert dirPackagesList != None

		extension = ".py"

		modules = []

		for packageDir in dirPackagesList:
			packagePath = os.path.join (baseDir, packageDir)

			# Проверить, что это директория
			if os.path.isdir (packagePath):
				# Переберем все файлы внутри packagePath и попытаемся их импортировать
				for filename in os.listdir (packagePath):
					if filename.endswith (extension) and filename != "__init__.py":
						try:
							# Попытаться импортировать модуль
							modulename = packageDir + "." + filename[: -len (extension)]
							package = __import__ (modulename)
						except ImportError:
							continue

						modules.append (getattr (package, filename[: -len (extension)]) )

		return modules


	def __loadPlugins (self, modules):
		assert modules != None

		for module in modules:
			for name in dir (module):
				if name.startswith (self.__pluginsStartName):
					obj = getattr (module, name)
					if not issubclass (obj, object):
						continue
					
					try:
						plugin = obj (Application, os.path.dirname (module.__file__) )
					except BaseException:
						continue

					if self.__testPlugin (plugin):
						self.__plugins.append (plugin)

	
	def __testPlugin (self, plugin):
		"""
		Проверка на то, что плагин удовлетворяет всем накладываемым требованиям - имеет все нужные свойства
		"""
		try:
			plugin.name
			plugin.version
			plugin.description
		except AttributeError:
			return False

		return True


	def __len__ (self):
		return len (self.__plugins)


	def __getitem__ (self, index):
		return self.__plugins[index]
