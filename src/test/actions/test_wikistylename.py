# -*- coding: utf-8 -*-

import unittest

import wx

from test.basetestcases import BaseOutWikerGUIMixin
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.actions.wikistyle import WikiStyleOnlyAction
from outwiker.gui.tester import Tester


class WikiStyleNameActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.actionController = self.application.actionController
        self.action = self.application.actionController.getAction(WikiStyleOnlyAction.stringId)

        WikiPageFactory().create(self.wikiroot, "wiki", [])
        self.testedPage = self.wikiroot["wiki"]
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.testedPage

        self.editor = self.application.mainWindow.pagePanel.pageView.codeEditor
        Tester.dialogTester.clear()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        Tester.dialogTester.clear()

    def test_empty_editor_set_style_name(self):
        def dialog_func(dialog):
            dialog.SetDataForTest('test-style')
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%test-style%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_inline(self):
        def dialog_func(dialog):
            dialog.SetDataForTest('test-style')
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)

        text = 'Блок текста бла-бла-бла'
        self.editor.SetText(text)
        self.editor.SetSelection(5, 11)
        self.action.run(None)

        result_right = 'Блок %test-style%текста%% бла-бла-бла'
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_block(self):
        def dialog_func(dialog):
            dialog.SetDataForTest('test-style')
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)

        text = '''Блок текста
Бла-бла-бла

Еще текст'''
        self.editor.SetText(text)
        self.editor.SetSelection(12, 23)
        self.action.run(None)

        result_right = '''Блок текста
%test-style%
Бла-бла-бла
%%

Еще текст'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)
