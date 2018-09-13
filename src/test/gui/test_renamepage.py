# -*- coding: utf-8 -*-

from os.path import basename
import unittest

from outwiker.core.commands import renamePage
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUIMixin


class RenamePageGuiTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты переименования страниц
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot, "Страница 4", [])

        Tester.dialogTester.clear()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        Tester.dialogTester.clear()

    def test_rename_simple(self):
        page = self.wikiroot['Страница 1']
        renamePage(page, 'Новое имя')

        self.assertIsNone(self.wikiroot['Страница 1'])
        self.assertIsNotNone(self.wikiroot['Новое имя'])
        self.assertEqual(page.display_title, 'Новое имя')
        self.assertIsNone(page.alias)

    def test_rename_simple_spaces(self):
        page = self.wikiroot['Страница 1']
        renamePage(page, '   Новое имя   ')

        self.assertIsNone(self.wikiroot['Страница 1'])
        self.assertIsNotNone(self.wikiroot['Новое имя'])
        self.assertEqual(page.display_title, 'Новое имя')
        self.assertIsNone(page.alias)

    def test_rename_special_chars(self):
        page = self.wikiroot['Страница 1']
        renamePage(page, 'Тест ><|?*:"\\/#% проверка')

        self.assertIsNone(self.wikiroot['Страница 1'])
        self.assertIsNotNone(self.wikiroot['Тест ___________ проверка'])
        self.assertEqual(page.display_title, 'Тест ><|?*:"\\/#% проверка')
        self.assertEqual(page.alias, 'Тест ><|?*:"\\/#% проверка')

    def test_rename_duplicate_01(self):
        renamePage(self.wikiroot['Страница 2'], 'Страница 1')

        self.assertIsNone(self.wikiroot['Страница 2'])
        self.assertIsNotNone(self.wikiroot['Страница 1 (1)'])
        self.assertEqual(self.wikiroot['Страница 1 (1)'].alias, 'Страница 1')
        self.assertEqual(self.wikiroot['Страница 1 (1)'].display_title,
                         'Страница 1')

    def test_rename_duplicate_02(self):
        renamePage(self.wikiroot['Страница 2'], 'Страница 1')
        renamePage(self.wikiroot['Страница 4'], 'Страница 1')

        self.assertIsNone(self.wikiroot['Страница 2'])
        self.assertIsNotNone(self.wikiroot['Страница 1 (1)'])
        self.assertEqual(self.wikiroot['Страница 1 (1)'].alias, 'Страница 1')
        self.assertEqual(self.wikiroot['Страница 1 (1)'].display_title,
                         'Страница 1')

        self.assertIsNone(self.wikiroot['Страница 4'])
        self.assertIsNotNone(self.wikiroot['Страница 1 (2)'])
        self.assertEqual(self.wikiroot['Страница 1 (2)'].alias, 'Страница 1')
        self.assertEqual(self.wikiroot['Страница 1 (2)'].display_title,
                         'Страница 1')

    def test_alias(self):
        self.wikiroot['Страница 1'].alias = 'Бла-бла-бла'
        renamePage(self.wikiroot['Страница 1'], 'Викистраница')

        self.assertIsNotNone(self.wikiroot['Викистраница'])
        self.assertIsNone(self.wikiroot['Викистраница'].alias)
        self.assertEqual(self.wikiroot['Викистраница'].title, 'Викистраница')
        self.assertEqual(self.wikiroot['Викистраница'].display_title,
                         'Викистраница')

    def test_some_name(self):
        page = self.wikiroot['Страница 1']
        renamePage(page, 'Страница 1')

        self.assertIsNotNone(self.wikiroot['Страница 1'])
        self.assertEqual(page.display_title, 'Страница 1')
        self.assertIsNone(page.alias)

    def test_some_name_spaces(self):
        page = self.wikiroot['Страница 1']
        renamePage(page, '    Страница 1    ')

        self.assertIsNotNone(self.wikiroot['Страница 1'])
        self.assertEqual(page.display_title, 'Страница 1')
        self.assertIsNone(page.alias)

    def testCommand_02(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "Страница 2")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["Страница 2"])
        self.assertIsNotNone(self.wikiroot["Страница 2 (1)"])

    def testCommand_03(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "safsd/Абырвалг")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["safsd_Абырвалг"])

    def testCommand_04(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["(1)"])

    def testCommand_05(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "    \t\n")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["(1)"])

    def testCommand_begins_underlines_01(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "__asdasdf")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["--asdasdf"])
        self.assertEqual(self.wikiroot["--asdasdf"].alias, '__asdasdf')

    def testCommand_begins_underlines_02(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "##asdasdf")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["--asdasdf"])
        self.assertEqual(self.wikiroot["--asdasdf"].alias, '##asdasdf')

    def testCommand_07_readonly(self):
        Tester.dialogTester.appendOk()
        self.wikiroot["Страница 1"].readonly = True

        renamePage(self.wikiroot["Страница 1"], "Абырвалг")

        self.assertIsNotNone(self.wikiroot["Страница 1"])
        self.assertIsNone(self.wikiroot["Абырвалг"])
        self.assertEqual(Tester.dialogTester.count, 0)

    def testCommand_double_dots(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "..")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["(1)"])
        self.assertEqual(self.wikiroot["(1)"].alias, '..')

    def testCommand_dots(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "...")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot["..."])
        self.assertIsNone(self.wikiroot["..."].alias)

    def testCommand_09(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "..\\")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot[".._"])

    def testCommand_10(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "../sadfasdf")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot[".._sadfasdf"])

    def testCommand_11(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 1"], "..\\Абырвалг")

        self.assertIsNone(self.wikiroot["Страница 1"])
        self.assertIsNotNone(self.wikiroot[".._Абырвалг"])

    def testCommand_12(self):
        renamePage(self.wikiroot["Страница 2/Страница 3"], "Абырвалг")

        self.assertIsNone(self.wikiroot["Страница 2/Страница 3"])
        self.assertIsNotNone(self.wikiroot["Страница 2"])
        self.assertIsNotNone(self.wikiroot["Страница 2/Абырвалг"])

    def testCommand_13(self):
        Tester.dialogTester.appendError()
        renamePage(self.wikiroot["Страница 2/Страница 3"], "..")

        self.assertIsNone(self.wikiroot["Страница 2/Страница 3"])
        self.assertIsNone(self.wikiroot[".."])

    def testCommand_14_root(self):
        Tester.dialogTester.appendOk()
        renamePage(self.wikiroot, "Абырвалг")

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(self.wikiroot.title, basename(self.wikiroot.path))
