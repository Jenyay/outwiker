# -*- coding: utf-8 -*-

import os.path
import unittest

from outwiker.core.attachment import Attachment
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class TextEditorDropTargetTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Test for drop files to the HTML editor
    """

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testpage = TextPageFactory().create(self.wikiroot, "Страница", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.testpage

        self.editor = self.application.mainWindow.pagePanel.pageView.GetEditor()
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
        files = [os.path.abspath('testdata/images/icon.png')]
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = files[0]
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_several_external(self):
        files = [
            os.path.abspath('testdata/images/icon.png'),
            os.path.abspath('testdata/images/first.png'),
        ]
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = ' '.join(files)
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_single_attach(self):
        attach = Attachment(self.testpage)
        attach.attach(['testdata/images/icon.png'])

        files = sorted(attach.attachmentFull)
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = 'icon.png'
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_several_attach(self):
        attach = Attachment(self.testpage)
        attach.attach(['testdata/images/icon.png',
                      'testdata/images/first.png'])

        files = sorted(attach.attachmentFull)
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = 'first.png icon.png'
        self.assertEqual(self.editor.GetText(), expected_text)

    def test_drop_several_mixed(self):
        attach = Attachment(self.testpage)
        attach.attach(['testdata/images/first.png'])

        files = (attach.attachmentFull +
                 [os.path.abspath('testdata/images/icon.png')])
        self.dropTarget.OnDropFiles(0, 0, files)

        expected_text = ('first.png '
                         + os.path.abspath('testdata/images/icon.png'))

        self.assertEqual(self.editor.GetText(), expected_text)
