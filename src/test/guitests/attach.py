# -*- coding: UTF-8 -*-

import os.path

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from test.utils import removeWiki
from outwiker.core.attachment import Attachment


class AttachPanelTest (BaseMainWndTest):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])

        self.page = self.wikiroot[u"Страница 2/Страница 3"]

        filesPath = u"../test/samplefiles/"
        self.files = [u"accept.png", u"add.png", u"anchor.png", u"файл с пробелами.tmp", u"dir"]
        self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]


    def testEmpty (self):
        self.assertNotEqual (None, self.wnd.attachPanel.panel)
        self.assertNotEqual (None, self.wnd.attachPanel.panel.attachList)
        self.assertNotEqual (None, self.wnd.attachPanel.panel.toolBar)
        self.assertEqual (0, self.wnd.attachPanel.panel.attachList.GetItemCount())


    def testAttach1 (self):
        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        Application.wikiroot = self.wikiroot
        Application.wikiroot.selectedPage = self.page
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))

        attach.removeAttach ([self.files[0]])
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath) - 1)


    def testAttach2 (self):
        Application.wikiroot = self.wikiroot
        Application.wikiroot.selectedPage = self.page

        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))


    def testAttach3 (self):
        Application.wikiroot = self.wikiroot
        Application.wikiroot.selectedPage = self.page

        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath[:1])

        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), 1)
        attach.attach (self.fullFilesPath[1:])

        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))


    def testAttach4 (self):
        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        Application.wikiroot = self.wikiroot
        Application.wikiroot.selectedPage = self.page
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))

        Application.wikiroot.selectedPage = self.wikiroot[u"Страница 1"]
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), 0)


    def testAttach5 (self):
        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        Application.wikiroot = self.wikiroot
        Application.wikiroot.selectedPage = self.page
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))

        Application.wikiroot = None
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), 0)


    def testAttach6 (self):
        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        Application.wikiroot = self.wikiroot
        Application.wikiroot.selectedPage = self.page
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))

        Application.wikiroot.selectedPage = None
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), 0)


    def testAttach7 (self):
        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        self.wikiroot.selectedPage = self.page
        Application.wikiroot = self.wikiroot

        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))

        Application.wikiroot.selectedPage = None
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), 0)


    def testAttach8 (self):
        # Не подключаем к Application созданную вики. Панель не должна реагировать на прикрепленные файлы
        self.wikiroot.selectedPage = self.page

        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), 0)


    def testReloading (self):
        attach = Attachment (self.page)
        attach.attach (self.fullFilesPath)

        self.wikiroot.selectedPage = self.page
        Application.wikiroot = self.wikiroot

        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (self.fullFilesPath))

        # Создадим другую независимую вики
        newpath = u"../test/testwiki2"
        newwikiroot = WikiDocument.create (newpath)

        TextPageFactory().create (newwikiroot, u"Новая страница 1", [])
        TextPageFactory().create (newwikiroot, u"Новая страница 2", [])

        filesPath = u"../test/samplefiles/"
        newfiles = [u"accept.png", u"add.png", u"anchor.png"]
        newfullFilesPath = [os.path.join (filesPath, fname) for fname in newfiles]

        newattach = Attachment (newwikiroot[u"Новая страница 1"])
        newattach.attach (newfullFilesPath)
        newwikiroot.selectedPage = newwikiroot[u"Новая страница 1"]

        Application.wikiroot = newwikiroot
        self.assertEqual (self.wnd.attachPanel.panel.attachList.GetItemCount(), len (newfullFilesPath))

        Application.wikiroot.selectedPage = None
        Application.wikiroot = None
        removeWiki (newpath)
