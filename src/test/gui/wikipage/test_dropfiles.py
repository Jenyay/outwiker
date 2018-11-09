# -*- coding: utf-8 -*-

import os.path
import unittest

from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class TextEditorTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Test for drop files to the wiki editor
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testpage = WikiPageFactory().create(self.wikiroot, "Страница", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.testpage

        self.editor = self.application.mainWindow.pagePanel.pageView.codeEditor
        self.dropTarget = self.editor.dropTarget

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_drop_empty(self):
        files = []
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = ''
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_single_external(self):
        files = [os.path.abspath('../test/images/icon.png')]
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = files[0]
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_several_external(self):
        files = [
            os.path.abspath('../test/images/icon.png'),
            os.path.abspath('../test/images/first.png'),
        ]
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = ' '.join(files)
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_single_attach(self):
        attach = Attachment(self.testpage)
        attach.attach(['../test/images/icon.png'])

        files = sorted(attach.attachmentFull)
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = 'Attach:icon.png'
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_several_attach(self):
        attach = Attachment(self.testpage)
        attach.attach(['../test/images/icon.png', '../test/images/first.png'])

        files = sorted(attach.attachmentFull)
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = 'Attach:first.png Attach:icon.png'
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_several_mixed(self):
        attach = Attachment(self.testpage)
        attach.attach(['../test/images/first.png'])

        files = (attach.attachmentFull +
                 [os.path.abspath('../test/images/icon.png')])
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = ('Attach:first.png '
                         + os.path.abspath('../test/images/icon.png'))

        self.assertEqual(self.editor.GetText(), expected_text)
