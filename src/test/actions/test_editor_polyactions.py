# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.commands import getClipboardText
from test.basetestcases import BaseOutWikerGUITest
from outwiker.actions.polyactionsid import *


class BaseEditorPolyactionsTest(BaseOutWikerGUITest, metaclass=ABCMeta):
    @abstractmethod
    def _createPage(self):
        pass

    @abstractmethod
    def _getEditor(self):
        pass

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.page = self._createPage()
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.page

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_LineDuplicate_01(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = 'Строка 1\nСтрока 1\nСтрока 2\nСтрока 3'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_LineDuplicate_02(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3'
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = 'Строка 1\nСтрока 2\nСтрока 2\nСтрока 3'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_LineDuplicate_03(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = ''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = '\n'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_MoveLinesDown_01(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = 'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_MoveLinesDown_02(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 15)

        result = 'Строка 3\nСтрока 1\nСтрока 2\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_MoveLinesUp_01(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = 'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_MoveLinesUp_02(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(10, 21)

        result = 'Строка 2\nСтрока 3\nСтрока 1\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_MoveLinesUpDown_empty(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = ''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = ''

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'), result)

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'), result)

    def test_DeleteCurrentLine_01(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = 'Строка 2\nСтрока 3\nСтрока 4'

        actionController.getAction(DELETE_CURRENT_LINE).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_DeleteCurrentLine_02(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(10, 10)

        result = 'Строка 1\nСтрока 3\nСтрока 4'

        actionController.getAction(DELETE_CURRENT_LINE).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_DeleteCurrentLine_03_empty(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = ''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = ''

        actionController.getAction(DELETE_CURRENT_LINE).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         result)

    def test_GotoNextWord_01(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'слово слово2 ещеоднослово'
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_NEXT_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 6)

        actionController.getAction(GOTO_NEXT_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

        actionController.getAction(GOTO_NEXT_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GotoPrevWord_01(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = 'слово слово2 ещеоднослово'
        editor.SetText(text)
        editor.GotoPos(25)

        actionController.getAction(GOTO_PREV_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

        actionController.getAction(GOTO_PREV_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 6)

        actionController.getAction(GOTO_PREV_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GotoWord_empty(self):
        editor = self._getEditor()
        actionController = self.application.actionController
        text = ''
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_NEXT_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

        actionController.getAction(GOTO_PREV_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_01(self):
        text = ''
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_02(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_03(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(3)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_04(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(5)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_05(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(6)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_06(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(7)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_07(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(13)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_08(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(14)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_09(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(25)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordEnd_01(self):
        text = ''
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordEnd_02(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_03(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(1)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_04(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(6)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_05(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(12)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_06(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(13)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_07(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(14)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_08(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(25)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_CopyLineToClipboard_01(self):
        text = ''
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text, '')

    def test_CopyLineToClipboard_02(self):
        text = '\n'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace('\r\n', '\n'), '\n')

    def test_CopyLineToClipboard_03(self):
        text = 'Строка 1'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace('\r\n', '\n'), 'Строка 1')

    def test_CopyLineToClipboard_04(self):
        text = 'Строка 1\n'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace('\r\n', '\n'), 'Строка 1\n')

    def test_CopyLineToClipboard_05(self):
        text = 'Строка 1\nСтрока 2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace('\r\n', '\n'), 'Строка 2')

    def test_CopyLineToClipboard_06(self):
        text = 'Строка 1\nСтрока 2\n'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace('\r\n', '\n'), 'Строка 2\n')

    def test_CutLineToClipboard_01(self):
        text = ''
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText()
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, '')
        self.assertEqual(newtext, '')

    def test_CutLineToClipboard_02(self):
        text = 'Строка 1'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'Строка 1')
        self.assertEqual(newtext, '')

    def test_CutLineToClipboard_03(self):
        text = 'Строка 1\n'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'Строка 1\n')
        self.assertEqual(newtext, '')

    def test_CutLineToClipboard_04(self):
        text = 'Строка 1\nСтрока 2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'Строка 1\n')
        self.assertEqual(newtext, 'Строка 2')

    def test_CutLineToClipboard_05(self):
        text = 'Строка 1\nСтрока 2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'Строка 2')
        self.assertEqual(newtext, 'Строка 1\n')

    def test_CutLineToClipboard_06(self):
        text = 'Строка 1\nСтрока 2\nСтрока 3'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'Строка 2\n')
        self.assertEqual(newtext, 'Строка 1\nСтрока 3')

    def test_CopyWordToClipboard_01(self):
        text = ''
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        self.assertEqual(cb_text, '')

    def test_CopyWordToClipboard_02(self):
        text = 'слово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        self.assertEqual(cb_text, 'слово')

    def test_CopyWordToClipboard_03(self):
        text = 'слово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(2)

        actionController.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        self.assertEqual(cb_text, 'слово')

    def test_CopyWordToClipboard_04(self):
        text = 'слово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(5)

        actionController.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        self.assertEqual(cb_text, 'слово')

    def test_CopyWordToClipboard_05(self):
        text = ' слово '
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(1)

        actionController.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        self.assertEqual(cb_text, 'слово')

    def test_CopyWordToClipboard_06(self):
        text = ' слово слово2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(7)

        actionController.getAction(CLIPBOARD_COPY_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        self.assertEqual(cb_text, 'слово2')

    def test_CutWordToClipboard_01(self):
        text = ''
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, '')
        self.assertEqual(newtext, '')

    def test_CutWordToClipboard_02(self):
        text = 'слово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово')
        self.assertEqual(newtext, '')

    def test_CutWordToClipboard_03(self):
        text = 'слово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(2)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово')
        self.assertEqual(newtext, '')

    def test_CutWordToClipboard_04(self):
        text = 'слово'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(5)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово')
        self.assertEqual(newtext, '')

    def test_CutWordToClipboard_05(self):
        text = 'слово слово2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово')
        self.assertEqual(newtext, ' слово2')

    def test_CutWordToClipboard_06(self):
        text = 'слово слово2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(5)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово')
        self.assertEqual(newtext, ' слово2')

    def test_CutWordToClipboard_07(self):
        text = 'слово слово2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(6)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово2')
        self.assertEqual(newtext, 'слово ')

    def test_CutWordToClipboard_08(self):
        text = 'слово слово2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(8)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово2')
        self.assertEqual(newtext, 'слово ')

    def test_CutWordToClipboard_09(self):
        text = 'слово слово2'
        editor = self._getEditor()
        actionController = self.application.actionController
        editor.SetText(text)
        editor.GotoPos(12)

        actionController.getAction(CLIPBOARD_CUT_WORD).run(None)
        cb_text = getClipboardText().replace('\r\n', '\n')
        newtext = editor.GetText().replace('\r\n', '\n')

        self.assertEqual(cb_text, 'слово2')
        self.assertEqual(newtext, 'слово ')


class WikiEditorPolyactionsTest(BaseEditorPolyactionsTest):
    """
    Test polyactions for wiki pages
    """
    def _createPage(self):
        return WikiPageFactory().create(self.wikiroot, "Викистраница", [])

    def _getEditor(self):
        return self.application.mainWindow.pagePanel.pageView.codeEditor


class HtmlEditorPolyactionsTest(BaseEditorPolyactionsTest):
    """
    Test polyactions for HTML pages
    """
    def _createPage(self):
        return HtmlPageFactory().create(self.wikiroot, "HTML-страница", [])

    def _getEditor(self):
        return self.application.mainWindow.pagePanel.pageView.codeEditor


class TextEditorPolyactionsTest(BaseEditorPolyactionsTest):
    """
    Test polyactions for text pages
    """
    def _createPage(self):
        return TextPageFactory().create(self.wikiroot,
                                        "Текстовая страница",
                                        [])

    def _getEditor(self):
        return self.application.mainWindow.pagePanel.pageView.textEditor
