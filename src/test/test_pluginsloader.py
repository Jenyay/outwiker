# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.gui.guiconfig import PluginsConfig


class PluginsLoaderTest(unittest.TestCase):
    def setUp(self):
        self.config = PluginsConfig (Application.config)
        self.config.disabledPlugins.value = []


    def tearDown (self):
        self.config.disabledPlugins.value = []


    def testEmpty (self):
        loader = PluginsLoader(Application)
        self.assertEqual (len (loader), 0)


    def testLoad (self):
        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testempty2"]
        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 2)
        self.assertEqual (loader[u"TestEmpty1"].name, u"TestEmpty1")
        self.assertEqual (loader[u"TestEmpty1"].version, u"0.1")
        self.assertEqual (loader[u"TestEmpty1"].description,
                          u"This plugin is empty")
        self.assertEqual (loader[u"TestEmpty1"].application, Application)

        self.assertEqual (loader[u"TestEmpty2"].name, u"TestEmpty2")
        self.assertEqual (loader[u"TestEmpty2"].version, u"0.1")
        self.assertEqual (loader[u"TestEmpty2"].description,
                          u"This plugin is empty")

        # Проверим, как работает итерация
        for plugin in loader:
            self.assertTrue (plugin == loader[u"TestEmpty1"] or
                             plugin == loader[u"TestEmpty2"])

        loader.clear()
        self.assertEqual (len (loader), 0)


    def testLoadInvalid (self):
        dirlist = [u"../test/plugins/testinvalid",            # Нет такой директории
                   u"../test/plugins/testinvalid1",
                   u"../test/plugins/testinvalid2",
                   u"../test/plugins/testinvalid4",
                   u"../test/plugins/testinvalid5",
                   u"../test/plugins/testinvalid6",
                   u"../test/plugins/testinvalid7",
                   u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testempty2",                # Ссылка на плагин testempty2 повторяется еще раз
                   u"../test/plugins/testwikicommand",
                   u"../test/plugins/testoutdated",
                   u"../test/plugins/testfromfuture",
                   ]

        loader = PluginsLoader(Application)
        loader.enableOutput = False
        loader.load (dirlist)

        self.assertEqual (len (loader), 3)
        self.assertEqual (loader[u"TestEmpty1"].name, u"TestEmpty1")
        self.assertEqual (loader[u"TestEmpty1"].version, u"0.1")
        self.assertEqual (loader[u"TestEmpty1"].description,
                          u"This plugin is empty")

        self.assertEqual (loader[u"TestEmpty2"].name, u"TestEmpty2")
        self.assertEqual (loader[u"TestEmpty2"].version, u"0.1")
        self.assertEqual (loader[u"TestEmpty2"].description,
                          u"This plugin is empty")

        self.assertEqual (loader[u"TestWikiCommand"].name, u"TestWikiCommand")
        self.assertEqual (loader[u"TestWikiCommand"].version, u"0.1")


    def testDisabledPlugins (self):
        # Добавим плагин TestEmpty1 в черный список
        self.config.disabledPlugins.value = [u"TestEmpty1"]

        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 2)
        self.assertEqual (loader[u"TestEmpty2"].name, u"TestEmpty2")
        self.assertEqual (loader[u"TestEmpty2"].version, u"0.1")
        self.assertEqual (loader[u"TestEmpty2"].description,
                          u"This plugin is empty")

        self.assertEqual (loader[u"TestWikiCommand"].name, u"TestWikiCommand")
        self.assertEqual (loader[u"TestWikiCommand"].version, u"0.1")

        self.assertEqual (len (loader.disabledPlugins), 1)
        self.assertEqual (loader.disabledPlugins[u"TestEmpty1"].name,
                          u"TestEmpty1")
        self.assertEqual (
            loader.disabledPlugins[u"TestEmpty1"].version, u"0.1"
        )
        self.assertEqual (loader.disabledPlugins[u"TestEmpty1"].description,
                          u"This plugin is empty")


    def testOnOffPlugins1 (self):
        # Тест на включение/выключение плагинов
        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 3)
        self.assertEqual (len (loader.disabledPlugins), 0)

        # Отключим плагин TestEmpty1
        self.config.disabledPlugins.value = [u"TestEmpty1"]
        loader.updateDisableList()

        self.assertEqual (len (loader), 2)
        self.assertEqual (len (loader.disabledPlugins), 1)

        self.assertEqual (loader[u"TestEmpty2"].name, u"TestEmpty2")
        self.assertEqual (loader.disabledPlugins[u"TestEmpty1"].name,
                          u"TestEmpty1")


    def testOnOffPlugins2 (self):
        # Тест на включение/выключение плагинов
        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 3)
        self.assertEqual (len (loader.disabledPlugins), 0)

        # Обновим черный список без изменений
        loader.updateDisableList()

        self.assertEqual (len (loader), 3)
        self.assertEqual (len (loader.disabledPlugins), 0)


    def testOnOffPlugins3 (self):
        # Тест на включение/выключение плагинов
        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 3)
        self.assertEqual (len (loader.disabledPlugins), 0)

        # Добавим в черный список плагины, которые не существуют
        self.config.disabledPlugins.value = [u"TestEmpty1111"]
        loader.updateDisableList()

        self.assertEqual (len (loader), 3)
        self.assertEqual (len (loader.disabledPlugins), 0)


    def testOnOffPlugins4 (self):
        # Тест на включение/выключение плагинов
        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testwikicommand"]

        # Сразу заблокируем все плагины
        self.config.disabledPlugins.value = [u"TestEmpty1",
                                             u"TestEmpty2",
                                             u"TestWikiCommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 0)
        self.assertEqual (len (loader.disabledPlugins), 3)

        # Обновим плагины без изменений
        loader.updateDisableList()

        self.assertEqual (len (loader), 0)
        self.assertEqual (len (loader.disabledPlugins), 3)


    def testOnOffPlugins5 (self):
        # Тест на включение/выключение плагинов
        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testwikicommand"]

        # Сразу заблокируем все плагины
        self.config.disabledPlugins.value = [u"TestEmpty1",
                                             u"TestEmpty2",
                                             u"TestWikiCommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 0)
        self.assertEqual (len (loader.disabledPlugins), 3)

        # Включим все плагины
        self.config.disabledPlugins.value = []
        loader.updateDisableList()

        self.assertEqual (len (loader), 3)
        self.assertEqual (len (loader.disabledPlugins), 0)


    def testOnOffPlugins6 (self):
        # Тест на включение/выключение плагинов
        dirlist = [u"../test/plugins/testempty1",
                   u"../test/plugins/testempty2",
                   u"../test/plugins/testwikicommand"]

        loader = PluginsLoader(Application)
        loader.load (dirlist)

        self.assertEqual (len (loader), 3)
        self.assertEqual (len (loader.disabledPlugins), 0)
        self.assertTrue (loader[u"TestEmpty1"].enabled)

        # Отключим плагин TestEmpty1
        self.config.disabledPlugins.value = [u"TestEmpty1"]
        loader.updateDisableList()

        self.assertFalse (loader.disabledPlugins[u"TestEmpty1"].enabled)

        # Опять включим плагин TestEmpty1
        self.config.disabledPlugins.value = []
        loader.updateDisableList()

        self.assertTrue (loader[u"TestEmpty1"].enabled)
