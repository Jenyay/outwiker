# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp
import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUIMixin


class AttachPanelTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])

        self.page = self.wikiroot["Страница 2/Страница 3"]

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png", "add.png", "anchor.png", "файл с пробелами.tmp", "dir"]
        self.fullFilesPath = [os.path.join(filesPath, fname) for fname in self.files]

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testEmpty(self):
        self.assertNotEqual(None, self.mainWindow.attachPanel.panel)
        self.assertNotEqual(None, self.mainWindow.attachPanel.panel.attachList)
        self.assertNotEqual(None, self.mainWindow.attachPanel.panel.toolBar)
        self.assertEqual(0, self.mainWindow.attachPanel.panel.attachList.GetItemCount())

    def testAttach1(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.page
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

        attach.removeAttach([self.files[0]])
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath) - 1)

    def testAttach2(self):
        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.page

        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

    def testAttach3(self):
        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.page

        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath[:1])

        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), 1)
        attach.attach(self.fullFilesPath[1:])

        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

    def testAttach4(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.page
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

        self.application.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), 0)

    def testAttach5(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.page
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

        self.application.wikiroot = None
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), 0)

    def testAttach6(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.page
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

        self.application.wikiroot.selectedPage = None
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), 0)

    def testAttach7(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.wikiroot.selectedPage = self.page
        self.application.wikiroot = self.wikiroot

        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

        self.application.wikiroot.selectedPage = None
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), 0)

    def testAttach8(self):
        # Не подключаем к self.application созданную вики. Панель не должна реагировать на прикрепленные файлы
        self.wikiroot.selectedPage = self.page

        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), 0)

    def testReloading(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.wikiroot.selectedPage = self.page
        self.application.wikiroot = self.wikiroot

        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(self.fullFilesPath))

        # Создадим другую независимую вики
        newpath = mkdtemp(prefix='Абыр Абырвалг')
        newwikiroot = WikiDocument.create(newpath)

        TextPageFactory().create(newwikiroot, "Новая страница 1", [])
        TextPageFactory().create(newwikiroot, "Новая страница 2", [])

        filesPath = "../test/samplefiles/"
        newfiles = ["accept.png", "add.png", "anchor.png"]
        newfullFilesPath = [os.path.join(filesPath, fname) for fname in newfiles]

        newattach = Attachment(newwikiroot["Новая страница 1"])
        newattach.attach(newfullFilesPath)
        newwikiroot.selectedPage = newwikiroot["Новая страница 1"]

        self.application.wikiroot = newwikiroot
        self.assertEqual(self.mainWindow.attachPanel.panel.attachList.GetItemCount(), len(newfullFilesPath))

        self.application.wikiroot.selectedPage = None
        self.application.wikiroot = None
        removeDir(newpath)
