# -*- coding: utf-8 -*-

import unittest

import wx

from test.basetestcases import BaseOutWikerGUIMixin
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.actions.wikistyle import WikiStyleAdvancedAction
from outwiker.gui.tester import Tester


class WikiStyleAdvancedActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.actionController = self.application.actionController
        self.action = self.application.actionController.getAction(WikiStyleAdvancedAction.stringId)

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

    def test_empty(self):
        Tester.dialogTester.appendOk()
        self.action.run(None)

        result_right = '''%%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_empty_editor_set_color_named(self):
        def dialog_func(dialog):
            dialog.setTextColor(wx.RED)
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%red%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_empty_editor_set_color(self):
        def dialog_func(dialog):
            dialog.setTextColor(wx.Colour(10, 20, 30))
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%color="#0a141e"%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_empty_editor_set_bgcolor_named(self):
        def dialog_func(dialog):
            dialog.setBackgroundColor(wx.RED)
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%bg-red%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_empty_editor_set_bgcolor(self):
        def dialog_func(dialog):
            dialog.setBackgroundColor(wx.Colour(10, 20, 30))
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%bgcolor="#0a141e"%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_empty_editor_set_custom_CSS(self):
        def dialog_func(dialog):
            dialog.setCustomCSS('font-weight: bold;')
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%style="font-weight: bold;"%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_empty_editor_set_many_params(self):
        def dialog_func(dialog):
            dialog.setCustomCSS('font-weight: bold;')
            dialog.setBackgroundColor(wx.RED)
            dialog.setTextColor(wx.BLUE)
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%blue bg-red style="font-weight: bold;"%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_block_01(self):
        def dialog_func(dialog):
            dialog.setTextColor(wx.BLUE)
            return wx.ID_OK
        Tester.dialogTester.append(dialog_func)

        text = 'Блок текста'
        self.editor.SetText(text)
        self.editor.SetSelection(0, len(text))
        self.action.run(None)

        result_right = '''%blue%
Блок текста
%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_block_02(self):
        def dialog_func(dialog):
            dialog.setTextColor(wx.BLUE)
            return wx.ID_OK
        Tester.dialogTester.append(dialog_func)

        text = '''Блок текста
Бла-бла-бла

Еще текст'''
        self.editor.SetText(text)
        self.editor.SetSelection(12, 23)
        self.action.run(None)

        result_right = '''Блок текста
%blue%
Бла-бла-бла
%%

Еще текст'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_block_03(self):
        def dialog_func(dialog):
            dialog.setTextColor(wx.BLUE)
            return wx.ID_OK
        Tester.dialogTester.append(dialog_func)

        text = '''Блок текста
Бла-бла-бла
Еще текст'''
        self.editor.SetText(text)
        self.editor.SetSelection(12, 23)
        self.action.run(None)

        result_right = '''Блок текста
%blue%
Бла-бла-бла
%%
Еще текст'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_inline(self):
        def dialog_func(dialog):
            dialog.setTextColor(wx.BLUE)
            return wx.ID_OK
        Tester.dialogTester.append(dialog_func)

        text = 'Блок текста бла-бла-бла'
        self.editor.SetText(text)
        self.editor.SetSelection(5, 11)
        self.action.run(None)

        result_right = 'Блок %blue%текста%% бла-бла-бла'
        result = self.editor.GetText()

        self.assertEqual(result, result_right)
