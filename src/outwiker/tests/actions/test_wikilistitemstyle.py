# -*- coding: utf-8 -*-

from dataclasses import dataclass
import unittest

import wx

from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.actions.listitemstyle import ListItemStyleAction
from outwiker.pages.wiki.gui.listitemstyledialog import ListItemStyleDialog
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin



@dataclass(frozen=True)
class SingleTestParams:
     init_text: str
     init_position: int
     dialog_selection: int
     dialog_result: int
     expected_text: str
     expected_position: int


class WikiListItemStyleTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.actionController = self.application.actionController
        self.action = self.application.actionController.getAction(
            ListItemStyleAction.stringId)

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

    def test_all(self):
        params = [
                SingleTestParams(init_text='',
                                 init_position = 0,
                                 dialog_selection = 0,
                                 dialog_result = wx.ID_CANCEL,
                                 expected_text = '',
                                 expected_position = 0),
                SingleTestParams(init_text='',
                                 init_position = 0,
                                 dialog_selection = 0,
                                 dialog_result = wx.ID_OK,
                                 expected_text = '* ',
                                 expected_position = 2),
                SingleTestParams(init_text='',
                                 init_position = 0,
                                 dialog_selection = 1,
                                 dialog_result = wx.ID_OK,
                                 expected_text = '* [ ] ',
                                 expected_position = 6),
                SingleTestParams(init_text='bla-bla-bla',
                                 init_position = 3,
                                 dialog_selection = 1,
                                 dialog_result = wx.ID_OK,
                                 expected_text = '* [ ] bla-bla-bla',
                                 expected_position = 3 + 6),
                SingleTestParams(init_text='bla-bla-bla',
                                 init_position = 11,
                                 dialog_selection = 1,
                                 dialog_result = wx.ID_OK,
                                 expected_text = '* [ ] bla-bla-bla',
                                 expected_position = 11 + 6),
                SingleTestParams(init_text='* bla-bla-bla',
                                 init_position = 2,
                                 dialog_selection = 1,
                                 dialog_result = wx.ID_OK,
                                 expected_text = '* [ ] bla-bla-bla',
                                 expected_position = 6),
                SingleTestParams(init_text='** bla-bla-bla',
                                 init_position = 3,
                                 dialog_selection = 1,
                                 dialog_result = wx.ID_OK,
                                 expected_text = '** [ ] bla-bla-bla',
                                 expected_position = 7),
                SingleTestParams(init_text='** bla-bla-bla',
                                 init_position = 3,
                                 dialog_selection = 0,
                                 dialog_result = wx.ID_OK,
                                 expected_text = '** bla-bla-bla',
                                 expected_position = 3),
                ]

        for param in params:
            with self.subTest():
                def dialog_func(dialog: ListItemStyleDialog):
                    dialog.SetSelection(param.dialog_selection)
                    return param.dialog_result

                Tester.dialogTester.append(dialog_func)

                self.editor.SetText(param.init_text)
                self.editor.SetCurrentPosition(param.init_position)
                self.action.run(None)

                result = self.editor.GetText()
                cursor_pos = self.editor.GetCurrentPosition()

                self.assertEqual(result, param.expected_text)
                self.assertEqual(cursor_pos, param.expected_position)
