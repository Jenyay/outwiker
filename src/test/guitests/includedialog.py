#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path

import wx

from basemainwnd import BaseMainWndTest
from outwiker.pages.wiki.actions.include import IncludeDialog, IncludeDialogController
from outwiker.core.application import Application
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.core.attachment import Attachment
from test.utils import removeWiki


class IncludeDialogTest (BaseMainWndTest):
    """
    Тесты диалога для вставки команды (:include:)
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)
        self._dialog = IncludeDialog (Application.mainWindow)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory.create (self.wikiroot, u"Викистраница", [])
        self.testedPage = self.wikiroot[u"Викистраница"]

        filesPath = u"../test/samplefiles/"
        self.files = [u"accept.png", u"add.png", u"anchor.png", u"файл с пробелами.tmp", u"dir"]
        self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]

        Attachment (self.testedPage).attach (self.fullFilesPath)


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def testCancel (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        self._dialog.SetModalResult (wx.ID_CANCEL)
        result = controller.getDialogResult()

        self.assertEqual (result, None)
        self.assertEqual (len (self._dialog.attachmentList), 5)


    def test_01 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:include Attach:accept.png:)")


    def test_02 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 1
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:include Attach:add.png:)")


    def test_03 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 3
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:include Attach:dir:)")


    def test_04 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 4
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:include Attach:файл с пробелами.tmp:)")


    def test_05 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 400
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:include Attach:accept.png:)")


    def test_encoding_01 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png encoding="utf-16":)')


    def test_encoding_02 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 6
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png encoding="mac_cyrillic":)')


    def test_encoding_04 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 600
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png:)')


    def test_escapeHtml_01 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = True
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png htmlescape:)')


    def test_escapeHtml_02 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = True
        self._dialog.parseWiki = False

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png encoding="utf-16" htmlescape:)')


    def test_wikiparse_01 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 0
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = True

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png wikiparse:)')


    def test_wikiparse_02 (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = False
        self._dialog.parseWiki = True

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png encoding="utf-16" wikiparse:)')


    def test_wikiparse_escapehtml (self):
        controller = IncludeDialogController (self._dialog, self.testedPage)
        
        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedAttachment = 0
        self._dialog.selectedEncoding = 1
        self._dialog.escapeHtml = True
        self._dialog.parseWiki = True

        result = controller.getDialogResult()

        self.assertEqual (result, u'(:include Attach:accept.png encoding="utf-16" htmlescape wikiparse:)')
