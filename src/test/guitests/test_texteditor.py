# -*- coding: utf-8 -*-

from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUITest


class TextEditorTest(BaseOutWikerGUITest):
    """
    Тесты действий для викистраницы
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        TextPageFactory().create(self.wikiroot, "Страница", [])

        self.testpage = self.wikiroot["Страница"]

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.testpage

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _getEditor(self):
        return self.application.mainWindow.pagePanel.pageView.textEditor

    def testGetSetText(self):
        sourceText = "000 Проверка 111"

        self._getEditor().SetText(sourceText)

        text = self._getEditor().GetText()

        self.assertEqual(text, sourceText)
        self.assertEqual(text[:10], sourceText[:10])

    def testGetTextEmpty(self):
        self.assertEqual(len(self._getEditor().GetText()), 0)

    def testAddText(self):
        self._getEditor().AddText("Абырвалг")
        self.assertEqual(self._getEditor().GetText(), "Абырвалг")

        self._getEditor().AddText("\nРаз два три")
        self.assertEqual(self._getEditor().GetText(), "Абырвалг\nРаз два три")

    def testGetSelectionEmpty(self):
        self.assertEqual(len(self._getEditor().GetText()), 0)

    def testSelection(self):
        text = """Абырвалг
проверка
раз два три
четыре
"""
        self._getEditor().SetText(text)
        self.assertEqual(len(self._getEditor().GetSelectedText()), 0)

        self._getEditor().SetSelection(0, 0)
        self.assertEqual(len(self._getEditor().GetSelectedText()), 0)

        self._getEditor().SetSelection(0, 1)
        self.assertEqual(self._getEditor().GetSelectedText(), "А")

        self._getEditor().SetSelection(0, -1)
        self.assertEqual(self._getEditor().GetSelectedText(), text[0: -1])

        self._getEditor().SetSelection(0, len(text))
        self.assertEqual(self._getEditor().GetSelectedText(), text)

        self._getEditor().SetSelection(11, 16)
        self.assertEqual(self._getEditor().GetSelectedText(), text[11: 16])

    def testReplaceText(self):
        text = """Абырвалг
проверка
раз два три
четыре
"""

        # Замена при пустом тексте
        self._getEditor().replaceText("Абырвалг")
        self.assertEqual(self._getEditor().GetText(), "Абырвалг")

        self._getEditor().SetText(text)
        self._getEditor().replaceText("Абырвалг")
        self.assertEqual(self._getEditor().GetText(), """АбырвалгАбырвалг
проверка
раз два три
четыре
""")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, 3)
        self._getEditor().replaceText("Замена")
        self.assertEqual(self._getEditor().GetText(), """Заменарвалг
проверка
раз два три
четыре
""")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(1, 5)
        self._getEditor().replaceText("Замена")
        self.assertEqual(self._getEditor().GetText(), """АЗаменаалг
