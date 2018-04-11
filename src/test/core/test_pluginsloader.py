# -*- coding: utf-8 -*-

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.appinfo import AppInfo
from outwiker.gui.guiconfig import PluginsConfig
from test.basetestcases import BaseOutWikerMixin
import unittest
import shutil
import os
from time import sleep

class PluginsLoaderTest(BaseOutWikerMixin, unittest.TestCase):
    def setUp(self):
        self.initApplication()
        self.config = PluginsConfig(self.application.config)
        self.config.disabledPlugins.value = []

    def tearDown(self):
        self.destroyApplication()

    def testEmpty(self):
        loader = PluginsLoader(self.application)
        self.assertEqual(len(loader), 0)

    def testLoad(self):
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testempty2"]
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

    def testReload(self):

        tmp_plugin_dir = "../test/plugins/testreload"

        # init test
        shutil.copyfile('../test/plugins/testreload/testreload/testreload.v1',
                  '../test/plugins/testreload/testreload/testreload.py')

        dirlist = [tmp_plugin_dir]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        # pre-observation
        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestReload"].name, "TestReload")
        self.assertEqual(loader["TestReload"].version, "0.1")

        # replace plugin file to ver 0.2
        os.remove('../test/plugins/testreload/testreload/testreload.py')
        sleep(1)
        shutil.copyfile('../test/plugins/testreload/testreload/testreload.v2',
                        '../test/plugins/testreload/testreload/testreload.py')

        # observation
        loader.reload("TestReload")
        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestReload"].name, "TestReload")
        self.assertEqual(loader["TestReload"].version, "0.2")

        # restore
        os.remove('../test/plugins/testreload/testreload/testreload.py')

    def testVersion_01(self):
        dirlist = ["../test/plugins/testempty3"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestEmpty3"].name, "TestEmpty3")
        self.assertEqual(loader["TestEmpty3"].version, "0.5")

    def testVersion_02(self):
        dirlist = ["../test/plugins/testempty4"]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)
        self.assertEqual(loader["TestEmpty4"].name, "TestEmpty4")
        self.assertEqual(loader["TestEmpty4"].version, None)

    def testLoadInvalid_01(self):
        dirlist = ["../test/plugins/testinvalid",            # Нет такой директории
                   "../test/plugins/testinvalid1",
                   "../test/plugins/testinvalid2",
                   "../test/plugins/testinvalid4",
                   "../test/plugins/testinvalid5",
                   "../test/plugins/testinvalid6",
                   "../test/plugins/testinvalid7",
                   "../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testempty2",                # Ссылка на плагин testempty2 повторяется еще раз
                   "../test/plugins/testwikicommand",
                   "../test/plugins/testoutdated",
                   "../test/plugins/testfromfuture",
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

    def testDisabledPlugins(self):
        # Добавим плагин TestEmpty1 в черный список
        self.config.disabledPlugins.value = ["TestEmpty1"]

        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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

    def testOnOffPlugins1(self):
        # Тест на включение/выключение плагинов
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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

    def testLoadInvalid_02(self):
        dirlist = ["../test/plugins/testinvalid1"]

        loader = PluginsLoader(self.application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)

        self.assertIn('TypeError', loader.invalidPlugins[0].description)

    def testLoadInvalid_03(self):
        dirlist = ["../test/plugins/testfromfuture"]

        loader = PluginsLoader(self.application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)
        # self.assertIn(u'Please, install a new OutWiker version.',
        #               loader.invalidPlugins[0].description)

    def testLoadInvalid_04(self):
        dirlist = ["../test/plugins/testoutdated"]

        loader = PluginsLoader(self.application)
        loader.enableOutput = False
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.invalidPlugins), 1)
        # self.assertIn(u'Please, update the plug-in.',
        #               loader.invalidPlugins[0].description)

    def testGetInfo(self):
        dirlist = ["../test/plugins/testempty1",]
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

        dirlist = ["../test/plugins/testempty1", ]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 0)
        self.assertEqual(len(loader.disabledPlugins), 1)

        plugInfo = loader.getInfo("TestEmpty1")
        self.assertIsInstance(plugInfo, AppInfo)


    def testGetInfo_None(self):
        dirlist = ["../test/plugins/testempty1",]
        loader = PluginsLoader(self.application)
        loader.load(dirlist)

        self.assertEqual(len(loader), 1)

        plugInfo = loader.getInfo("Wring_module")
        self.assertIs(plugInfo, None)

    def testOnOffPlugins1(self):
        # Test for remove plugin
        dirlist = ["../test/plugins/testempty1",
                   "../test/plugins/testempty2",
                   "../test/plugins/testwikicommand"]

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
