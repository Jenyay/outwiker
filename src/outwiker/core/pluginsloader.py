#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import sys

from .pluginbase import Plugin


class PluginsLoader (object):
	"""
	Класс для загрузки плагинов
	"""
	def __init__ (self, application):
		self.__application = application

		self.__plugins = []

		# Пути, где ищутся плагины
		self.__dirlist = []

		# Имя классов плагинов должно начинаться с "Plugins"
		self.__pluginsStartName = "Plugin"


	def load (self, dirlist):
		"""
		Загрузить плагины из указанных директорий.
		Каждый вызов метода load() добавляет плагины в список загруженных плагинов, не очищая его
		dirlist - список директорий, где могут располагаться плагины. Каждый плагин расположен в своей поддиректории
		"""
		assert dirlist != None

		for currentDir in dirlist:
			if os.path.exists (currentDir):
				dirPackets = os.listdir (currentDir)

				# Добавить путь до currentDir в sys.path
				fullpath = os.path.abspath (currentDir)
				if fullpath not in sys.path:
					sys.path.insert (0, fullpath)

				# Все поддиректории попытаемся открыть как пакеты
				modules = self.__importModules (currentDir, dirPackets)

				# Загрузим классы плагинов из модулей
				self.__loadPlugins (modules)


	def clear (self):
		"""
		Уничтожить все загруженные плагины
		"""
		for plugin in self.__plugins:
			plugin.destroy()

		self.__plugins = []


	def __importModules (self, baseDir, dirPackagesList):
		"""
		Попытаться импортировать пакеты
		baseDir - директория, где расположены пакеты
		dirPackagesList - список директорий (только имена директорий), возможно являющихся пакетами
		"""
		assert dirPackagesList != None

		modules = []

		for packageName in dirPackagesList:
			packagePath = os.path.join (baseDir, packageName)

			# Проверить, что это директория
			if os.path.isdir (packagePath):
				# Переберем все файлы внутри packagePath и попытаемся их импортировать
				for fileName in os.listdir (packagePath):
					module = self.__importSingleModule (packageName, fileName)
					if module != None:
						modules.append (module)

		return modules


	def __importSingleModule (self, packageName, fileName):
		"""
		Импортировать один модуль по имени пакета и файла с модулем
		"""
		extension = ".py"

		# Проверим, что файл может быть модулем
		if fileName.endswith (extension) and fileName != "__init__.py":
			modulename = fileName[: -len (extension)]
			try:
				# Попытаться импортировать модуль
				package = __import__ (packageName + "." + modulename)
				return getattr (package, modulename)
			except ImportError:
				# Ну не шмогли импортировать, тогда этот модуль игнорируем
				pass

		return None


	def __loadPlugins (self, modules):
		"""
		Найти классы плагинов и создать их экземпляры
		"""
		assert modules != None

		for module in modules:
			for name in dir (module):
				if name.startswith (self.__pluginsStartName):
					obj = getattr (module, name)
					if not issubclass (obj, Plugin):
						continue

					try:
						plugin = obj (self.__application)
					except BaseException as e:
						#print str (obj)
						#print e
						continue

					self.__plugins.append (plugin)

	
	def __len__ (self):
		return len (self.__plugins)


	def __getitem__ (self, index):
		return self.__plugins[index]