проверка
раз два три
четыре
""")

    def testEscapeHtmlEmpty(self):
        self._getEditor().escapeHtml()
        self.assertEqual(len(self._getEditor().GetText()), 0)

    def testEscapeHtml(self):
        text = "Проверка > тест < 1234"

        self._getEditor().SetText(text)
        self._getEditor().escapeHtml()
        self.assertEqual(self._getEditor().GetText(), text)

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, 10)
        self._getEditor().escapeHtml()
        self.assertEqual(self._getEditor().GetText(),
                         "Проверка &gt; тест < 1234")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, -1)
        self._getEditor().escapeHtml()
        self.assertEqual(self._getEditor().GetText(),
                         "Проверка &gt; тест &lt; 1234")

    def testTurnTextEmpty(self):
        self._getEditor().turnText("Лево", "Право")
        self.assertEqual(self._getEditor().GetText(), "ЛевоПраво")

    def testTurnText(self):
        text = "Проверка абырвалг"

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, 1)
        self._getEditor().turnText("Лево", "Право")
        self.assertEqual(self._getEditor().GetText(),
                         "ЛевоППравороверка абырвалг")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(1, 3)
        self._getEditor().turnText("Лево", "Право")
        self.assertEqual(self._getEditor().GetText(),
                         "ПЛевороПравоверка абырвалг")

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(0, len(text))
        self._getEditor().turnText("Лево", "Право")
        self.assertEqual(self._getEditor().GetText(),
                         "ЛевоПроверка абырвалгПраво")

    def testTurnTextSelection_01(self):
        text = "Проверка абырвалг"

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(9, 17)

        self.assertEqual(self._getEditor().GetSelectedText(), "абырвалг")

        self._getEditor().turnText("Лево ", " Право")

        self.assertEqual(self._getEditor().GetSelectedText(), "абырвалг")

        self.assertEqual(self._getEditor().GetText(),
                         "Проверка Лево абырвалг Право")

    def testTurnTextSelection_02(self):
        text = "Проверка  абырвалг"

        self._getEditor().SetText(text)
        self._getEditor().SetSelection(9, 9)

        self.assertEqual(self._getEditor().GetSelectedText(), "")

        self._getEditor().turnText("Лево ", " Право")

        self.assertEqual(self._getEditor().GetSelectedText(), "")

        self.assertEqual(self._getEditor().GetText(),
                         "Проверка Лево  Право абырвалг")

    def testGetCurrentPositionEmpty(self):
        self.assertEqual(self._getEditor().GetCurrentPosition(), 0)

    def testGetCurrentPosition(self):
        text = "Проверка абырвалг"
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
        text = "Проверка абырвалг"
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

        searchController.setSearchPhrase("Абырвалг")
        self.assertEqual(searchController.getSearchPhrase(), "Абырвалг")

    def testSearchNext(self):
        editor = self._getEditor()
        editor.SetText("Абырвалг проверка абырвалг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase("абырвалг")
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
        editor.SetText("Абырвалг проверка абырвалг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase("абырвалг")

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
        editor.SetText("ыыыыыыыыы")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase("ыыы")
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
        editor.SetText("ыыыыыыыыы")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel

        searchController.setSearchPhrase("ыыы")
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

        self.assertEqual(searchController.getReplacePhrase(), "")

        searchController.setReplacePhrase("Абырвалг")
        self.assertEqual(searchController.getReplacePhrase(), "Абырвалг")

    def testReplace1(self):
        editor = self._getEditor()
        editor.SetText("Абырвалг проверка абырвалг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase("Проверка")
        searchController.replace()

        self.assertEqual(editor.GetText(), "Абырвалг проверка абырвалг")

    def testReplace2(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase("Проверка111")
        searchController.setSearchPhrase("абырвалг")
        searchController.replace()

        self.assertEqual(editor.GetText(), "Проверка111 проверка абыРВАлг")
        self.assertEqual(editor.GetSelectionStart(), 21)
        self.assertEqual(editor.GetSelectionEnd(), 29)

        searchController.replace()
        self.assertEqual(editor.GetText(), "Проверка111 проверка Проверка111")
        self.assertEqual(editor.GetSelectionStart(), 32)
        self.assertEqual(editor.GetSelectionEnd(), 32)

    def testReplace3(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(1, 1)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase("Проверка111")
        searchController.setSearchPhrase("абырвалг")

        self.assertEqual(editor.GetSelectionStart(), 18)
        self.assertEqual(editor.GetSelectionEnd(), 26)

        searchController.replace()

        self.assertEqual(editor.GetText(), "АбыРваЛг проверка Проверка111")
        self.assertEqual(editor.GetSelectionStart(), 0)
        self.assertEqual(editor.GetSelectionEnd(), 8)

        searchController.replace()
        self.assertEqual(editor.GetText(), "Проверка111 проверка Проверка111")
        self.assertEqual(editor.GetSelectionStart(), 11)
        self.assertEqual(editor.GetSelectionEnd(), 11)

    def testReplace4(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase("")
        searchController.setSearchPhrase("абырвалг")
        searchController.replace()

        self.assertEqual(editor.GetText(), " проверка абыРВАлг")
        self.assertEqual(editor.GetSelectionStart(), 10)
        self.assertEqual(editor.GetSelectionEnd(), 18)

        searchController.replace()
        self.assertEqual(editor.GetText(), " проверка ")
        self.assertEqual(editor.GetSelectionStart(), 10)
        self.assertEqual(editor.GetSelectionEnd(), 10)

    def testReplaceAll1(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(0, 0)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase("Проверка111")
        searchController.setSearchPhrase("абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(), "Проверка111 проверка Проверка111")

    def testReplaceAll2(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setReplacePhrase("Проверка111")
        searchController.setSearchPhrase("абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(), "Проверка111 проверка Проверка111")

    def testReplaceAll3(self):
        editor = self._getEditor()
        editor.SetText("qqq АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("Абырвалг111")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         "qqq Абырвалг111 проверка Абырвалг111 qqq")

    def testReplaceAll4(self):
        editor = self._getEditor()
        editor.SetText("qqq АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("111Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         "qqq 111Абырвалг проверка 111Абырвалг qqq")

    def testReplaceAll5(self):
        editor = self._getEditor()
        editor.SetText("qqq АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         "qqq Абырвалг проверка Абырвалг qqq")

    def testReplaceAll6(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("111Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         "111Абырвалг проверка 111Абырвалг qqq")

    def testReplaceAll7(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг qqq")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("Абырвалг111")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         "Абырвалг111 проверка Абырвалг111 qqq")

    def testReplaceAll8(self):
        editor = self._getEditor()
        editor.SetText("ыыы АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("111Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         "ыыы 111Абырвалг проверка 111Абырвалг")

    def testReplaceAll9(self):
        editor = self._getEditor()
        editor.SetText("ыыы АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("Абырвалг111")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(),
                         "ыыы Абырвалг111 проверка Абырвалг111")

    def testReplaceAll10(self):
        editor = self._getEditor()
        editor.SetText("АбыРваЛг проверка абыРВАлг")
        editor.SetSelection(10, 10)

        searchController = editor.searchPanel
        searchController.switchToReplaceMode()
        searchController.setSearchPhrase("абырвалг")
        searchController.setReplacePhrase("Абырвалг")
        searchController.replaceAll()

        self.assertEqual(editor.GetText(), "Абырвалг проверка Абырвалг")

    def testSetLine_01(self):
        editor = self._getEditor()
        editor.SetText("Абырвалг Абырвалг")
        editor.SetLine(0, 'Проверка')

        self.assertEqual(editor.GetText(), "Проверка")

    def testSetLine_02(self):
        editor = self._getEditor()
        editor.SetText("""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(0, 'Проверка\n')

        self.assertEqual(editor.GetText(), """Проверка
Строка 2
Строка 3""")

    def testSetLine_03(self):
        editor = self._getEditor()
        editor.SetText("""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(1, 'Проверка\n')

        self.assertEqual(editor.GetText(), """Строка 1
Проверка
Строка 3""")

    def testSetLine_04(self):
        editor = self._getEditor()
        editor.SetText("""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(2, 'Проверка')

        self.assertEqual(editor.GetText(), """Строка 1
Строка 2
Проверка""")

    def testSetLine_05(self):
        editor = self._getEditor()
        editor.SetText('')
        editor.SetLine(0, 'Проверка')
        self.assertEqual(editor.GetText(), 'Проверка')

    def testSetLine_06(self):
        editor = self._getEditor()
        editor.SetText("""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(0, 'Проверка')

        self.assertEqual(editor.GetText(), """ПроверкаСтрока 2
Строка 3""")

    def testSetLine_07(self):
        editor = self._getEditor()
        editor.SetText("""Строка 1
Строка 2
Строка 3""")
        editor.SetLine(2, 'Проверка')

        self.assertEqual(editor.GetText(), """Строка 1
Строка 2
Проверка""")

    def testGetLine_01(self):
        editor = self._getEditor()
        editor.SetText("""Строка 1
Строка 2
Строка 3""")
        self.assertEqual(editor.GetLine(0), 'Строка 1\n')
        self.assertEqual(editor.GetLine(1), 'Строка 2\n')
        self.assertEqual(editor.GetLine(2), 'Строка 3')

    def testGetSelectionLines_01(self):
        editor = self._getEditor()
        editor.SetText('')
        editor.SetSelection(0, 0)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 0)
        self.assertEqual(end, 0)

    def testGetSelectionLines_02(self):
        editor = self._getEditor()
        editor.SetText('''Проверка\n''')
        editor.SetSelection(0, 8)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 0)
        self.assertEqual(end, 0)

    def testGetSelectionLines_03(self):
        editor = self._getEditor()
        editor.SetText('''Проверка\n''')
        editor.SetSelection(0, 9)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 0)
        self.assertEqual(end, 1)

    def testGetSelectionLines_04(self):
        editor = self._getEditor()
        editor.SetText('''Проверка\nПроверка\nПроверка''')
        editor.SetSelection(9, 18)
        start, end = editor.GetSelectionLines()
        self.assertEqual(start, 1)
        self.assertEqual(end, 2)

    def test_toddleLinePrefix_01(self):
        editor = self._getEditor()
        editor.SetText('')

        editor.toddleLinePrefix(0, 'Тест ')
        self.assertEqual(editor.GetText(), 'Тест ')

        editor.toddleLinePrefix(0, 'Тест ')
        self.assertEqual(editor.GetText(), '')

    def test_toddleLinePrefix_02(self):
        editor = self._getEditor()
        editor.SetText('Проверка')

        editor.toddleLinePrefix(0, 'Тест ')
        self.assertEqual(editor.GetText(), 'Тест Проверка')

        editor.toddleLinePrefix(0, 'Тест ')
        self.assertEqual(editor.GetText(), 'Проверка')

    def test_toddleLinePrefix_03(self):
        editor = self._getEditor()
        editor.SetText('''Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(0, 'Тест ')
        self.assertEqual(editor.GetText(),
                         '''Тест Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(0, 'Тест ')
        self.assertEqual(editor.GetText(),
                         '''Проверка
Проверка
Проверка''')

    def test_toddleLinePrefix_04(self):
        editor = self._getEditor()
        editor.SetText('''Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(1, 'Тест ')
        self.assertEqual(editor.GetText(),
                         '''Проверка
Тест Проверка
Проверка''')

        editor.toddleLinePrefix(1, 'Тест ')
        self.assertEqual(editor.GetText(),
                         '''Проверка
Проверка
Проверка''')

    def test_toddleLinePrefix_05(self):
        editor = self._getEditor()
        editor.SetText('''Проверка
Проверка
Проверка''')

        editor.toddleLinePrefix(2, 'Тест ')
        self.assertEqual(editor.GetText(),
                         '''Проверка
Проверка
Тест Проверка''')

        editor.toddleLinePrefix(2, 'Тест ')
        self.assertEqual(editor.GetText(),
                         '''Проверка
Проверка
Проверка''')

    def test_GetLineStartPosition_01(self):
        editor = self._getEditor()
        editor.SetText('')
        lineStart = editor.GetLineStartPosition(0)
        self.assertEqual(lineStart, 0)

    def test_GetLineStartPosition_02(self):
        editor = self._getEditor()
        editor.SetText('Проверка')
        lineStart = editor.GetLineStartPosition(0)
        self.assertEqual(lineStart, 0)

    def test_GetLineStartPosition_03(self):
        editor = self._getEditor()
        editor.SetText('Проверка\nПроверка')
        lineStart = editor.GetLineStartPosition(1)
        self.assertEqual(lineStart, 9)

    def test_GetLineEndPosition_01(self):
        editor = self._getEditor()
        editor.SetText('')
        lineEnd = editor.GetLineEndPosition(0)
        self.assertEqual(lineEnd, 0)

    def test_GetLineEndPosition_02(self):
        editor = self._getEditor()
        editor.SetText('Проверка')
        lineEnd = editor.GetLineEndPosition(0)
        self.assertEqual(lineEnd, 8)

    def test_GetLineEndPosition_03(self):
        editor = self._getEditor()
        editor.SetText('Проверка\n')
        lineEnd = editor.GetLineEndPosition(0)
        self.assertEqual(lineEnd, 8)

    def test_GetLineEndPosition_04(self):
        editor = self._getEditor()
        editor.SetText('Проверка\nПроверка')
        lineEnd = editor.GetLineEndPosition(1)
        self.assertEqual(lineEnd, 17)

    def test_toddleSelectedLinesPrefix_01(self):
        editor = self._getEditor()
        editor.SetText('')
        editor.SetSelection(0, 0)

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), 'Тест ')

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), '')

    def test_toddleSelectedLinesPrefix_02(self):
        editor = self._getEditor()
        editor.SetText('Проверка')
        editor.SetSelection(0, 0)

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), 'Тест Проверка')

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), 'Проверка')

    def test_toddleSelectedLinesPrefix_03(self):
        editor = self._getEditor()
        editor.SetText('Проверка\nПроверка')
        editor.SetSelection(2, 5)

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), 'Тест Проверка\nПроверка')

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), 'Проверка\nПроверка')

    def test_toddleSelectedLinesPrefix_04(self):
        editor = self._getEditor()
        editor.SetText('Проверка\nПроверка')
        editor.SetSelection(2, 9)

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), 'Тест Проверка\nТест Проверка')

        editor.toddleSelectedLinesPrefix('Тест ')
        self.assertEqual(editor.GetText(), 'Проверка\nПроверка')

    def test_MoveSelectedLinesDown_01(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4')

    def test_MoveSelectedLinesDown_02(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 9)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         'Строка 1\nСтрока 3\nСтрока 2\nСтрока 4')

    def test_MoveSelectedLinesDown_03(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 10)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         'Строка 3\nСтрока 1\nСтрока 2\nСтрока 4')

    def test_MoveSelectedLinesDown_04(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 18)

        editor.MoveSelectedLinesDown()
        self.assertEqual(editor.GetText(),
                         'Строка 3\nСтрока 1\nСтрока 2\nСтрока 4')

    def test_MoveSelectedLinesUp_01(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 9)

        editor.MoveSelectedLinesUp()
        self.assertEqual(editor.GetText(),
                         'Строка 2\nСтрока 1\nСтрока 3\nСтрока 4')

    def test_MoveSelectedLinesUp_02(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 23)

        editor.MoveSelectedLinesUp()
        self.assertEqual(editor.GetText(),
                         'Строка 2\nСтрока 3\nСтрока 1\nСтрока 4')

    def test_LineDuplicate_01(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.LineDuplicate()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1\nСтрока 1\nСтрока 2\nСтрока 3\nСтрока 4')

    def test_LineDuplicate_02(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(9, 9)

        editor.LineDuplicate()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1\nСтрока 2\nСтрока 2\nСтрока 3\nСтрока 4')

    def test_LineDelete_01(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.LineDelete()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 2\nСтрока 3\nСтрока 4')

    def test_LineDelete_02(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(10, 10)

        editor.LineDelete()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1\nСтрока 3\nСтрока 4')

    def test_LineDelete_03_empty(self):
        editor = self._getEditor()
        editor.SetText('')
        editor.SetSelection(0, 0)

        editor.LineDelete()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'), '')

    def test_JoinLines_01(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 0)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1Строка 2\nСтрока 3\nСтрока 4')

    def test_JoinLines_02(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 13)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1Строка 2\nСтрока 3\nСтрока 4')

    def test_JoinLines_03(self):
        editor = self._getEditor()
        editor.SetText('Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')
        editor.SetSelection(0, 20)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1Строка 2Строка 3\nСтрока 4')

    def test_JoinLines_04(self):
        text = 'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4'
        editor = self._getEditor()
        editor.SetText(text)
        editor.SetSelection(len(text) - 1, len(text) - 1)

        editor.JoinLines()
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1\nСтрока 2\nСтрока 3\nСтрока 4')

    def test_GoToWordStart_01(self):
        text = ''
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_02(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_03(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(3)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_04(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(5)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordStart_05(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(6)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_06(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(7)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 6)

    def test_GoToWordStart_07(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(13)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_08(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(14)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordStart_09(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(25)

        editor.GotoWordStart()
        self.assertEqual(editor.GetCurrentPosition(), 13)

    def test_GoToWordEnd_01(self):
        text = ''
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 0)

    def test_GoToWordEnd_02(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(0)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_03(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(1)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 5)

    def test_GoToWordEnd_04(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(6)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_05(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(12)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 12)

    def test_GoToWordEnd_06(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(13)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_07(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(14)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_GoToWordEnd_08(self):
        text = 'слово слово2 ещеоднослово'
        editor = self._getEditor()
        editor.SetText(text)
        editor.GotoPos(25)

        editor.GotoWordEnd()
        self.assertEqual(editor.GetCurrentPosition(), 25)

    def test_WordStartPosition_01(self):
        text = ''
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(0)

        self.assertEqual(wordStart, 0)

    def test_WordStartPosition_02(self):
        text = 'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(0)

        self.assertEqual(wordStart, 0)

    def test_WordStartPosition_03(self):
        text = 'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(3)

        self.assertEqual(wordStart, 0)

    def test_WordStartPosition_04(self):
        text = ' слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(3)

        self.assertEqual(wordStart, 1)

    def test_WordStartPosition_05(self):
        text = ' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(7)

        self.assertEqual(wordStart, 7)

    def test_WordStartPosition_06(self):
        text = ' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordStart = editor.WordStartPosition(9)

        self.assertEqual(wordStart, 7)

    def test_WordEndPosition_01(self):
        text = ''
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(0)

        self.assertEqual(wordEnd, 0)

    def test_WordEndPosition_02(self):
        text = 'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(0)

        self.assertEqual(wordEnd, 5)

    def test_WordEndPosition_03(self):
        text = 'слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(3)

        self.assertEqual(wordEnd, 5)

    def test_WordEndPosition_04(self):
        text = ' слово'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(3)

        self.assertEqual(wordEnd, 6)

    def test_WordEndPosition_05(self):
        text = ' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(7)

        self.assertEqual(wordEnd, 13)

    def test_WordEndPosition_06(self):
        text = ' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        wordEnd = editor.WordEndPosition(9)

        self.assertEqual(wordEnd, 13)

    def test_GetWord_01(self):
        text = ''
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(0)

        self.assertEqual(word, '')

    def test_GetWord_02(self):
        text = ''
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(10)

        self.assertEqual(word, '')

    def test_GetWord_03(self):
        text = 'слово'
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(0)

        self.assertEqual(word, 'слово')

    def test_GetWord_04(self):
        text = ' слово '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(1)

        self.assertEqual(word, 'слово')

    def test_GetWord_05(self):
        text = ' слово '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(6)

        self.assertEqual(word, 'слово')

    def test_GetWord_06(self):
        text = ' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(7)

        self.assertEqual(word, 'слово2')

    def test_GetWord_07(self):
        text = ' слово слово2'
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(13)

        self.assertEqual(word, 'слово2')

    def test_GetWord_08(self):
        text = ' слово слово2 '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(13)

        self.assertEqual(word, 'слово2')

    def test_GetWord_09(self):
        text = ' слово слово2 '
        editor = self._getEditor()
        editor.SetText(text)
        word = editor.GetWord(100)

        self.assertEqual(word, '')
