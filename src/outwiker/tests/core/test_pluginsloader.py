# -*- coding: utf-8 -*-

import unittest
import shutil
import os
from time import sleep

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.appinfo import AppInfo
from outwiker.gui.guiconfig import PluginsConfig
from outwiker.tests.basetestcases import BaseOutWikerMixin


class PluginsLoaderRepositoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._app = BaseOutWikerMixin()
        cls._app.initApplication()
        cls.application = cls._app.application
        cls.config = PluginsConfig(cls.application.config)
        cls.loader = PluginsLoader(cls.application)

    @classmethod
    def tearDownClass(cls):
        cls._app.destroyApplication()

    def setUp(self):
        pass

    def tearDown(self):
        self.config.disabledPlugins.value = []

    def testLoadedPlugins(self):
        # Test for remove plugin
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        # Disable TestEmpty2
        self.config.disabledPlugins.value = ["TestEmpty2"]
        loader.updateDisableList()

        self.assertEqual(len(loader.loadedPlugins), 3)
        self.assertIn("TestEmpty1", loader.loadedPlugins)
        self.assertIn("TestEmpty2", loader.loadedPlugins)
        self.assertIn("TestWikiCommand", loader.loadedPlugins)

    def testDisabledPlugins(self):
        # Добавим плагин TestEmpty1 в черный список
        self.config.disabledPlugins.value = ["TestEmpty1"]

        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 2)
        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader["TestEmpty2"].version, "0.1")
        self.assertEqual(loader["TestEmpty2"].description,
                         "This plugin is empty")

        self.assertEqual(loader["TestWikiCommand"].name, "TestWikiCommand")
        self.assertEqual(loader["TestWikiCommand"].version, "0.1")

        self.assertEqual(len(loader.disabledPlugins), 1)
        self.assertEqual(loader.disabledPlugins["TestEmpty1"].name,
                         "TestEmpty1")
        self.assertEqual(
            loader.disabledPlugins["TestEmpty1"].version, "0.1"
        )
        self.assertEqual(loader.disabledPlugins["TestEmpty1"].description,
                         "This plugin is empty")

    def testRemove(self):
        # Test for remove plugin
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        # Disable TestEmpty2
        self.config.disabledPlugins.value = ["TestEmpty2"]
        loader.updateDisableList()

        # pre-check
        self.assertEqual(len(loader), 2)
        self.assertEqual(len(loader.disabledPlugins), 1)

        # remove "TestEmpty1" (enabled)
        self.assertEqual(loader.remove("TestEmpty1"), True)

        self.assertEqual(len(loader), 1)
        self.assertEqual(len(loader.disabledPlugins), 1)

        # remove "TestEmpty2" (disabled)
        self.assertEqual(loader.remove("TestEmpty2"), True)

        self.assertEqual(len(loader), 1)
        self.assertEqual(len(loader.disabledPlugins), 0)

        # remove "TestEmpty3" (None)
        self.assertIs(loader.remove("TestEmpty3"), None)

        self.assertEqual(len(loader), 1)
        self.assertEqual(len(loader.disabledPlugins), 0)

    def testOnOffPlugins1(self):
        # Тест на включение/выключение плагинов
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

        # Отключим плагин TestEmpty1
        self.config.disabledPlugins.value = ["TestEmpty1"]
        loader.updateDisableList()

        self.assertEqual(len(loader), 2)
        self.assertEqual(len(loader.disabledPlugins), 1)

        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader.disabledPlugins["TestEmpty1"].name,
                         "TestEmpty1")

    def testOnOffPlugins2(self):
        # Тест на включение/выключение плагинов
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

        # Обновим черный список без изменений
        loader.updateDisableList()

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

    def testOnOffPlugins3(self):
        # Тест на включение/выключение плагинов
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

        # Добавим в черный список плагины, которые не существуют
        self.config.disabledPlugins.value = ["TestEmpty1111"]
        loader.updateDisableList()

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

    def testOnOffPlugins4(self):
        # Тест на включение/выключение плагинов
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        # Сразу заблокируем все плагины
        self.config.disabledPlugins.value = ["TestEmpty1",
                                             "TestEmpty2",
                                             "TestWikiCommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 3)

        # Обновим плагины без изменений
        loader.updateDisableList()

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 3)

    def testOnOffPlugins5(self):
        # Тест на включение/выключение плагинов
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        # Сразу заблокируем все плагины
        self.config.disabledPlugins.value = ["TestEmpty1",
                                             "TestEmpty2",
                                             "TestWikiCommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 3)

        # Включим все плагины
        self.config.disabledPlugins.value = []
        loader.updateDisableList()

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)

    def testOnOffPlugins6(self):
        # Тест на включение/выключение плагинов
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand"]

        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(len(loader.disabledPlugins), 0)
        self.assertTrue(loader["TestEmpty1"].enabled)

        # Отключим плагин TestEmpty1
        self.config.disabledPlugins.value = ["TestEmpty1"]
        loader.updateDisableList()

        self.assertFalse(loader.disabledPlugins["TestEmpty1"].enabled)

        # Опять включим плагин TestEmpty1
        self.config.disabledPlugins.value = []
        loader.updateDisableList()

        self.assertTrue(loader["TestEmpty1"].enabled)

    def testDisable(self):
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader.loadedPlugins), 2)

        loader.disable('TestEmpty1')

        self.assertEqual(len(loader.disabledPlugins), 1)

    def testDoubleDisable(self):
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader.loadedPlugins), 2)

        loader.disable('TestEmpty1')
        loader.disable('TestEmpty1')

        self.assertEqual(len(loader.disabledPlugins), 1)

    def testEnable(self):
        self.config.disabledPlugins.value = ["TestEmpty1",
                                             "TestEmpty2"]

        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader.disabledPlugins), 2)

        loader.enable('TestEmpty1')

        self.assertEqual(len(loader), 1)
        self.assertEqual(len(loader.disabledPlugins), 1)

        loader.enable('TestEmpty2')
        loader.enable('TestEmpty2')

        self.assertEqual(len(loader), 2)
        self.assertEqual(len(loader.disabledPlugins), 0)


class PluginsLoaderImportTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._app = BaseOutWikerMixin()
        cls._app.initApplication()
        cls.application = cls._app.application
        cls.config = PluginsConfig(cls.application.config)

    @classmethod
    def tearDownClass(cls):
        cls._app.destroyApplication()

    def setUp(self):
        pass

    def tearDown(self):
        self.config.disabledPlugins.value = []

    def testEmpty(self):
        loader = PluginsLoader(self.application)
        self.assertEqual(len(loader), 0)

    def testLoad(self):
        dirlist = ["testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testempty2"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 2)
        self.assertEqual(loader["TestEmpty1"].name, "TestEmpty1")
        self.assertEqual(loader["TestEmpty1"].version, "0.1")
        self.assertEqual(loader["TestEmpty1"].description,
                         "This plugin is empty")
        self.assertEqual(loader["TestEmpty1"].application, self.application)

        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader["TestEmpty2"].version, "0.1")
        self.assertEqual(loader["TestEmpty2"].description,
                         "This plugin is empty")

        # Проверим, как работает итерация
        for plugin in loader:
            self.assertTrue(plugin == loader["TestEmpty1"] or
                            plugin == loader["TestEmpty2"])

        loader.clear()
        self.assertEqual(len(loader), 0)

    def testImport(self):
        dirlist = ["testdata/plugins/testimport"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)

    def testReload(self):

        tmp_plugin_dir = "testdata/plugins/testreload"

        # init test
        shutil.copyfile('testdata/plugins/testreload/testreload/testreload.v1',
                        'testdata/plugins/testreload/testreload/plugin.py')

        dirlist = [tmp_plugin_dir]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        # pre-observation
        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestReload"].name, "TestReload")
        self.assertEqual(loader["TestReload"].version, "0.1")

        # replace plugin file to ver 0.2
        os.remove('testdata/plugins/testreload/testreload/plugin.py')
        sleep(1)
        shutil.copyfile('testdata/plugins/testreload/testreload/testreload.v2',
                        'testdata/plugins/testreload/testreload/plugin.py')

        # observation
        loader.reload("TestReload")
        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestReload"].name, "TestReload")
        self.assertEqual(loader["TestReload"].version, "0.2")

        # restore
        os.remove('testdata/plugins/testreload/testreload/plugin.py')

    def testVersion_01(self):
        dirlist = ["testdata/plugins/testempty3"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestEmpty3"].name, "TestEmpty3")
        self.assertEqual(loader["TestEmpty3"].version, "0.5")

    def testVersion_02(self):
        dirlist = ["testdata/plugins/testempty4"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestEmpty4"].name, "TestEmpty4")
        self.assertEqual(loader["TestEmpty4"].version, None)

    def testLoadInvalid_01(self):
        dirlist = ["testdata/plugins/testinvalid",            # Нет такой директории
                   "testdata/plugins/testinvalid1",
                   "testdata/plugins/testinvalid2",
                   "testdata/plugins/testinvalid4",
                   "testdata/plugins/testinvalid5",
                   "testdata/plugins/testinvalid6",
                   "testdata/plugins/testinvalid7",
                   # no plugin.py file in the packages
                   "testdata/plugins/testinvalid8",
                   "testdata/plugins/testempty1",
                   "testdata/plugins/testempty2",
                   # Ссылка на плагин testempty2 повторяется еще раз
                   "testdata/plugins/testempty2",
                   "testdata/plugins/testwikicommand",
                   "testdata/plugins/testoutdated",
                   "testdata/plugins/testfromfuture",
                   ]

        loader = PluginsLoader(self.application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 3)
        self.assertEqual(loader["TestEmpty1"].name, "TestEmpty1")
        self.assertEqual(loader["TestEmpty1"].version, "0.1")
        self.assertEqual(loader["TestEmpty1"].description,
                         "This plugin is empty")

        self.assertEqual(loader["TestEmpty2"].name, "TestEmpty2")
        self.assertEqual(loader["TestEmpty2"].version, "0.1")
        self.assertEqual(loader["TestEmpty2"].description,
                         "This plugin is empty")

        self.assertEqual(loader["TestWikiCommand"].name, "TestWikiCommand")
        self.assertEqual(loader["TestWikiCommand"].version, "0.1")

    def testLoadInvalid_02(self):
        dirlist = ["testdata/plugins/testinvalid1"]

        loader = PluginsLoader(self.application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)

        self.assertIn('TypeError', loader.invalidPlugins[0].description)

    def testLoadInvalid_03(self):
        dirlist = ["testdata/plugins/testfromfuture"]

        loader = PluginsLoader(self.application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)

    def testLoadInvalid_04(self):
        dirlist = ["testdata/plugins/testoutdated"]

        loader = PluginsLoader(self.application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)

    def testGetInfo(self):
        dirlist = ["testdata/plugins/testempty1", ]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestEmpty1"].name, "TestEmpty1")
        self.assertEqual(loader["TestEmpty1"].version, "0.1")

        plugInfo = loader.getInfo("TestEmpty1")
        self.assertIsInstance(plugInfo, AppInfo)

    def testGetInfo_disabled(self):
        # Добавим плагин TestEmpty1 в черный список
        self.config.disabledPlugins.value = ["TestEmpty1"]

        dirlist = ["testdata/plugins/testempty1", ]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 1)

        plugInfo = loader.getInfo("TestEmpty1")
        self.assertIsInstance(plugInfo, AppInfo)

    def testGetInfo_None(self):
        dirlist = ["testdata/plugins/testempty1", ]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)

        plugInfo = loader.getInfo("Wring_module")
        self.assertIs(plugInfo, None)
