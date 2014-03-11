#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import sys

from .pluginbase import Plugin
from outwiker.gui.guiconfig import PluginsConfig
from .system import getOS


class PluginsLoader (object):
    """
    Класс для загрузки плагинов
    """
    def __init__ (self, application):
        self.__application = application

        # Словарь с загруженными плагинами
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self.__plugins = {}

        # Словарь с плагинами, которые были отключены пользователем
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self.__disabledPlugins = {}

        # Пути, где ищутся плагины
        self.__dirlist = []

        # Имя классов плагинов должно начинаться с "Plugins"
        self.__pluginsStartName = "Plugin"

        # Установить в False, если не нужно выводить ошибки (например, в тестах)
        self.enableOutput = True


    def _print (self, text):
        if self.enableOutput:
            print text


    @property
    def disabledPlugins (self):
        """
        Возвращает список отключенных плагинов
        """
        return self.__disabledPlugins


    def updateDisableList (self):
        """
        Обновление состояния плагинов. Одни отключить, другие включить
        """
        options = PluginsConfig (self.__application.config)

        # Пройтись по включенным плагинам и отключить те,
        # что попали в черный список
        self.__disableEnabledPlugins (options.disabledPlugins.value)

        # Пройтись по отключенным плагинам и включить те, 
        # что не попали в "черный список"
        self.__enableDisabledPlugins (options.disabledPlugins.value)


    def __disableEnabledPlugins (self, disableList):
        """
        Отключить загруженные плагины, попавшие в "черный список" (disableList)
        """
        for pluginname in disableList:
            if pluginname in self.__plugins.keys():
                self.__plugins[pluginname].destroy()

                assert pluginname not in self.__disabledPlugins
                self.__disabledPlugins[pluginname] = self.__plugins[pluginname]
                del self.__plugins[pluginname]


    def __enableDisabledPlugins (self, disableList):
        """
        Включить отключенные плагины, если их больше нет в "черном списке"
        """
        for plugin in self.__disabledPlugins.values():
            if plugin.name not in disableList:
                plugin.initialize ()

                assert plugin.name not in self.__plugins
                self.__plugins[plugin.name] = plugin

                del self.__disabledPlugins[plugin.name]


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
                # TODO: Разобраться с Unicode в следующей строке. 
                # Иногда выскакивает предупреждение:
                # ...\outwiker\core\pluginsloader.py:41: UnicodeWarning: Unicode equal comparison failed to convert both arguments to Unicode - interpreting them as being unequal

                syspath = [unicode (item, getOS().filesEncoding) 
                        if type (item) != unicode else item 
                        for item in sys.path]

                if fullpath not in syspath:
                    sys.path.insert (0, fullpath)

                # Все поддиректории попытаемся открыть как пакеты
                modules = self.__importModules (currentDir, dirPackets)

                # Загрузим классы плагинов из модулей
                self.__loadPlugins (modules)


    def clear (self):
        """
        Уничтожить все загруженные плагины
        """
        map (lambda plugin: plugin.destroy(), self.__plugins.values())
        self.__plugins = {}


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

            # Флаг, обозначающий, что удалось импортировать хотя бы один модуль
            success = False

            # Список строк, описывающий возникшие ошибки во время импортирования
            # Выводятся только если не удалось импортировать ни одного модуля
            errors = []

            # Проверить, что это директория
            if os.path.isdir (packagePath):
                # Переберем все файлы внутри packagePath 
                # и попытаемся их импортировать
                for fileName in os.listdir (packagePath):
                    try:
                        module = self._importSingleModule (packageName, fileName)
                        if module != None:
                            modules.append (module)
                            success = True
                    except ImportError as e:
                        errors.append ("*** Plugin loading error ***\n{package}/{fileName}\n{error}".format (
                            package = packageName, 
                            fileName = fileName,
                            error=str(e) ))

            if not success:
                self._print (u"\n\n".join (errors) + u"\n")

        return modules


    def _importSingleModule (self, packageName, fileName):
        """
        Импортировать один модуль по имени пакета и файла с модулем
        """
        extension = ".py"
        result = None

        # Проверим, что файл может быть модулем
        if fileName.endswith (extension) and fileName != "__init__.py":
            modulename = fileName[: -len (extension)]
            # Попытаться импортировать модуль
            package = __import__ (packageName + "." + modulename)
            result = getattr (package, modulename)

        return result


    def __loadPlugins (self, modules):
        """
        Найти классы плагинов и создать их экземпляры
        """
        assert modules != None

        options = PluginsConfig (self.__application.config)

        for module in modules:
            for name in dir (module):
                self.__createObject (module, 
                        name, 
                        options.disabledPlugins.value)


    def __createObject (self, module, name, disabledPlugins):
        """
        Попытаться загрузить класс, возможно, это плагин

        module - модуль, откуда загружается класс
        name - имя класса потенциального плагина
        """
        if name.startswith (self.__pluginsStartName):
            obj = getattr (module, name)
            if obj == Plugin or not issubclass (obj, Plugin):
                return

            try:
                plugin = obj (self.__application)
            except BaseException as e:
                self._print ("*** Plugin loading error ***\n{classname}\n{error}\n".format (
                    classname=name, 
                    error=str(e) ) )
                return

            if not self.__isNewPlugin (plugin.name):
                return

            if plugin.name not in disabledPlugins:
                plugin.initialize()
                self.__plugins[plugin.name] = plugin
            else:
                self.__disabledPlugins[plugin.name] = plugin


    def __isNewPlugin (self, pluginname):
        """
        Проверка того, что плагин с таким именем еще не был загружен
        newplugin - плагин, который надо проверить
        """
        return (pluginname not in self.__plugins and 
                pluginname not in self.__disabledPlugins)


    def __len__ (self):
        return len (self.__plugins)


    def __getitem__ (self, pluginname):
        return self.__plugins[pluginname]


    def __iter__ (self):
        return self.__plugins.itervalues()
