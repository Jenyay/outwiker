# -*- coding: utf-8 -*-
"""
Тесты, связанные с конфигом
"""

import unittest
import os
import os.path
import configparser
import shutil
import datetime
import tempfile

from outwiker.core.config import (Config,
                                  StringOption,
                                  IntegerOption,
                                  DateTimeOption,
                                  BooleanOption,
                                  ListOption,
                                  StringListSection,
                                  StcStyleOption,
                                  JSONOption)
from outwiker.core.system import getCurrentDir, getConfigPath, getOS
from outwiker.gui.guiconfig import TrayConfig, EditorConfig
from outwiker.gui.stcstyle import StcStyle

from test.utils import removeDir


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.path = os.path.join(self.tempdir, "testconfig.ini")

    def tearDown(self):
        removeDir(self.tempdir)

    def testGetSet(self):
        config = Config(self.path)
        config.set("Секция 1", "Параметр 1", "Значение 1")
        config.set("Секция 1", "Параметр 2", 111)

        self.assertEqual(config.get("Секция 1", "Параметр 1"),
                         "Значение 1")
        self.assertEqual(config.getint("Секция 1", "Параметр 2"), 111)

    def testWrite(self):
        """
        Тесты на то, что измененные значения сразу сохраняются в файл
        """
        config = Config(self.path)
        config.set("Секция 1", "Параметр 1", "Значение 1")
        config.set("Секция 1", "Параметр 2", 111)

        config2 = Config(self.path)
        self.assertEqual(config2.get("Секция 1", "Параметр 1"),
                         "Значение 1")
        self.assertEqual(config2.getint("Секция 1", "Параметр 2"), 111)

    def testRemoveSection(self):
        config = Config(self.path)
        config.set("Секция 1", "Параметр 1", "Значение 1")
        config.set("Секция 1", "Параметр 2", 111)

        config.remove_section("Секция 1")

        config2 = Config(self.path)
        self.assertRaises(configparser.NoSectionError,
                          config2.get,
                          "Секция 1",
                          "Параметр 1")

    def testHasSection(self):
        config = Config(self.path)
        config.set("Секция 1", "Параметр 1", "Значение 1")
        config.set("Секция 1", "Параметр 2", 111)

        self.assertEqual(config.has_section("Секция 1"), True)

        config.remove_section("Секция 1")
        self.assertEqual(config.has_section("Секция 1"), False)

    def testPortableConfig(self):
        """
        Проверка правильности определения расположения конфига при хранении его
        в папке с программой
        """
        dirname = ".outwiker_test"
        fname = "outwiker_test.ini"

        programDir = getCurrentDir()
        localPath = os.path.join(programDir, fname)

        # Создадим файл рядом с запускаемым файлом
        fp = open(localPath, "w")
        fp.close()

        fullpath = getConfigPath(dirname, fname)

        self.assertEqual(localPath, fullpath)

        # Удалим созданный файл
        os.remove(localPath)

    def testNotPortableConfig1(self):
        """
        Проверка правильности определения расположения конфига при хранении его
        в папке профиля
        """
        dirname = ".outwiker_test"
        fname = "outwiker_test.ini"

        programDir = getCurrentDir()
        localPath = os.path.join(programDir, fname)

        # На всякий случай проверим, что файла в локальной папке нет,
        # иначе удалим его
        if os.path.exists(localPath):
            os.remove(localPath)

        homeDir = os.path.join(getOS().settingsDir, dirname)
        homePath = os.path.join(homeDir, fname)

        # Удалим папку в профиле
        if os.path.exists(homeDir):
            shutil.rmtree(homeDir)

        fullpath = getConfigPath(dirname, fname)

        self.assertEqual(homePath, fullpath)
        self.assertTrue(os.path.exists(homeDir))

        # Удалим папку в профиле
        if os.path.exists(homeDir):
            shutil.rmtree(homeDir)

    def testInvalidConfigFile(self):
        invalid_fname = "outwiker_invalid.ini"
        src_invalid_full_path = os.path.join("../test",
                                             "samplefiles",
                                             invalid_fname)

        shutil.copy(src_invalid_full_path, self.tempdir)

        fullpath = os.path.join(self.tempdir, invalid_fname)

        Config(fullpath)
        self.assertTrue(os.path.exists(fullpath))
        self.assertTrue(os.path.exists(fullpath + ".bak"))


