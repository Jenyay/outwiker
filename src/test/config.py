#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Тесты, связанные с конфигом
"""

import unittest
import os
import os.path
import ConfigParser
import shutil

from outwiker.core.config import Config
from outwiker.core.system import getCurrentDir, getConfigPath
import outwiker.core.config

from outwiker.gui.guiconfig import TrayConfig, EditorConfig


class ConfigTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/testconfig.ini"

        if os.path.exists (self.path):
            os.remove (self.path)

    def tearDown (self):
        if os.path.exists (self.path):
            os.remove (self.path)


    def testGetSet (self):
        config = Config (self.path)
        config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
        config.set (u"Секция 1", u"Параметр 2", 111)

        self.assertEqual (config.get (u"Секция 1", u"Параметр 1"), u"Значение 1")
        self.assertEqual (config.getint (u"Секция 1", u"Параметр 2"), 111)

    
    def testWrite (self):
        """
        Тесты на то, что измененные значения сразу сохраняются в файл
        """
        config = Config (self.path)
        config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
        config.set (u"Секция 1", u"Параметр 2", 111)

        config2 = Config (self.path)
        self.assertEqual (config2.get (u"Секция 1", u"Параметр 1"), u"Значение 1")
        self.assertEqual (config2.getint (u"Секция 1", u"Параметр 2"), 111)

    
    def testRemoveSection (self):
        config = Config (self.path)
        config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
        config.set (u"Секция 1", u"Параметр 2", 111)

        result = config.remove_section (u"Секция 1")

        config2 = Config (self.path)
        self.assertRaises (ConfigParser.NoSectionError, config2.get, u"Секция 1", u"Параметр 1")
    

    def testHasSection (self):
        config = Config (self.path)
        config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
        config.set (u"Секция 1", u"Параметр 2", 111)

        self.assertEqual (config.has_section (u"Секция 1"), True)
        
        result = config.remove_section (u"Секция 1")
        self.assertEqual (config.has_section (u"Секция 1"), False)
    

    def testPortableConfig (self):
        """
        Проверка правильности определения расположения конфига при хранении его в папке с программой
        """
        dirname = u".outwiker_test"
        fname = u"outwiker_test.ini"

        programDir = getCurrentDir()
        localPath = os.path.join (programDir, fname)

        # Создадим файл рядом с запускаемым файлом
        fp = open (localPath, "w")
        fp.close()
        
        fullpath = getConfigPath(dirname, fname)

        self.assertEqual (localPath, fullpath)

        # Удалим созданный файл
        os.remove (localPath)
    

    def testNotPortableConfig1 (self):
        """
        Проверка правильности определения расположения конфига при хранении его в папке профиля
        """
        dirname = u".outwiker_test"
        fname = u"outwiker_test.ini"

        programDir = getCurrentDir()
        localPath = os.path.join (programDir, fname)

        # На всякий случай проверим, что файла в локальной папке нет, иначе удалим его
        if os.path.exists (localPath):
            os.remove (localPath)

        homeDir = os.path.join (os.path.expanduser("~"), dirname)
        homePath = os.path.join (homeDir, fname)

        # Удалим папку в профиле
        if os.path.exists (homeDir):
            shutil.rmtree (homeDir)

        fullpath = getConfigPath(dirname, fname)

        self.assertEqual (homePath, fullpath)
        self.assertTrue (os.path.exists (homeDir))

        # Удалим папку в профиле
        if os.path.exists (homeDir):
            shutil.rmtree (homeDir)


class ConfigOptionsTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/testconfig.ini"

        # Создадим небольшой файл настроек
        with open (self.path, "wb") as fp:
            fp.write (u"[Test]\n")
            fp.write (u"intval=100\n")
            fp.write (u"boolval=True\n")
            fp.write (u"strval=тест\n".encode ("utf-8"))
            fp.write (u"list1=элемент 1;элемент 2;элемент 3\n".encode ("utf-8"))
            fp.write (u"list2=элемент 1\n".encode ("utf-8"))
            fp.write (u"list3=\n".encode ("utf-8"))
            fp.write (u"list4=;\n".encode ("utf-8"))
            fp.write (u"list5=;;\n".encode ("utf-8"))
            fp.write (u"list6=элемент 1;\n".encode ("utf-8"))

            fp.write (u"list8=элемент 1|элемент 2|элемент 3\n".encode ("utf-8"))
            fp.write (u"list9=элемент 1\n".encode ("utf-8"))
            fp.write (u"list10=\n".encode ("utf-8"))
            fp.write (u"list11=|\n".encode ("utf-8"))
            fp.write (u"list12=элемент 1|\n".encode ("utf-8"))

        self.config = outwiker.core.config.Config (self.path)
    

    def tearDown (self):
        os.remove (self.path)
    

    # Строковые опции
    def testStringOpt1 (self):
        opt = outwiker.core.config.StringOption (self.config, u"Test", u"strval", "defaultval")
        self.assertEqual (opt.value, u"тест")


    def testStringOpt2 (self):
        opt = outwiker.core.config.StringOption (self.config, u"Test", u"strval2", "defaultval")
        self.assertEqual (opt.value, u"defaultval")


    def testStringOpt3 (self):
        opt = outwiker.core.config.StringOption (self.config, u"Test", u"strval3", "defaultval")
        opt.value = u"проверка"

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.StringOption (newconfig, u"Test", u"strval3", "defaultval")

        self.assertEqual (newopt.value, u"проверка")


    def testStringOpt4 (self):
        opt = outwiker.core.config.StringOption (self.config, u"Test", u"strval3", "defaultval")
        newopt = outwiker.core.config.StringOption (self.config, u"Test", u"strval3", "defaultval")

        opt.value = u"проверка"

        self.assertEqual (newopt.value, u"проверка")
    

    # Целочисленные опции
    def testIntOpt1 (self):
        opt = outwiker.core.config.IntegerOption (self.config, u"Test", u"intval", 777)
        self.assertEqual (opt.value, 100)


    def testIntOpt2 (self):
        opt = outwiker.core.config.IntegerOption (self.config, u"Test", u"intval2", 777)
        self.assertEqual (opt.value, 777)


    def testIntOpt3 (self):
        opt = outwiker.core.config.IntegerOption (self.config, u"Test", u"intval3", 777)
        opt.value = 666

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.IntegerOption (newconfig, u"Test", u"intval3", 888)

        self.assertEqual (newopt.value, 666)
    

    def testIntOpt4 (self):
        opt = outwiker.core.config.IntegerOption (self.config, u"Test", u"intval3", 777)
        newopt = outwiker.core.config.IntegerOption (self.config, u"Test", u"intval3", 888)

        opt.value = 666

        self.assertEqual (newopt.value, 666)
    

    # Булевы опции
    def testBoolOpt1 (self):
        opt = outwiker.core.config.BooleanOption (self.config, u"Test", u"Boolval", False)
        self.assertEqual (opt.value, True)


    def testBoolOpt2 (self):
        opt = outwiker.core.config.BooleanOption (self.config, u"Test", u"Boolval2", False)
        self.assertEqual (opt.value, False)


    def testBoolOpt3 (self):
        opt = outwiker.core.config.BooleanOption (self.config, u"Test", u"Boolval3", False)
        opt.value = True

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.BooleanOption (newconfig, u"Test", u"Boolval3", False)

        self.assertEqual (newopt.value, True)
    

    def testBoolOpt4 (self):
        opt = outwiker.core.config.BooleanOption (self.config, u"Test", u"Boolval3", False)
        newopt = outwiker.core.config.BooleanOption (self.config, u"Test", u"Boolval3", False)

        opt.value = True

        self.assertEqual (newopt.value, True)


    def testRemoveOption1 (self):
        opt = outwiker.core.config.StringOption (self.config, u"Test", u"strval", u"Значение по умолчанию")
        self.assertEqual (opt.value, u"тест")

        opt.remove_option()
        self.assertEqual (opt.value, u"Значение по умолчанию")


    def testRemoveOption2 (self):
        opt = outwiker.core.config.StringOption (self.config, u"Test", u"strval", u"Значение по умолчанию")
        opt.remove_option()

        opt2 = outwiker.core.config.StringOption (self.config, u"Test", u"strval", u"Значение по умолчанию")
        self.assertEqual (opt2.value, u"Значение по умолчанию")


    def testRemoveOption3 (self):
        opt = outwiker.core.config.StringOption (self.config, u"Test", u"invalid", u"Значение по умолчанию")
        opt.remove_option()


    def testListOption1 (self):
        opt1 = outwiker.core.config.ListOption (self.config, u"Test", u"list1", [])
        self.assertEqual (opt1.value, [u"элемент 1", u"элемент 2", u"элемент 3"])

        opt2 = outwiker.core.config.ListOption (self.config, u"Test", u"list2", [])
        self.assertEqual (opt2.value, [u"элемент 1"])

        opt3 = outwiker.core.config.ListOption (self.config, u"Test", u"list3", [])
        self.assertEqual (opt3.value, [u""])

        opt4 = outwiker.core.config.ListOption (self.config, u"Test", u"list4", [])
        self.assertEqual (opt4.value, [u"", u""])

        opt5 = outwiker.core.config.ListOption (self.config, u"Test", u"list5", [])
        self.assertEqual (opt5.value, [u"", u"", u""])

        opt6 = outwiker.core.config.ListOption (self.config, u"Test", u"list6", [])
        self.assertEqual (opt6.value, [u"элемент 1", u""])

        opt7 = outwiker.core.config.ListOption (self.config, u"Test", u"list7", [])
        self.assertEqual (opt7.value, [])

    
    def testListOption2 (self):
        opt8 = outwiker.core.config.ListOption (self.config, u"Test", u"list8", [], separator="|")
        self.assertEqual (opt8.value, [u"элемент 1", u"элемент 2", u"элемент 3"])

        opt9 = outwiker.core.config.ListOption (self.config, u"Test", u"list9", [], separator="|")
        self.assertEqual (opt9.value, [u"элемент 1"])

        opt10 = outwiker.core.config.ListOption (self.config, u"Test", u"list10", [], separator="|")
        self.assertEqual (opt10.value, [u""])

        opt11 = outwiker.core.config.ListOption (self.config, u"Test", u"list11", [], separator="|")
        self.assertEqual (opt11.value, [u"", u""])

        opt12 = outwiker.core.config.ListOption (self.config, u"Test", u"list12", [], separator="|")
        self.assertEqual (opt12.value, [u"элемент 1", u""])


    def testSaveListOption1 (self):
        testlist = [u"элемент 1", u"элемент 2", u"элемент 3"] 

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])

        self.assertEqual (newopt.value, testlist)

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"элемент 1;элемент 2;элемент 3")


    def testSaveListOption2 (self):
        testlist = [u"элемент 1"]

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])

        self.assertEqual (newopt.value, testlist)

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"элемент 1")


    def testSaveListOption3 (self):
        testlist = []

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])

        self.assertEqual (newopt.value, [u""])

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"")


    def testSaveListOption4 (self):
        testlist = [u"элемент 1", u"элемент 2", u"элемент 3"] 

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")

        self.assertEqual (newopt.value, testlist)

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"элемент 1|элемент 2|элемент 3")


    def testSaveListOption5 (self):
        testlist = [u"элемент 1"]

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")

        self.assertEqual (newopt.value, testlist)

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"элемент 1")


    def testSaveListOption6 (self):
        testlist = []

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")

        self.assertEqual (newopt.value, [""])

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"")


    def testSaveListOption7 (self):
        testlist = [u""]

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")

        self.assertEqual (newopt.value, testlist)

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"")


    def testSaveListOption8 (self):
        testlist = [u""]

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [])

        self.assertEqual (newopt.value, testlist)

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"")


    def testSaveListOption9 (self):
        testlist = [u""]

        opt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")
        opt.value = testlist

        newconfig = outwiker.core.config.Config (self.path)
        newopt = outwiker.core.config.ListOption (self.config, u"Test", u"savelist", [], separator="|")

        self.assertEqual (newopt.value, testlist)

        stringopt = outwiker.core.config.StringOption (self.config, u"Test", u"savelist", "")
        self.assertEqual (stringopt.value.strip(), u"")



class TrayConfigTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/testconfig.ini"
        self.config = outwiker.core.config.Config (self.path)

        self.trayConfig = TrayConfig (self.config)
    

    def tearDown (self):
        if os.path.exists (self.path):
            os.remove (self.path)


    def testDefault (self):
        self.assertEqual (self.trayConfig.minimizeOption.value, True)
        self.assertEqual (self.trayConfig.startIconizedOption.value, False)
        self.assertEqual (self.trayConfig.alwaysShowTrayIconOption.value, False)
    

    def testChange (self):
        newConfig = TrayConfig (self.config)

        newConfig.minimizeOption.value = False
        self.assertEqual (self.trayConfig.minimizeOption.value, False)

        newConfig.startIconizedOption.value = True
        self.assertEqual (self.trayConfig.startIconizedOption.value, True)

        newConfig.alwaysShowTrayIconOption.value = True
        self.assertEqual (self.trayConfig.alwaysShowTrayIconOption.value, True)



class EditorConfigTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/testconfig.ini"
        self.config = outwiker.core.config.Config (self.path)

        self.editorConfig = EditorConfig (self.config)
    

    def tearDown (self):
        if os.path.exists (self.path):
            os.remove (self.path)
    

    def testDefault (self):
        self.assertEqual (self.editorConfig.lineNumbersOption.value, False)
        self.assertEqual (self.editorConfig.tabWidthOption.value, 4)
        self.assertEqual (self.editorConfig.fontSizeOption.value, 10)
        self.assertEqual (self.editorConfig.fontFaceNameOption.value, "")
        self.assertEqual (self.editorConfig.fontIsBold.value, False)
        self.assertEqual (self.editorConfig.fontIsItalic.value, False)


    def testChange (self):
        newConfig = EditorConfig (self.config)

        newConfig.lineNumbersOption.value = True
        self.assertEqual (self.editorConfig.lineNumbersOption.value, True)

        newConfig.tabWidthOption.value = 8
        self.assertEqual (self.editorConfig.tabWidthOption.value, 8)

        newConfig.fontSizeOption.value = 12
        self.assertEqual (self.editorConfig.fontSizeOption.value, 12)

        newConfig.fontFaceNameOption.value = "Arial"
        self.assertEqual (self.editorConfig.fontFaceNameOption.value, "Arial")

        newConfig.fontIsBold.value = True
        self.assertEqual (self.editorConfig.fontIsBold.value, True)

        newConfig.fontIsItalic.value = True
        self.assertEqual (self.editorConfig.fontIsItalic.value, True)
