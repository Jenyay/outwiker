# -*- coding: utf-8 -*-

import os
import os.path
import sys
import traceback
import logging
import importlib
import pkgutil

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
    Load and keep plugins.
    for loading all plugins packages from folder 'foo'
        plugins = PluginsLoader(wx.app).load(['foo'])
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
        :param dirlist:
            List of paths from where plugins packages should be loaded.
            For example to load 3 plugins the dirlist should be ['/path1', '/path2']
            /path1/
                plugin1/
                    plugin.py
                    plugin.xml
                plugin2/
                    plugin.py
                    plugin.xml
            /path2/
                plugin3/
                    plugin.py
                    plugin.xml
        :return:
            function return None
            the installed plugins can be get by properties
        """
        assert dirlist is not None

        logger.debug(u'Plugins loading started')

        for currentDir in dirlist:
            if os.path.exists(currentDir):

                # Add currentDir to sys.path
                fullpath = os.path.abspath(currentDir)
                if fullpath not in sys.path:
                    sys.path.insert(0, fullpath)

                # Get list of submodules in currentDir
                # only folders with __init__.py can be submodules
                packagesList = [pkg_name for _, pkg_name, is_pkg in
                                   pkgutil.iter_modules([currentDir]) if is_pkg]

                for packageName in packagesList:
                    packagePath = os.path.join(currentDir, packageName)
                    self.__importPackage(packagePath)

        logger.debug(u'Plugins loading ended')

    def clear(self):
        """
        Uninstall all active plugins and clear plugins list
        Do not clear Disabled and Invalid plugins
        :return:
            None
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

    def __importPackage(self, packagePath):
        """
        Try to load plugin from packagePath
        :param packagePath:
            path to python package from where the plugin should be import
        :return:
            add packagePath to one of the following lists:
            - self.__plugins
            - self.__disabledPlugins
            - self.__invalidPlugins
        """
        # aliases
        join = os.path.join
        packageName = os.path.basename(packagePath)

        logger.debug(u'Trying to load the plug-in: {}'.format(
            packageName))

        # Checking information from plugin.xml file
        plugin_fname = join(packagePath,
                            PLUGIN_VERSION_FILE_NAME)
        try:
            appinfo = self.__loadPluginInfo(plugin_fname)
        except EnvironmentError:
            error = _(u'Plug-in "{}". Can\'t read "{}" file').format(
                packageName, PLUGIN_VERSION_FILE_NAME)

            self._print(error)
            self.__invalidPlugins.append(InvalidPlugin(packageName,
                                                       error))
            return

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
            return
        elif versions_result == pv.OUTWIKER_MUST_BE_UPGRADED:
            error = _(u'Plug-in "{}" is designed for a newer version OutWiker. Please, install a new OutWiker version.').format(pluginname)
            self._print(error)

            self.__invalidPlugins.append(
                InvalidPlugin(pluginname,
                              error,
                              pluginversion))
            return

        # Список строк, описывающий возникшие ошибки
        # во время импортирования
        # Выводятся только если не удалось импортировать
        # ни одного модуля
        errors = []

        # Количество загруженных плагинов до импорта нового
        oldPluginsCount = (len(self.__plugins) +
                           len(self.__disabledPlugins))

        # Find the module with Plugin root class and
        # create  the instance of the class to
        for __, module, is_pkg in pkgutil.iter_modules([packagePath]):
            if is_pkg:
                continue

            try:
                module = importlib.import_module(packageName + "." + module)

                plugin = self.__loadPlugin(module)
                if plugin:
                    plugin.version = appinfo.currentVersionStr
            except BaseException as e:
                errors.append("*** Plug-in {package} loading error ***\n{package}/{fileName}\n{error}\n{traceback}".format(
                    package=packageName,
                    fileName=module,
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

    def __loadPlugin(self, module):
        """
        Find Plugin class in module and try to make instance for it
        :param module:
            module already imported
        :return:
            The instance of loaded plugin or None
        """
        options = PluginsConfig(self.__application.config)

        # get only attr starts with 'Plugin'
        pluginClasses = [attr for attr in dir(module)
                            if attr.startswith(self.__pluginsStartName)]

        for name in pluginClasses:

            plugin = self.__createPlugin(module, name)

            if plugin and self.__isNewPlugin(plugin.name):
                if plugin.name not in options.disabledPlugins.value:
                    plugin.initialize()
                    self.__plugins[plugin.name] = plugin
                else:
                    self.__disabledPlugins[plugin.name] = plugin
                return plugin

    def __createPlugin(self, module, name):
        """
        Create plugin instance if name is a subclass of Plugin
        :param module:
            module name
        :param name:
            attribute from the module
        :return:
            instance of name class or None
        """
        obj = getattr(module, name)
        if issubclass(obj, Plugin) and obj != Plugin:
            return obj(self.__application)


    def __isNewPlugin(self, pluginname):
        """
        Проверка того, что плагин с таким именем еще не был загружен
        newplugin - плагин, который надо проверить
        """
        return (pluginname not in self.__plugins and
                pluginname not in self.__disabledPlugins)

    def reload(self, pluginname):
        """
        Reload plugin module and plugin instance in self.__plugins list
        :param pluginname:
            name of the actual plugin
        :return:
            None
        """
        if pluginname in self.__plugins:
            plug_path = self.__plugins[pluginname].pluginPath
            module = sys.modules[self.__plugins[pluginname].__class__.__module__]

            # destroy plugin
            self.__plugins[pluginname].destroy()
            del self.__plugins[pluginname]

            # reload module
            importlib.invalidate_caches()
            importlib.reload(module)

            # import plugin again
            self.__importPackage(plug_path)

    def getInfo(self, pluginname, langlist=["en"]):
        """
        Retrieve a AppInfo for plugin_name
        :param pluginname:
            name of the loaded plugin
        :param lang:
            langlist - list of the languages name ("en", "ru_RU" etc)
        :return:
            AppInfo for pluginname
            if pluginname cannot be located, then None is returned.
        :exception IOError:
            if plugin.xml cannot be read
        """
        if pluginname in self.__plugins:
            module = self.__plugins[pluginname].__class__.__module__
        elif pluginname in self.__disabledPlugins:
            module = self.__disabledPlugins[pluginname].__class__.__module__
        else:
            module = ''

        xml_content = pkgutil.get_data(module, PLUGIN_VERSION_FILE_NAME)
        if xml_content:
            return XmlVersionParser(langlist).parse(xml_content)


    def __len__(self):
        return len(self.__plugins)

    def __getitem__(self, pluginname):
        return self.__plugins[pluginname]

    def __iter__(self):
        return iter(self.__plugins.values())