class ConfigOptionsTest(unittest.TestCase):
    def setUp(self):
        self.path = "../test/testconfig.ini"

        # Создадим небольшой файл настроек
        with open(self.path, "w", encoding='utf8') as fp:
            fp.write("[Test]\n")
            fp.write("intval=100\n")
            fp.write("boolval=True\n")
            fp.write("datetimeval=2012-08-25 16:18:24.171654\n")
            fp.write("datetimeerror=sdfasdfasdf\n")
            fp.write("strval=тест\n")

            fp.write("style_01=fore:#AAAAAA,back:#111111,bold,italic,underline\n")
            fp.write("style_02=back:#111111,bold,italic,underline\n")
            fp.write("style_03=bold\n")
            fp.write("style_invalid_01=asdfadsfads\n")

            fp.write("list1=элемент 1;элемент 2;элемент 3\n")
            fp.write("list2=элемент 1\n")
            fp.write("list3=\n")
            fp.write("list4=;\n")
            fp.write("list5=;;\n")
            fp.write("list6=элемент 1;\n")

            fp.write("list8=элемент 1|элемент 2|элемент 3\n")
            fp.write("list9=элемент 1\n")
            fp.write("list10=\n")
            fp.write("list11=|\n")
            fp.write("list12=элемент 1|\n")

            fp.write("jsonval_01={}\n")
            fp.write('jsonval_02="строка"\n')
            fp.write("jsonval_03=[]\n")
            fp.write("jsonval_04=[1, 2, 3]\n")
            fp.write('jsonval_05={"x": 100}\n')

        self.config = Config(self.path)

    def tearDown(self):
        os.remove(self.path)

    # Строковые опции
    def testStringOpt1(self):
        opt = StringOption(self.config, "Test", "strval", "defaultval")
        self.assertEqual(opt.value, "тест")

    def testStringOpt2(self):
        opt = StringOption(self.config, "Test", "strval2", "defaultval")
        self.assertEqual(opt.value, "defaultval")

    def testStringOpt3(self):
        opt = StringOption(self.config, "Test", "strval3", "defaultval")
        opt.value = "проверка"

        newconfig = Config(self.path)
        newopt = StringOption(newconfig, "Test", "strval3", "defaultval")

        self.assertEqual(newopt.value, "проверка")

    def testStringOpt4(self):
        opt = StringOption(self.config, "Test", "strval3", "defaultval")
        newopt = StringOption(self.config, "Test", "strval3", "defaultval")

        opt.value = "проверка"

        self.assertEqual(newopt.value, "проверка")

    # Целочисленные опции
    def testIntOpt1(self):
        opt = IntegerOption(self.config, "Test", "intval", 777)
        self.assertEqual(opt.value, 100)

    def testIntOpt2(self):
        opt = IntegerOption(self.config, "Test", "intval2", 777)
        self.assertEqual(opt.value, 777)

    def testIntOpt3(self):
        opt = IntegerOption(self.config, "Test", "intval3", 777)
        opt.value = 666

        newconfig = Config(self.path)
        newopt = IntegerOption(newconfig, "Test", "intval3", 888)

        self.assertEqual(newopt.value, 666)

    def testIntOpt4(self):
        opt = IntegerOption(self.config, "Test", "intval3", 777)
        newopt = IntegerOption(self.config, "Test", "intval3", 888)

        opt.value = 666

        self.assertEqual(newopt.value, 666)

    # Опции для хранения даты/времени
    def testDateTimeOpt1(self):
        strdatetime = "2012-08-25 16:18:24.171654"

        opt = DateTimeOption(self.config, "Test", "datetimeval", None)
        self.assertEqual(opt.value,
                         datetime.datetime.strptime(
                              strdatetime,
                              DateTimeOption.formatDate))

    def testDateTimeOpt2(self):
        opt = DateTimeOption(self.config,
                             "Test",
                             "datetimeval_invalid",
                             None)
        self.assertEqual(opt.value, None)

    def testDateTimeOpt3(self):
        defaultValue = datetime.datetime(2012, 8, 25)

        opt = DateTimeOption(self.config,
                             "Test",
                             "datetimeval_invalid",
                             defaultValue)
        self.assertEqual(opt.value, defaultValue)

    def testDateTimeOpt4(self):
        newdate = datetime.datetime(2012, 8, 25)
        opt = DateTimeOption(self.config, "Test", "datetimeval2", None)
        opt.value = newdate

        newconfig = Config(self.path)
        newopt = DateTimeOption(newconfig, "Test", "datetimeval2", None)

        self.assertEqual(newopt.value, newdate)

    def testDateTimeOpt5(self):
        defaultValue = datetime.datetime(2012, 8, 25)

        opt = DateTimeOption(self.config,
                             "Test",
                             "datetimeerror",
                             defaultValue)
        self.assertEqual(opt.value, defaultValue)

    # Булевы опции
    def testBoolOpt1(self):
        opt = BooleanOption(self.config, "Test", "Boolval", False)
        self.assertEqual(opt.value, True)

    def testBoolOpt2(self):
        opt = BooleanOption(self.config, "Test", "Boolval2", False)
        self.assertEqual(opt.value, False)

    def testBoolOpt3(self):
        opt = BooleanOption(self.config, "Test", "Boolval3", False)
        opt.value = True

        newconfig = Config(self.path)
        newopt = BooleanOption(newconfig, "Test", "Boolval3", False)

        self.assertEqual(newopt.value, True)

    def testBoolOpt4(self):
        opt = BooleanOption(self.config, "Test", "Boolval3", False)
        newopt = BooleanOption(self.config, "Test", "Boolval3", False)

        opt.value = True

        self.assertEqual(newopt.value, True)

    def testBoolOpt5(self):
        self.config.set('Test', 'Boolval', True)
        self.assertEqual(self.config.getbool('Test', 'Boolval'), True)

    def testBoolOpt6(self):
        self.config.set('Test', 'Boolval', False)
        self.assertEqual(self.config.getbool('Test', 'Boolval'), False)

    def testBoolOpt7(self):
        self.config.set('Test', 'Boolval', 'True')
        self.assertEqual(self.config.getbool('Test', 'Boolval'), True)

    def testBoolOpt8(self):
        self.config.set('Test', 'Boolval', 'False')
        self.assertEqual(self.config.getbool('Test', 'Boolval'), False)

    def testBoolOpt9(self):
        self.config.set('Test', 'Boolval', '   True   ')
        self.assertEqual(self.config.getbool('Test', 'Boolval'), True)

    def testBoolOpt10(self):
        self.config.set('Test', 'Boolval', '   False   ')
        self.assertEqual(self.config.getbool('Test', 'Boolval'), False)

    def testBoolOpt11(self):
        self.config.set('Test', 'Boolval', '   sdfasgfadsf   ')
        self.assertEqual(self.config.getbool('Test', 'Boolval'), False)

    def testRemoveOption1(self):
        opt = StringOption(self.config,
                           "Test",
                           "strval",
                           "Значение по умолчанию")
        self.assertEqual(opt.value, "тест")

        opt.remove_option()
        self.assertEqual(opt.value, "Значение по умолчанию")

    def testRemoveOption2(self):
        opt = StringOption(self.config,
                           "Test",
                           "strval",
                           "Значение по умолчанию")
        opt.remove_option()

        opt2 = StringOption(self.config,
                            "Test",
                            "strval",
                            "Значение по умолчанию")
        self.assertEqual(opt2.value, "Значение по умолчанию")

    def testRemoveOption3(self):
        opt = StringOption(self.config,
                           "Test",
                           "invalid",
                           "Значение по умолчанию")
        opt.remove_option()

    def testListOption1(self):
        opt1 = ListOption(self.config, "Test", "list1", [])
        self.assertEqual(opt1.value,
                         ["элемент 1", "элемент 2", "элемент 3"])

        opt2 = ListOption(self.config, "Test", "list2", [])
        self.assertEqual(opt2.value, ["элемент 1"])

        opt3 = ListOption(self.config, "Test", "list3", [])
        self.assertEqual(opt3.value, [""])

        opt4 = ListOption(self.config, "Test", "list4", [])
        self.assertEqual(opt4.value, ["", ""])

        opt5 = ListOption(self.config, "Test", "list5", [])
        self.assertEqual(opt5.value, ["", "", ""])

        opt6 = ListOption(self.config, "Test", "list6", [])
        self.assertEqual(opt6.value, ["элемент 1", ""])

        opt7 = ListOption(self.config, "Test", "list7", [])
        self.assertEqual(opt7.value, [])

    def testListOption2(self):
        opt8 = ListOption(self.config, "Test", "list8", [], separator="|")
        self.assertEqual(opt8.value,
                         ["элемент 1", "элемент 2", "элемент 3"])

        opt9 = ListOption(self.config, "Test", "list9", [], separator="|")
        self.assertEqual(opt9.value, ["элемент 1"])

        opt10 = ListOption(self.config, "Test", "list10", [], separator="|")
        self.assertEqual(opt10.value, [""])

        opt11 = ListOption(self.config, "Test", "list11", [], separator="|")
        self.assertEqual(opt11.value, ["", ""])

        opt12 = ListOption(self.config, "Test", "list12", [], separator="|")
        self.assertEqual(opt12.value, ["элемент 1", ""])

    def testSaveListOption1(self):
        testlist = ["элемент 1", "элемент 2", "элемент 3"]

        opt = ListOption(self.config, "Test", "savelist", [])
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [])

        self.assertEqual(newopt.value, testlist)

        stringopt = StringOption(newconfig, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(),
                         "элемент 1;элемент 2;элемент 3")

    def testSaveListOption2(self):
        testlist = ["элемент 1"]

        opt = ListOption(self.config, "Test", "savelist", [])
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [])

        self.assertEqual(newopt.value, testlist)

        stringopt = StringOption(newconfig, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(), "элемент 1")

    def testSaveListOption3(self):
        testlist = []

        opt = ListOption(self.config, "Test", "savelist", [])
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [])

        self.assertEqual(newopt.value, [""])

        stringopt = StringOption(newconfig, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(), "")

    def testSaveListOption4(self):
        testlist = ["элемент 1", "элемент 2", "элемент 3"]

        opt = ListOption(self.config, "Test", "savelist", [], separator="|")
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [], separator="|")

        self.assertEqual(newopt.value, testlist)

        stringopt = StringOption(newconfig, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(),
                         "элемент 1|элемент 2|элемент 3")

    def testSaveListOption5(self):
        testlist = ["элемент 1"]

        opt = ListOption(self.config, "Test", "savelist", [], separator="|")
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [], separator="|")

        self.assertEqual(newopt.value, testlist)

        stringopt = StringOption(newconfig, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(), "элемент 1")

    def testSaveListOption6(self):
        testlist = []

        opt = ListOption(self.config, "Test", "savelist", [], separator="|")
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [], separator="|")

        self.assertEqual(newopt.value, [""])

        stringopt = StringOption(newconfig, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(), "")

    def testSaveListOption7(self):
        testlist = [""]

        opt = ListOption(self.config, "Test", "savelist", [], separator="|")
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [], separator="|")

        self.assertEqual(newopt.value, testlist)

        stringopt = StringOption(newconfig, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(), "")

    def testSaveListOption8(self):
        testlist = [""]

        opt = ListOption(self.config, "Test", "savelist", [])
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [])

        self.assertEqual(newopt.value, testlist)

        stringopt = StringOption(self.config, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(), "")

    def testSaveListOption9(self):
        testlist = [""]

        opt = ListOption(self.config, "Test", "savelist", [], separator="|")
        opt.value = testlist

        newconfig = Config(self.path)
        newopt = ListOption(newconfig, "Test", "savelist", [], separator="|")

        self.assertEqual(newopt.value, testlist)

        stringopt = StringOption(self.config, "Test", "savelist", "")
        self.assertEqual(stringopt.value.strip(), "")

    def testStringListSection1(self):
        section = "listSection"
        paramname = "param_"

        testlist = ["Бла-бла-бла",
                    "Строка 1",
                    "Строка 2"]

        self.config.remove_section(section)
        opt = StringListSection(self.config, section, paramname)
        self.assertEqual(opt.value, [])

        # Установим список
        opt.value = testlist
        self.assertEqual(len(opt.value), 3)
        self.assertEqual(opt.value[0], "Бла-бла-бла")
        self.assertEqual(opt.value[1], "Строка 1")
        self.assertEqual(opt.value[2], "Строка 2")

        self.assertTrue(self.config.has_section(section))
        self.assertEqual(self.config.get(section, "param_0"), "Бла-бла-бла")
        self.assertEqual(self.config.get(section, "param_1"), "Строка 1")
        self.assertEqual(self.config.get(section, "param_2"), "Строка 2")
        self.config.remove_section(section)

    def testStringListSection2(self):
        section = "listSection"
        paramname = "param_"

        testlist = ["Бла-бла-бла",
                    "Строка 1",
                    "Строка 2"]

        self.config.remove_section(section)
        opt = StringListSection(self.config, section, paramname)
        self.assertEqual(opt.value, [])

        # Установим список
        opt.value = testlist

        opt_other = StringListSection(self.config, section, paramname)
        self.assertEqual(len(opt_other.value), 3)
        self.assertEqual(opt_other.value[0], "Бла-бла-бла")
        self.assertEqual(opt_other.value[1], "Строка 1")
        self.assertEqual(opt_other.value[2], "Строка 2")
        self.config.remove_section(section)

    def testStcStyle_01(self):
        defaultStyle = StcStyle()

        opt = StcStyleOption(self.config, "Test", "style_01", defaultStyle)
        self.assertEqual(opt.value.fore, "#AAAAAA")
        self.assertEqual(opt.value.back, "#111111")
        self.assertEqual(opt.value.bold, True)
        self.assertEqual(opt.value.italic, True)
        self.assertEqual(opt.value.underline, True)

    def testStcStyle_02(self):
        defaultStyle = StcStyle()

        opt = StcStyleOption(self.config, "Test", "style_02", defaultStyle)
        self.assertEqual(opt.value.fore, "#000000")
        self.assertEqual(opt.value.back, "#111111")
        self.assertEqual(opt.value.bold, True)
        self.assertEqual(opt.value.italic, True)
        self.assertEqual(opt.value.underline, True)

    def testStcStyle_03(self):
        defaultStyle = StcStyle()

        opt = StcStyleOption(self.config, "Test", "style_03", defaultStyle)
        self.assertEqual(opt.value.fore, "#000000")
        self.assertEqual(opt.value.back, "#FFFFFF")
        self.assertEqual(opt.value.bold, True)
        self.assertEqual(opt.value.italic, False)
        self.assertEqual(opt.value.underline, False)

    def testStcStyle_invalid_01(self):
        defaultStyle = StcStyle()

        opt = StcStyleOption(self.config,
                             "Test",
                             "style_invalid_01",
                             defaultStyle)
        self.assertEqual(opt.value.fore, "#000000")
        self.assertEqual(opt.value.back, "#FFFFFF")
        self.assertEqual(opt.value.bold, False)
        self.assertEqual(opt.value.italic, False)
        self.assertEqual(opt.value.underline, False)

    def testJSON_01(self):
        opt = JSONOption(self.config, "Test", "jsonval_none", None)
        self.assertEqual(opt.value, None)

    def testJSON_02(self):
        opt = JSONOption(self.config, "Test", "jsonval_01", None)
        self.assertEqual(opt.value, {})

    def testJSON_03(self):
        opt = JSONOption(self.config, "Test", "jsonval_02", None)
        self.assertEqual(opt.value, 'строка')

    def testJSON_04(self):
        opt = JSONOption(self.config, "Test", "jsonval_03", None)
        self.assertEqual(opt.value, [])

    def testJSON_05(self):
        opt = JSONOption(self.config, "Test", "jsonval_04", None)
        self.assertEqual(opt.value, [1, 2, 3])

    def testJSON_06(self):
        opt = JSONOption(self.config, "Test", "jsonval_05", None)
        self.assertEqual(opt.value['x'], 100)

    def testJSON_07(self):
        opt = JSONOption(self.config, "Test", "json_test", None)
        newopt = JSONOption(self.config, "Test", "json_test", None)

        opt.value = [1, 2, 3]

        self.assertEqual(newopt.value, [1, 2, 3])

    def testJSON_08(self):
        opt = JSONOption(self.config, "Test", "json_test", None)
        newopt = JSONOption(self.config, "Test", "json_test", None)

        opt.value = {'x': 100, 'y': 200}

        self.assertEqual(newopt.value, {'x': 100, 'y': 200})

    def testJSON_09(self):
        opt = JSONOption(self.config, "Test", "json_test", None)
        newopt = JSONOption(self.config, "Test", "json_test", None)

        opt.value = '111\n222\n333'

        self.assertEqual(newopt.value, '111\n222\n333')


