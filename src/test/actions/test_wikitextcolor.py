# -*- coding: utf-8 -*-

import unittest

import wx

from test.basetestcases import BaseOutWikerGUIMixin
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.actions.polyactionsid import TEXT_COLOR_STR_ID
from outwiker.gui.tester import Tester


class WikiTextColorActionTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.actionController = self.application.actionController
        self.action = self.application.actionController.getAction(TEXT_COLOR_STR_ID)

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

    def test_empty_editor_set_color_named(self):
        def dialog_func(dialog):
            colordata = wx.ColourData()
            colordata.SetColour(wx.RED)
            dialog.SetDataForTest(colordata)
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%red%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_empty_editor_set_color(self):
        def dialog_func(dialog):
            colordata = wx.ColourData()
            colordata.SetColour(wx.Colour(10, 20, 30))
            dialog.SetDataForTest(colordata)
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)
        self.action.run(None)

        result_right = '''%#0a141e%

%%'''
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_inline(self):
        def dialog_func(dialog):
            colordata = wx.ColourData()
            colordata.SetColour(wx.BLUE)
            dialog.SetDataForTest(colordata)
            return wx.ID_OK

        Tester.dialogTester.append(dialog_func)

        text = 'Блок текста бла-бла-бла'
        self.editor.SetText(text)
        self.editor.SetSelection(5, 11)
        self.action.run(None)

        result_right = 'Блок %blue%текста%% бла-бла-бла'
        result = self.editor.GetText()

        self.assertEqual(result, result_right)

    def test_incapsulate_block_01(self):
        def dialog_func(dialog):
            colordata = wx.ColourData()
            colordata.SetColour(wx.BLUE)
            dialog.SetDataForTest(colordata)
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

    def test_incapsulate_block_02(self):
        def dialog_func(dialog):
            colordata = wx.ColourData()
            colordata.SetColour(wx.BLUE)
            dialog.SetDataForTest(colordata)
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
