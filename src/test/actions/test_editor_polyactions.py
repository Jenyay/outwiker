# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod


from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.commands import getClipboardText
from outwiker.actions.polyactionsid import *


class BaseEditorPolyactionsTest (BaseMainWndTest):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _createPage(self):
        pass

    @abstractmethod
    def _getEditor(self):
        pass

    def setUp(self):
        BaseMainWndTest.setUp(self)
        self.page = self._createPage()
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.page

    def test_LineDuplicate_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'Строка 1\nСтрока 1\nСтрока 2\nСтрока 3'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_LineDuplicate_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3'
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = u'Строка 1\nСтрока 2\nСтрока 2\nСтрока 3'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_LineDuplicate_03(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'\n'

        actionController.getAction(LINE_DUPLICATE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesDown_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesDown_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 15)

        result = u'Строка 3\nСтрока 1\nСтрока 2\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesUp_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(15, 15)

        result = u'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesUp_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(10, 21)

        result = u'Строка 2\nСтрока 3\nСтрока 1\nСтрока 4'

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_MoveLinesUpDown_empty(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u''

        actionController.getAction(MOVE_SELECTED_LINES_UP_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'), result)

        actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'), result)

    def test_DeleteCurrentLine_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u'Строка 2\nСтрока 3\nСтрока 4'

        actionController.getAction(DELETE_CURRENT_LINE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_DeleteCurrentLine_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor.SetText(text)
        editor.SetSelection(10, 10)

        result = u'Строка 1\nСтрока 3\nСтрока 4'

        actionController.getAction(DELETE_CURRENT_LINE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_DeleteCurrentLine_03_empty(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u''
        editor.SetText(text)
        editor.SetSelection(0, 0)

        result = u''

        actionController.getAction(DELETE_CURRENT_LINE_ID).run(None)
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         result)

    def test_GotoNextWord_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = u'слово слово2 ещеоднослово'
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
        actionController = Application.actionController
        text = u'слово слово2 ещеоднослово'
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
        actionController = Application.actionController
        text = u''
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_NEXT_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

        actionController.getAction(GOTO_PREV_WORD).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_01(self):
        text = u''
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_02(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_03(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(3)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_04(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(5)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_05(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(6)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_06(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(7)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_07(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(13)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_08(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(14)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_09(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(25)

        actionController.getAction(GOTO_WORD_START).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordEnd_01(self):
        text = u''
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordEnd_02(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_03(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(1)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_04(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(6)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_05(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(12)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_06(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(13)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_07(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(14)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_08(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(25)

        actionController.getAction(GOTO_WORD_END).run(None)
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_CopyLineToClipboard_01(self):
        text = u''
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text, u'')

    def test_CopyLineToClipboard_02(self):
        text = u'\n'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace(u'\r\n', u'\n'), u'\n')

    def test_CopyLineToClipboard_03(self):
        text = u'Строка 1'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace(u'\r\n', u'\n'), u'Строка 1')

    def test_CopyLineToClipboard_04(self):
        text = u'Строка 1\n'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace(u'\r\n', u'\n'), u'Строка 1\n')

    def test_CopyLineToClipboard_05(self):
        text = u'Строка 1\nСтрока 2'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace(u'\r\n', u'\n'), u'Строка 2')

    def test_CopyLineToClipboard_06(self):
        text = u'Строка 1\nСтрока 2\n'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_COPY_LINE).run(None)
        cb_text = getClipboardText()

        self.assertEqual(cb_text.replace(u'\r\n', u'\n'), u'Строка 2\n')

    def test_CutLineToClipboard_01(self):
        text = u''
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText()
        newtext = editor.GetText().replace(u'\r\n', u'\n')

        self.assertEqual(cb_text, u'')
        self.assertEqual(newtext, u'')

    def test_CutLineToClipboard_02(self):
        text = u'Строка 1'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace(u'\r\n', u'\n')
        newtext = editor.GetText().replace(u'\r\n', u'\n')

        self.assertEqual(cb_text, u'Строка 1')
        self.assertEqual(newtext, u'')

    def test_CutLineToClipboard_03(self):
        text = u'Строка 1\n'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace(u'\r\n', u'\n')
        newtext = editor.GetText().replace(u'\r\n', u'\n')

        self.assertEqual(cb_text, u'Строка 1\n')
        self.assertEqual(newtext, u'')

    def test_CutLineToClipboard_04(self):
        text = u'Строка 1\nСтрока 2'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(0)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace(u'\r\n', u'\n')
        newtext = editor.GetText().replace(u'\r\n', u'\n')

        self.assertEqual(cb_text, u'Строка 1\n')
        self.assertEqual(newtext, u'Строка 2')

    def test_CutLineToClipboard_05(self):
        text = u'Строка 1\nСтрока 2'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace(u'\r\n', u'\n')
        newtext = editor.GetText().replace(u'\r\n', u'\n')

        self.assertEqual(cb_text, u'Строка 2')
        self.assertEqual(newtext, u'Строка 1\n')

    def test_CutLineToClipboard_06(self):
        text = u'Строка 1\nСтрока 2\nСтрока 3'
        editor = self._getEditor()
        actionController = Application.actionController
        editor.SetText(text)
        editor.GotoPos(9)

        actionController.getAction(CLIPBOARD_CUT_LINE).run(None)
        cb_text = getClipboardText().replace(u'\r\n', u'\n')
        newtext = editor.GetText().replace(u'\r\n', u'\n')

        self.assertEqual(cb_text, u'Строка 2\n')
        self.assertEqual(newtext, u'Строка 1\nСтрока 3')


class WikiEditorPolyactionsTest (BaseEditorPolyactionsTest):
    """
    Test polyactions for wiki pages
    """
    def _createPage(self):
        return WikiPageFactory().create(self.wikiroot, u"Викистраница", [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.codeEditor


class HtmlEditorPolyactionsTest (BaseEditorPolyactionsTest):
    """
    Test polyactions for HTML pages
    """
    def _createPage(self):
        return HtmlPageFactory().create(self.wikiroot, u"HTML-страница", [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.codeEditor


class TextEditorPolyactionsTest (BaseEditorPolyactionsTest):
    """
    Test polyactions for text pages
    """
    def _createPage(self):
        return TextPageFactory().create(self.wikiroot,
                                        u"Текстовая страница",
                                        [])

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.textEditor