class TrayConfigTest(unittest.TestCase):
    def setUp(self):
        self.path = "../test/testconfig.ini"
        self.config = Config(self.path)

        self.trayConfig = TrayConfig(self.config)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def testDefault(self):
        self.assertEqual(self.trayConfig.minimizeToTray.value, True)
        self.assertEqual(self.trayConfig.startIconized.value, False)
        self.assertEqual(self.trayConfig.alwaysShowTrayIcon.value, False)

    def testChange(self):
        newConfig = TrayConfig(self.config)

        newConfig.minimizeToTray.value = False
        self.assertEqual(self.trayConfig.minimizeToTray.value, False)

        newConfig.startIconized.value = True
        self.assertEqual(self.trayConfig.startIconized.value, True)

        newConfig.alwaysShowTrayIcon.value = True
        self.assertEqual(self.trayConfig.alwaysShowTrayIcon.value, True)


class EditorConfigTest(unittest.TestCase):
    def setUp(self):
        self.path = "../test/testconfig.ini"
        self.config = Config(self.path)

        self.editorConfig = EditorConfig(self.config)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def testDefault(self):
        self.assertEqual(self.editorConfig.lineNumbers.value, False)
        self.assertEqual(self.editorConfig.tabWidth.value, 4)
        self.assertEqual(self.editorConfig.fontSize.value, 10)
        self.assertEqual(self.editorConfig.fontName.value, "")
        self.assertEqual(self.editorConfig.fontIsBold.value, False)
        self.assertEqual(self.editorConfig.fontIsItalic.value, False)

    def testChange(self):
        newConfig = EditorConfig(self.config)

        newConfig.lineNumbers.value = True
        self.assertEqual(self.editorConfig.lineNumbers.value, True)

        newConfig.tabWidth.value = 8
        self.assertEqual(self.editorConfig.tabWidth.value, 8)

        newConfig.fontSize.value = 12
        self.assertEqual(self.editorConfig.fontSize.value, 12)

        newConfig.fontName.value = "Arial"
        self.assertEqual(self.editorConfig.fontName.value, "Arial")

        newConfig.fontIsBold.value = True
        self.assertEqual(self.editorConfig.fontIsBold.value, True)

        newConfig.fontIsItalic.value = True
        self.assertEqual(self.editorConfig.fontIsItalic.value, True)
