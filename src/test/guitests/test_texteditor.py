# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory


class TextEditorTest(BaseMainWndTest):
    """
    Тесты действий для викистраницы
    """
    def setUp(self):
        BaseMainWndTest.setUp(self)

        TextPageFactory().create(self.wikiroot, u"Страница", [])

        self.testpage = self.wikiroot[u"Страница"]

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.testpage

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.textEditor

    def testGetSetText(self):
        sourceText = u"000 Проверка 111"

        self._getEditor().SetText(sourceText)

        text = self._getEditor().GetText()

        self.assertEqual(text, sourceText)
        self.assertEqual(text[:10], sourceText[:10])

    def testGetTextEmpty(self):
        self.assertEqual(len(self._getEditor().GetText()), 0)

    def testAddText(self):
        self._getEditor().AddText(u"Абырвалг")
        self.assertEqual(self._getEditor().GetText(), u"Абырвалг")

        self._getEditor().AddText(u"\nРаз два три")
        self.assertEqual(self._getEditor().GetText(), u"Абырвалг\nРаз два три")

    def testGetSelectionEmpty(self):
        self.assertEqual(len(self._getEditor().GetText()), 0)

    def testSelection(self):
        text = u"""Абырвалг
проверка
раз два три
четыре
"""
        self._getEditor().SetText(text)
        self.assertEqual(len(self._getEditor().GetSelectedText()), 0)

        self._getEditor().SetSelection(0, 0)
        self.assertEqual(len(self._getEditor().GetSelectedText()), 0)

        self._getEditor().SetSelection(0, 1)
        self.assertEqual(self._getEditor().GetSelectedText(), u"А")

        self._getEditor().SetSelection(0, -1)
        self.assertEqual(self._getEditor().GetSelectedText(), text[0: -1])

        self._getEditor().SetSelection(0, len(text))
        self.assertEqual(self._getEditor().GetSelectedText(), text)

        self._getEditor().SetSelection(11, 16)
        self.assertEqual(self._getEditor().GetSelectedText(), text[11: 16])

    def testReplaceText(self):
        text = u"""Абырвалг
проверка
раз два три
четыре
"""

        # Замена при пустом тексте
        self._getEditor().replaceText(u"Абырвалг")
        self.assertEqual(self._getEditor().GetText(), u"Абырвалг")

        self._getEditor().SetText(text)
        self._getEditor().replaceText(u"Абырвалг")
        self.assertEqual(self._getEditor().GetText(), u"""АбырвалгАбырвалг
проверка
раз два три
четыре
""")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, 3)
        self._getEditor().replaceText(u"Замена")
        self.assertEqual(self._getEditor().GetText(), u"""Заменарвалг
проверка
раз два три
четыре
""")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(1, 5)
        self._getEditor().replaceText(u"Замена")
        self.assertEqual(self._getEditor().GetText(), u"""АЗаменаалг
проверка
раз два три
четыре
""")

    def testEscapeHtmlEmpty(self):
        self._getEditor().escapeHtml()
        self.assertEqual(len(self._getEditor().GetText()), 0)

    def testEscapeHtml(self):
        text = u"Проверка > тест < 1234"

        self._getEditor().SetText(text)
        self._getEditor().escapeHtml()
        self.assertEqual(self._getEditor().GetText(), text)

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, 10)
        self._getEditor().escapeHtml()
        self.assertEqual(self._getEditor().GetText(),
                         u"Проверка &gt; тест < 1234")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, -1)
        self._getEditor().escapeHtml()
        self.assertEqual(self._getEditor().GetText(),
                         u"Проверка &gt; тест &lt; 1234")

    def testTurnTextEmpty(self):
        self._getEditor().turnText(u"Лево", u"Право")
        self.assertEqual(self._getEditor().GetText(), u"ЛевоПраво")

    def testTurnText(self):
        text = u"Проверка абырвалг"

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, 1)
        self._getEditor().turnText(u"Лево", u"Право")
        self.assertEqual(self._getEditor().GetText(),
                         u"ЛевоППравороверка абырвалг")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(1, 3)
        self._getEditor().turnText(u"Лево", u"Право")
        self.assertEqual(self._getEditor().GetText(),
                         u"ПЛевороПравоверка абырвалг")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, len(text))
        self._getEditor().turnText(u"Лево", u"Право")
        self.assertEqual(self._getEditor().GetText(),
                         u"ЛевоПроверка абырвалгПраво")

    def testTurnTextSelection_01(self):
        text = u"Проверка абырвалг"

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(9, 17)

        self.assertEqual(self._getEditor().GetSelectedText(), u"абырвалг")

        self._getEditor().turnText(u"Лево ", u" Право")

        self.assertEqual(self._getEditor().GetSelectedText(), u"абырвалг")

        self.assertEqual(self._getEditor().GetText(),
                         u"Проверка Лево абырвалг Право")

    def testTurnTextSelection_02(self):
        text = u"Проверка  абырвалг"

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(9, 9)

        self.assertEqual(self._getEditor().GetSelectedText(), u"")

        self._getEditor().turnText(u"Лево ", u" Право")

        self.assertEqual(self._getEditor().GetSelectedText(), u"")

        self.assertEqual(self._getEditor().GetText(),
                         u"Проверка Лево  Право абырвалг")

    def testGetCurrentPositionEmpty(self):
        self.assertEqual(self._getEditor().GetCurrentPosition(), 0)

    def testGetCurrentPosition(self):
        text = u"Проверка абырвалг"
        self._getEditor().SetText(text)

        self._getEditor().SetSelection(0, 1)
        self.assertEqual(self._getEditor().GetCurrentPosition(), 1)

        self._getEditor().SetSelection(1, 0)
        self.assertEqual(self._getEditor().GetCurrentPosition(), 0)

        self._getEditor().SetSelection(10, 10)
        self.assertEqual(self._getEditor().GetCurrentPosition(), 10)

    def testGetSelectionPosEmpty(self):
        self.assertEqual(self._getEditor().GetSelectionStart(), 0)
        self.assertEqual(self._getEditor().GetSelectionEnd(), 0)

    def testGetSelectionPos(self):
        text = u"Проверка абырвалг"
        self._getEditor().SetText(text)

        self._getEditor().SetSelection(0, 0)
        self.assertEqual(self._getEditor().GetSelectionStart(), 0)
        self.assertEqual(self._getEditor().GetSelectionEnd(), 0)

        self._getEditor().SetSelection(0, 1)
        self.assertEqual(self._getEditor().GetSelectionStart(), 0)
        self.assertEqual(self._getEditor().GetSelectionEnd(), 1)

        self._getEditor().SetSelection(10, 10)
        self.assertEqual(self._getEditor().GetSelectionStart(), 10)
        self.assertEqual(self._getEditor().GetSelectionEnd(), 10)

        self._getEditor().SetSelection(0, len(text))
        self.assertEqual(self._getEditor().GetSelectionStart(), 0)
        self.assertEqual(self._getEditor().GetSelectionEnd(), len(text))
        self.assertEqual(self._getEditor().GetSelectedText(), text)

    def testGetSetSearchPhrase(self):
        searchController = self._getEditor().searchPanel

        searchController.setSearchPhrase(u"Абырвалг")
        self.assertEqual(searchController.getSearchPhrase(), u"Абырвалг")

    def testSearchNext(self):
        editor = self._getEditor()
        editor.SetText(u"Абырвалг проверка абырвалг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase(u"абырвалг")
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 8)

        searchController.nextSearch()
        self.assertEqual(editor.GetSelectionStart(), 18)
        self.assertEqual(editor.GetSelectionEnd(), 26)

        searchController.nextSearch()
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 8)

    def testSearchPrev(self):
        editor = self._getEditor()
        editor.SetText(u"Абырвалг проверка абырвалг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase(u"абырвалг")

        searchController.prevSearch()
        self.assertEqual(editor.GetSelectionStart(), 18)
        self.assertEqual(editor.GetSelectionEnd(), 26)

        searchController.prevSearch()
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 8)

        searchController.prevSearch()
        self.assertEqual(editor.GetSelectionStart(), 18)
        self.assertEqual(editor.GetSelectionEnd(), 26)

    def testSearchSiblingsNext(self):
        editor = self._getEditor()
        editor.SetText(u"ыыыыыыыыы")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase(u"ыыы")
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 3)

        searchController.nextSearch()
        self.assertEqual(editor.GetSelectionStart(), 3)
        self.assertEqual(editor.GetSelectionEnd(), 6)

        searchController.nextSearch()
        self.assertEqual(editor.GetSelectionStart(), 6)
        self.assertEqual(editor.GetSelectionEnd(), 9)

        searchController.nextSearch()
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 3)

    def testSearchSiblingsPrev(self):
        editor = self._getEditor()
        editor.SetText(u"ыыыыыыыыы")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase(u"ыыы")
        searchController.prevSearch()
        self.assertEqual(editor.GetSelectionStart(), 6)
        self.assertEqual(editor.GetSelectionEnd(), 9)

        searchController.prevSearch()
        self.assertEqual(editor.GetSelectionStart(), 3)
        self.assertEqual(editor.GetSelectionEnd(), 6)

        searchController.prevSearch()
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 3)

    def testGetSetReplacePhrase(self):
        editor = self._getEditor()
        searchController = editor.searchPanel
        searchController.switchToReplaceMode()

        self.assertEqual(searchController.getReplacePhrase(), u"")

        searchController.setReplacePhrase(u"Абырвалг")
        self.assertEqual(searchController.getReplacePhrase(), u"Абырвалг")

    def testReplace1(self):
        editor = self._getEditor()
        editor.SetText(u"Абырвалг проверка абырвалг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase(u"Проверка")
        searchController.replace()

        self.assertEqual(editor.GetText(), u"Абырвалг проверка абырвалг")

    def testReplace2(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase(u"Проверка111")
        searchController.setSearchPhrase(u"абырвалг")
        searchController.replace()

        self.assertEqual(editor.GetText(), u"Проверка111 проверка абыРВАлг")
        self.assertEqual(editor.GetSelectionStart(), 21)
        self.assertEqual(editor.GetSelectionEnd(), 29)

        searchController.replace()
        self.assertEqual(editor.GetText(), u"Проверка111 проверка Проверка111")
        self.assertEqual(editor.GetSelectionStart(), 32)
        self.assertEqual(editor.GetSelectionEnd(), 32)

    def testReplace3(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(1, 1)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase(u"Проверка111")
        searchController.setSearchPhrase(u"абырвалг")

        self.assertEqual(editor.GetSelectionStart(), 18)
        self.assertEqual(editor.GetSelectionEnd(), 26)

        searchController.replace()

        self.assertEqual(editor.GetText(), u"АбыРваЛг проверка Проверка111")
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 8)

        searchController.replace()
        self.assertEqual(editor.GetText(), u"Проверка111 проверка Проверка111")
        self.assertEqual(editor.GetSelectionStart(), 11)
        self.assertEqual(editor.GetSelectionEnd(), 11)

    def testReplace4(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase(u"")
        searchController.setSearchPhrase(u"абырвалг")
        searchController.replace()

        self.assertEqual(editor.GetText(), u" проверка абыРВАлг")
        self.assertEqual(editor.GetSelectionStart(), 10)
        self.assertEqual(editor.GetSelectionEnd(), 18)

        searchController.replace()
        self.assertEqual(editor.GetText(), u" проверка ")
        self.assertEqual(editor.GetSelectionStart(), 10)
        self.assertEqual(editor.GetSelectionEnd(), 10)

    def testReplaceAll1(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase(u"Проверка111")
        searchController.setSearchPhrase(u"абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(), u"Проверка111 проверка Проверка111")

    def testReplaceAll2(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase(u"Проверка111")
        searchController.setSearchPhrase(u"абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(), u"Проверка111 проверка Проверка111")

    def testReplaceAll3(self):
        editor = self._getEditor()
        editor.SetText(u"qqq АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"Абырвалг111")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         u"qqq Абырвалг111 проверка Абырвалг111 qqq")

    def testReplaceAll4(self):
        editor = self._getEditor()
        editor.SetText(u"qqq АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"111Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         u"qqq 111Абырвалг проверка 111Абырвалг qqq")

    def testReplaceAll5(self):
        editor = self._getEditor()
        editor.SetText(u"qqq АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         u"qqq Абырвалг проверка Абырвалг qqq")

    def testReplaceAll6(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"111Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         u"111Абырвалг проверка 111Абырвалг qqq")

    def testReplaceAll7(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"Абырвалг111")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         u"Абырвалг111 проверка Абырвалг111 qqq")

    def testReplaceAll8(self):
        editor = self._getEditor()
        editor.SetText(u"ыыы АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"111Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         u"ыыы 111Абырвалг проверка 111Абырвалг")

    def testReplaceAll9(self):
        editor = self._getEditor()
        editor.SetText(u"ыыы АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"Абырвалг111")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         u"ыыы Абырвалг111 проверка Абырвалг111")

    def testReplaceAll10(self):
        editor = self._getEditor()
        editor.SetText(u"АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase(u"абырвалг")
        searchController.setReplacePhrase(u"Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(), u"Абырвалг проверка Абырвалг")

    def testSetLine_01(self):
        editor = self._getEditor()
        editor.SetText(u"Абырвалг Абырвалг")
        editor.SetLine(0, u'Проверка')

        self.assertEqual(editor.GetText(), u"Проверка")

    def testSetLine_02(self):
        editor = self._getEditor()
        editor.SetText(u"""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(0, u'Проверка\n')

        self.assertEqual(editor.GetText(), u"""Проверка
Строка 2
Строка 3""")

    def testSetLine_03(self):
        editor = self._getEditor()
        editor.SetText(u"""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(1, u'Проверка\n')

        self.assertEqual(editor.GetText(), u"""Строка 1
Проверка
Строка 3""")

    def testSetLine_04(self):
        editor = self._getEditor()
        editor.SetText(u"""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(2, u'Проверка')

        self.assertEqual(editor.GetText(), u"""Строка 1
Строка 2
Проверка""")

    def testSetLine_05(self):
        editor = self._getEditor()
        editor.SetText(u'')
        editor.SetLine(0, u'Проверка')
        self.assertEqual(editor.GetText(), u'Проверка')

    def testSetLine_06(self):
        editor = self._getEditor()
        editor.SetText(u"""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(0, u'Проверка')

        self.assertEqual(editor.GetText(), u"""ПроверкаСтрока 2
Строка 3""")

    def testSetLine_07(self):
        editor = self._getEditor()
        editor.SetText(u"""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(2, u'Проверка')

        self.assertEqual(editor.GetText(), u"""Строка 1
Строка 2
Проверка""")

    def testGetLine_01(self):
        editor = self._getEditor()
        editor.SetText(u"""Строка 1
Строка 2
Строка 3""")
        self.assertEqual(editor.GetLine(0), u'Строка 1\n')
        self.assertEqual(editor.GetLine(1), u'Строка 2\n')
        self.assertEqual(editor.GetLine(2), u'Строка 3')

    def testGetSelectionLines_01(self):
        editor = self._getEditor()
        editor.SetText(u'')
        editor.SetSelection(0, 0)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 0)
        self.assertEqual(end, 0)

    def testGetSelectionLines_02(self):
        editor = self._getEditor()
        editor.SetText(u'''Проверка\n''')
        editor.SetSelection(0, 8)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 0)
        self.assertEqual(end, 0)

    def testGetSelectionLines_03(self):
        editor = self._getEditor()
        editor.SetText(u'''Проверка\n''')
        editor.SetSelection(0, 9)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 0)
        self.assertEqual(end, 1)

    def testGetSelectionLines_04(self):
        editor = self._getEditor()
        editor.SetText(u'''Проверка\nПроверка\nПроверка''')
        editor.SetSelection(9, 18)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 1)
        self.assertEqual(end, 2)

    def test_toddleLinePrefix_01(self):
        editor = self._getEditor()
        editor.SetText(u'')

        editor.toddleLinePrefix(0, u'Тест ')
        self.assertEqual(editor.GetText(), u'Тест ')

        editor.toddleLinePrefix(0, u'Тест ')
        self.assertEqual(editor.GetText(), u'')

    def test_toddleLinePrefix_02(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка')

        editor.toddleLinePrefix(0, u'Тест ')
        self.assertEqual(editor.GetText(), u'Тест Проверка')

        editor.toddleLinePrefix(0, u'Тест ')
        self.assertEqual(editor.GetText(), u'Проверка')

    def test_toddleLinePrefix_03(self):
        editor = self._getEditor()
        editor.SetText(u'''Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(0, u'Тест ')
        self.assertEqual(editor.GetText(),
                         u'''Тест Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(0, u'Тест ')
        self.assertEqual(editor.GetText(),
                         u'''Проверка
Проверка
Проверка''')

    def test_toddleLinePrefix_04(self):
        editor = self._getEditor()
        editor.SetText(u'''Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(1, u'Тест ')
        self.assertEqual(editor.GetText(),
                         u'''Проверка
Тест Проверка
Проверка''')

        editor.toddleLinePrefix(1, u'Тест ')
        self.assertEqual(editor.GetText(),
                         u'''Проверка
Проверка
Проверка''')

    def test_toddleLinePrefix_05(self):
        editor = self._getEditor()
        editor.SetText(u'''Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(2, u'Тест ')
        self.assertEqual(editor.GetText(),
                         u'''Проверка
Проверка
Тест Проверка''')

        editor.toddleLinePrefix(2, u'Тест ')
        self.assertEqual(editor.GetText(),
                         u'''Проверка
Проверка
Проверка''')

    def test_GetLineStartPosition_01(self):
        editor = self._getEditor()
        editor.SetText(u'')
        lineStart = editor.GetLineStartPosition(0)
        self.assertEqual(lineStart, 0)

    def test_GetLineStartPosition_02(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка')
        lineStart = editor.GetLineStartPosition(0)
        self.assertEqual(lineStart, 0)

    def test_GetLineStartPosition_03(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка\nПроверка')
        lineStart = editor.GetLineStartPosition(1)
        self.assertEqual(lineStart, 9)

    def test_GetLineEndPosition_01(self):
        editor = self._getEditor()
        editor.SetText(u'')
        lineEnd = editor.GetLineEndPosition(0)
        self.assertEqual(lineEnd, 0)

    def test_GetLineEndPosition_02(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка')
        lineEnd = editor.GetLineEndPosition(0)
        self.assertEqual(lineEnd, 8)

    def test_GetLineEndPosition_03(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка\n')
        lineEnd = editor.GetLineEndPosition(0)
        self.assertEqual(lineEnd, 8)

    def test_GetLineEndPosition_04(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка\nПроверка')
        lineEnd = editor.GetLineEndPosition(1)
        self.assertEqual(lineEnd, 17)

    def test_toddleSelectedLinesPrefix_01(self):
        editor = self._getEditor()
        editor.SetText(u'')
        editor.SetSelection(0, 0)

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'Тест ')

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'')

    def test_toddleSelectedLinesPrefix_02(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка')
        editor.SetSelection(0, 0)

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'Тест Проверка')

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'Проверка')

    def test_toddleSelectedLinesPrefix_03(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка\nПроверка')
        editor.SetSelection(2, 5)

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'Тест Проверка\nПроверка')

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'Проверка\nПроверка')

    def test_toddleSelectedLinesPrefix_04(self):
        editor = self._getEditor()
        editor.SetText(u'Проверка\nПроверка')
        editor.SetSelection(2, 9)

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'Тест Проверка\nТест Проверка')

        editor.toddleSelectedLinesPrefix(u'Тест ')
        self.assertEqual(editor.GetText(), u'Проверка\nПроверка')

    def test_MoveSelectedLinesDown_01(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         u'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4')

    def test_MoveSelectedLinesDown_02(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 9)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         u'Строка 1\nСтрока 3\nСтрока 2\nСтрока 4')

    def test_MoveSelectedLinesDown_03(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 10)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         u'Строка 3\nСтрока 1\nСтрока 2\nСтрока 4')

    def test_MoveSelectedLinesDown_04(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 18)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         u'Строка 3\nСтрока 1\nСтрока 2\nСтрока 4')

    def test_MoveSelectedLinesUp_01(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 9)

        editor.MoveSelectedLinesUp()
        self.assertEqual(editor.GetText(),
                         u'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4')

    def test_MoveSelectedLinesUp_02(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 23)

        editor.MoveSelectedLinesUp()
        self.assertEqual(editor.GetText(),
                         u'Строка 2\nСтрока 3\nСтрока 1\nСтрока 4')

    def test_LineDuplicate_01(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.LineDuplicate()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 1\nСтрока 1\nСтрока 2\nСтрока 3\nСтрока 4')

    def test_LineDuplicate_02(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 9)

        editor.LineDuplicate()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 1\nСтрока 2\nСтрока 2\nСтрока 3\nСтрока 4')

    def test_LineDelete_01(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.LineDelete()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 2\nСтрока 3\nСтрока 4')

    def test_LineDelete_02(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(10, 10)

        editor.LineDelete()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 1\nСтрока 3\nСтрока 4')

    def test_LineDelete_03_empty(self):
        editor = self._getEditor()
        editor.SetText(u'')
        editor.SetSelection(0, 0)

        editor.LineDelete()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'), u'')

    def test_JoinLines_01(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 1Строка 2\nСтрока 3\nСтрока 4')

    def test_JoinLines_02(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 13)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 1Строка 2\nСтрока 3\nСтрока 4')

    def test_JoinLines_03(self):
        editor = self._getEditor()
        editor.SetText(u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 20)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 1Строка 2Строка 3\nСтрока 4')

    def test_JoinLines_04(self):
        text = u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor = self._getEditor()
        editor.SetText(text)
        editor.SetSelection(len(text) - 1, len(text) - 1)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace(u'\r\n', u'\n'),
                         u'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')

    def test_GoToWordStart_01(self):
        text = u''
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_02(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_03(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(3)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_04(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(5)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_05(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(6)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_06(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(7)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_07(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(13)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_08(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(14)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_09(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(25)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordEnd_01(self):
        text = u''
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordEnd_02(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_03(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(1)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_04(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(6)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_05(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(12)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_06(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(13)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_07(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(14)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_08(self):
        text = u'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(25)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_WordStartPosition_01(self):
        text = u''
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(0)

        self.assertEqual(wordStart, 0)

    def test_WordStartPosition_02(self):
        text = u'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(0)

        self.assertEqual(wordStart, 0)

    def test_WordStartPosition_03(self):
        text = u'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(3)

        self.assertEqual(wordStart, 0)

    def test_WordStartPosition_04(self):
        text = u' слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(3)

        self.assertEqual(wordStart, 1)

    def test_WordStartPosition_05(self):
        text = u' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(7)

        self.assertEqual(wordStart, 7)

    def test_WordStartPosition_06(self):
        text = u' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(9)

        self.assertEqual(wordStart, 7)

    def test_WordEndPosition_01(self):
        text = u''
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(0)

        self.assertEqual(wordEnd, 0)

    def test_WordEndPosition_02(self):
        text = u'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(0)

        self.assertEqual(wordEnd, 5)

    def test_WordEndPosition_03(self):
        text = u'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(3)

        self.assertEqual(wordEnd, 5)

    def test_WordEndPosition_04(self):
        text = u' слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(3)

        self.assertEqual(wordEnd, 6)

    def test_WordEndPosition_05(self):
        text = u' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(7)

        self.assertEqual(wordEnd, 13)

    def test_WordEndPosition_06(self):
        text = u' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(9)

        self.assertEqual(wordEnd, 13)

    def test_GetWord_01(self):
        text = u''
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(0)

        self.assertEqual(word, u'')

    def test_GetWord_02(self):
        text = u''
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(10)

        self.assertEqual(word, u'')

    def test_GetWord_03(self):
        text = u'слово'
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(0)

        self.assertEqual(word, u'слово')

    def test_GetWord_04(self):
        text = u' слово '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(1)

        self.assertEqual(word, u'слово')

    def test_GetWord_05(self):
        text = u' слово '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(6)

        self.assertEqual(word, u'слово')

    def test_GetWord_06(self):
        text = u' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(7)

        self.assertEqual(word, u'слово2')

    def test_GetWord_07(self):
        text = u' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(13)

        self.assertEqual(word, u'слово2')

    def test_GetWord_08(self):
        text = u' слово слово2 '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(13)

        self.assertEqual(word, u'слово2')

    def test_GetWord_09(self):
        text = u' слово слово2 '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(100)

        self.assertEqual(word, u'')
