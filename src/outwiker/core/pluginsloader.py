# -*- coding: utf-8 -*-

import os
import os.path
import sys
import traceback
import logging

import outwiker.core
import outwiker.gui
import outwiker.pages
import outwiker.actions
import outwiker.utilites
import outwiker.libs

import outwiker.core.packageversion as pv

from outwiker.core.defines import PLUGIN_VERSION_FILE_NAME
from outwiker.core.pluginbase import Plugin, InvalidPlugin
from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.gui.guiconfig import PluginsConfig
from outwiker.utilites.textfile import readTextFile


logger = logging.getLogger('outwiker.core.pluginsloader')


class PluginsLoader (object):
    """
    Класс для загрузки плагинов
    """
    def __init__(self, application):
        self.__application = application

        # Словарь с загруженными плагинами
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self.__plugins = {}

        # Словарь с плагинами, которые были отключены пользователем
        # Ключ - имя плагина
        # Значение - экземпляр плагина
        self.__disabledPlugins = {}

        # The list of the InvalidPlugin instance.
        self.__invalidPlugins = []

        # Пути, где ищутся плагины
        self.__dirlist = []

        # Имя классов плагинов должно начинаться с "Plugins"
        self.__pluginsStartName = "Plugin"

        # Установить в False, если не нужно выводить ошибки
        # (например, в тестах)
        self.enableOutput = True

    def _print(self, text):
        if self.enableOutput:
            logger.error(text)

    @property
    def disabledPlugins(self):
        """
        Возвращает список отключенных плагинов
        """
        return self.__disabledPlugins

    @property
    def invalidPlugins(self):
        return self.__invalidPlugins

    def updateDisableList(self):
        """
        Обновление состояния плагинов. Одни отключить, другие включить
        """
        options = PluginsConfig(self.__application.config)

        # Пройтись по включенным плагинам и отключить те,
        # что попали в черный список
        self.__disableEnabledPlugins(options.disabledPlugins.value)

        # Пройтись по отключенным плагинам и включить те,
        # что не попали в "черный список"
        self.__enableDisabledPlugins(options.disabledPlugins.value)

    def __disableEnabledPlugins(self, disableList):
        """
        Отключить загруженные плагины, попавшие в "черный список" (disableList)
        """
        for pluginname in disableList:
            if pluginname in self.__plugins.keys():
                self.__plugins[pluginname].destroy()

                assert pluginname not in self.__disabledPlugins
                self.__disabledPlugins[pluginname] = self.__plugins[pluginname]
                del self.__plugins[pluginname]

    def __enableDisabledPlugins(self, disableList):
        """
        Включить отключенные плагины, если их больше нет в "черном списке"
        """
        for plugin in list(self.__disabledPlugins.values()):
            if plugin.name not in disableList:
                plugin.initialize()

                assert plugin.name not in self.__plugins
                self.__plugins[plugin.name] = plugin

                del self.__disabledPlugins[plugin.name]

    def load(self, dirlist):
        """
        Загрузить плагины из указанных директорий.
        Каждый вызов метода load() добавляет плагины в список загруженных
            плагинов, не очищая его.
        dirlist - список директорий, где могут располагаться плагины.
            Каждый плагин расположен в своей поддиректории
        """
        assert dirlist is not None

        logger.debug(u'Plugins loading started')

        for currentDir in dirlist:
            if os.path.exists(currentDir):
                dirPackets = sorted(os.listdir(currentDir))

                # Добавить путь до currentDir в sys.path
                fullpath = os.path.abspath(currentDir)

                if fullpath not in sys.path:
                    sys.path.insert(0, fullpath)

                # Все поддиректории попытаемся открыть как пакеты
                self.__importModules(currentDir, dirPackets)

        logger.debug(u'Plugins loading ended')

    def clear(self):
        """
        Уничтожить все загруженные плагины
        """
        [plugin.destroy() for plugin in self.__plugins.values()]
        self.__plugins = {}

    def __loadPluginInfo(self, plugin_fname):
        if not os.path.exists(plugin_fname):
            return None

        xml_content = readTextFile(plugin_fname)
        appinfo = XmlVersionParser().parse(xml_content)
        return appinfo

    def __checkPackageVersions(self, appinfo):
        if appinfo is None:
            return pv.PLUGIN_MUST_BE_UPGRADED

        api_required_version = appinfo.requirements.api_version
        if not api_required_version:
            api_required_version = [(0, 0)]

        return pv.checkVersionAny(outwiker.core.__version__,
                                  api_required_version)

    def __importModules(self, baseDir, dirPackagesList):
        """
        Попытаться импортировать пакеты
        baseDir - директория, где расположены пакеты
        dirPackagesList - список директорий (только имена директорий),
            возможно являющихся пакетами
        """
        assert dirPackagesList is not None

        for packageName in dirPackagesList:
            packagePath = os.path.join(baseDir, packageName)

            # Проверить, что это директория
            if os.path.isdir(packagePath):
                # It may be plugin if __init__.py file exists
                initFile = os.path.join(packagePath, u'__init__.py')
                if not os.path.exists(initFile):
                    continue

                logger.debug(u'Trying to load the plug-in: {}'.format(
                    packageName))

                # Checking information from plugin.xml file
                plugin_fname = os.path.join(packagePath,
                                            PLUGIN_VERSION_FILE_NAME)
                try:
                    appinfo = self.__loadPluginInfo(plugin_fname)
                except EnvironmentError:
                    error = _(u'Plug-in "{}". Can\'t read "{}" file').format(
                        packageName, PLUGIN_VERSION_FILE_NAME)

                    self._print(error)
                    self.__invalidPlugins.append(InvalidPlugin(packageName,
                                                               error))
                    continue

                versions_result = self.__checkPackageVersions(appinfo)

                pluginname = (appinfo.appname
                              if (appinfo is not None and
                                  appinfo.appname is not None)
                              else packageName)

                pluginversion = (appinfo.currentVersionStr
                                 if appinfo is not None
                                 else None)

                if versions_result == pv.PLUGIN_MUST_BE_UPGRADED:
                    error = _(u'Plug-in "{}" is outdated. Please, update the plug-in.').format(pluginname)
                    self._print(error)

                    self.__invalidPlugins.append(
                        InvalidPlugin(pluginname,
                                      error,
                                      pluginversion)
                    )
                    continue
                elif versions_result == pv.OUTWIKER_MUST_BE_UPGRADED:
                    error = _(u'Plug-in "{}" is designed for a newer version OutWiker. Please, install a new OutWiker version.').format(pluginname)
                    self._print(error)

                    self.__invalidPlugins.append(
                        InvalidPlugin(pluginname,
                                      error,
                                      pluginversion))
                    continue

                # Список строк, описывающий возникшие ошибки
                # во время импортирования
                # Выводятся только если не удалось импортировать
                # ни одного модуля
                errors = []

                # Количество загруженных плагинов до импорта нового
                oldPluginsCount = (len(self.__plugins) +
                                   len(self.__disabledPlugins))

                # Переберем все файлы внутри packagePath
                # и попытаемся их импортировать
                for fileName in sorted(os.listdir(packagePath)):
                    try:
                        module = self._importSingleModule(packageName,
                                                          fileName)
                        if module is not None:
                            plugin = self.__loadPlugin(module)
                            if plugin is not None:
                                plugin.version = appinfo.currentVersionStr
                    except BaseException as e:
                        errors.append("*** Plug-in {package} loading error ***\n{package}/{fileName}\n{error}\n{traceback}".format(
                            package=packageName,
                            fileName=fileName,
                            error=str(e),
                            traceback=traceback.format_exc()
                            ))

                # Проверим, удалось ли загрузить плагин
                newPluginsCount = (len(self.__plugins) +
                                   len(self.__disabledPlugins))

                # Вывод ошибок, если ни одного плагина из пакета не удалось
                # импортировать
                if newPluginsCount == oldPluginsCount and len(errors) != 0:
                    error = u"\n\n".join(errors)
                    self._print(error)
                    self._print(u"**********\n")

                    self.__invalidPlugins.append(
                        InvalidPlugin(appinfo.appname,
                                      error,
                                      appinfo.currentVersionStr))
                else:
                    logger.debug(u'Successfully loaded plug-in: {}'.format(
                        packageName))

    def _importSingleModule(self, packageName, fileName):
        """
        Импортировать один модуль по имени пакета и файла с модулем
        """
        extension = ".py"
        result = None

        # Проверим, что файл может быть модулем
        if fileName.endswith(extension) and fileName != "__init__.py":
            modulename = fileName[: -len(extension)]
            # Попытаться импортировать модуль
            package = __import__(packageName + "." + modulename)
            result = getattr(package, modulename)

        return result

    def __loadPlugin(self, module):
        """
        Найти классы плагинов и создать экземпляр первого из них
        """
        assert module is not None

        options = PluginsConfig(self.__application.config)

        for name in dir(module):
            plugin = self.__createPlugin(module,
                                         name,
                                         options.disabledPlugins.value)
            if plugin is not None:
                return plugin

    def __createPlugin(self, module, name, disabledPlugins):
        """
        Попытаться загрузить класс, возможно, это плагин

        module - модуль, откуда загружается класс
        name - имя класса потенциального плагина
        """
        if name.startswith(self.__pluginsStartName):
            obj = getattr(module, name)
            if obj == Plugin or not issubclass(obj, Plugin):
                return

            plugin = obj(self.__application)
            if not self.__isNewPlugin(plugin.name):
                return

            if plugin.name not in disabledPlugins:
                plugin.initialize()
                self.__plugins[plugin.name] = plugin
            else:
                self.__disabledPlugins[plugin.name] = plugin

            return plugin

    def __isNewPlugin(self, pluginname):
        """
        Проверка того, что плагин с таким именем еще не был загружен
        newplugin - плагин, который надо проверить
        """
        return (pluginname not in self.__plugins and
                pluginname not in self.__disabledPlugins)

    def __len__(self):
        return len(self.__plugins)

    def __getitem__(self, pluginname):
        return self.__plugins[pluginname]

    def __iter__(self):
        return iter(self.__plugins.values())
