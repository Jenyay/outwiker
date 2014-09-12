# -*- coding: UTF-8 -*-

from basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.commands import movePage
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester
from test.utils import removeWiki


class MovePageGuiTest (BaseMainWndTest):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot, u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 4", [])

        Tester.dialogTester.clear()
        Application.wikiroot = None


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.selectedPage = None
        Application.wikiroot = None
        removeWiki (self.path)


    def testCommandMove_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        Tester.dialogTester.appendOk()

        movePage (self.wikiroot[u"Страница 1"], self.wikiroot[u"Страница 1"])

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_02 (self):
        Tester.dialogTester.appendOk()

        movePage (self.wikiroot[u"Страница 1"], self.wikiroot[u"Страница 1"])

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_03 (self):
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot)
        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)


    def testCommandMove_04 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        movePage (self.wikiroot[u"Страница 1"], self.wikiroot)
        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)


    def testCommandMove_05 (self):
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot[u"Страница 2"])

        self.assertEqual (self.wikiroot[u"Страница 1"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2/Страница 1"], None)


    def testCommandMove_06 (self):
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot[u"Страница 2/Страница 3"])

        self.assertEqual (self.wikiroot[u"Страница 1"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2/Страница 3/Страница 1"], None)


    def testCommandMove_07 (self):
        Tester.dialogTester.appendOk()

        movePage (self.wikiroot[u"Страница 3"], self.wikiroot[u"Страница 2"])

        self.assertNotEqual (self.wikiroot[u"Страница 3"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2/Страница 3"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_08 (self):
        Tester.dialogTester.appendOk()

        movePage (self.wikiroot[u"Страница 2/Страница 3"], self.wikiroot)

        self.assertNotEqual (self.wikiroot[u"Страница 3"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2/Страница 3"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_09 (self):
        self.assertRaises (AssertionError, movePage, self.wikiroot[u"Страница 1"], None)
        self.assertRaises (AssertionError, movePage, None, self.wikiroot)


    def testCommandMove_10_readonly (self):
        self.wikiroot[u"Страница 1"].readonly = True
        self.wikiroot[u"Страница 2/Страница 3"].readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot[u"Страница 2/Страница 3"])

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_11_readonly (self):
        self.wikiroot[u"Страница 1"].readonly = False
        self.wikiroot[u"Страница 2/Страница 3"].readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot[u"Страница 2/Страница 3"])

        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3/Страница 1"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_12_readonly (self):
        self.wikiroot[u"Страница 1"].readonly = True
        self.wikiroot[u"Страница 2/Страница 3"].readonly = False

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot[u"Страница 2/Страница 3"])

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_13_readonly (self):
        self.wikiroot[u"Страница 1"].readonly = True
        self.wikiroot.readonly = False

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot)

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_14_readonly (self):
        self.wikiroot[u"Страница 1"].readonly = True
        self.wikiroot.readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot)

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_15_readonly (self):
        self.wikiroot[u"Страница 1"].readonly = False
        self.wikiroot.readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot[u"Страница 1"], self.wikiroot)

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)
