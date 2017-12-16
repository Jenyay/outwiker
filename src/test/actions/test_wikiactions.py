# -*- coding: UTF-8 -*-

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.actions.polyactionsid import *


class WikiActionsTest(BaseMainWndTest):
    """
    Тесты действий для викистраницы
    """
    def setUp(self):
        BaseMainWndTest.setUp(self)

        self._turnSyntax = [
            (BOLD_STR_ID, "'''", "'''"),
            (ITALIC_STR_ID, "''", "''"),
            (BOLD_ITALIC_STR_ID, "''''", "''''"),
            (UNDERLINE_STR_ID, "{+", "+}"),
            (STRIKE_STR_ID, "{-", "-}"),
            (SUBSCRIPT_STR_ID, "'_", "_'"),
            (SUPERSCRIPT_STR_ID, "'^", "^'"),
            (ALIGN_LEFT_STR_ID, "%left%", ""),
            (ALIGN_CENTER_STR_ID, "%center%", ""),
            (ALIGN_RIGHT_STR_ID, "%right%", ""),
            (ALIGN_JUSTIFY_STR_ID, "%justify%", ""),
            (PREFORMAT_STR_ID, "[@", "@]"),
            (CODE_STR_ID, "@@", "@@"),
            (ANCHOR_STR_ID, "[[#", "]]"),
            (QUOTE_STR_ID, "[>", "<]"),
        ]

        self._replaceSyntax = [
            (HORLINE_STR_ID, "----"),
        ]

        self._headingsSyntax = [
            (HEADING_1_STR_ID, '!!'),
            (HEADING_2_STR_ID, '!!!'),
            (HEADING_3_STR_ID, '!!!!'),
            (HEADING_4_STR_ID, '!!!!!'),
            (HEADING_5_STR_ID, '!!!!!!'),
            (HEADING_6_STR_ID, '!!!!!!!'),
        ]

        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        WikiPageFactory().create(self.wikiroot, "temp", [])

        # Страница, куда будем переключаться перед изменением содержимого
        # основной страницы. Можно было бы вместо temppage использовать None,
        # но тогда программе пришлось бы каждый раз удалять и создавать панели
        # инструментов, что медленно
        self.temppage = self.wikiroot["temp"]
        self.testpage = self.wikiroot["Викистраница"]

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.testpage

    def _getEditor(self):
        return Application.mainWindow.pagePanel.pageView.codeEditor

    def testTurnSyntaxEmpty(self):
        for syntax in self._turnSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = ""
            Application.selectedPage = self.testpage

            Application.actionController.getAction(syntax[0]).run(None)
            self.assertEqual(self._getEditor().GetText(),
                             syntax[1] + syntax[2])

    def testTurnSyntaxSelectedAll(self):
        text = "Бла-бла-бла"

        for syntax in self._turnSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection(0, len(text))

            Application.actionController.getAction(syntax[0]).run(None)
            self.assertEqual(self._getEditor().GetText(),
                             syntax[1] + "Бла-бла-бла" + syntax[2])

    def testTurnSyntaxSelectedPart(self):
        text = "Бла-бла-бла"

        for syntax in self._turnSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection(4, 7)

            Application.actionController.getAction(syntax[0]).run(None)
            self.assertEqual(
                self._getEditor().GetText(),
                "Бла-{}бла{}-бла".format(syntax[1], syntax[2]))

    def testReplaceSyntaxEmpty(self):
        for syntax in self._replaceSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = ""
            Application.selectedPage = self.testpage

            Application.actionController.getAction(syntax[0]).run(None)
            self.assertEqual(self._getEditor().GetText(), syntax[1])

    def testReplaceSyntaxSelectedAll(self):
        text = "Бла-бла-бла"

        for syntax in self._replaceSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection(0, len(text))

            Application.actionController.getAction(syntax[0]).run(None)
            self.assertEqual(self._getEditor().GetText(), syntax[1])

    def testReplaceSyntaxSelectedPart(self):
        text = "Бла-бла-бла"

        for syntax in self._replaceSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection(4, 7)

            Application.actionController.getAction(syntax[0]).run(None)
            self.assertEqual(self._getEditor().GetText(),
                             "Бла-{}-бла".format(syntax[1]))

    def testListBulletsEmpty(self):
        Application.selectedPage = self.temppage
        self.testpage.content = ""
        Application.selectedPage = self.testpage

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)
        self.assertEqual(self._getEditor().GetText(), "* ")

    def testListNumbersEmpty(self):
        Application.selectedPage = self.temppage
        self.testpage.content = ""
        Application.selectedPage = self.testpage

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)
        self.assertEqual(self._getEditor().GetText(), "# ")

    def testListBulletsSelectedAll(self):
        text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """* йцкуйцук
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(0, len(text))

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)
        self.assertEqual(self._getEditor().GetText(), result)

    def testListNumbersSelectedAll(self):
        text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """# йцкуйцук
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(0, len(text))

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)
        self.assertEqual(self._getEditor().GetText(), result)

    def testListBulletsSelectedPart_01(self):
        text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """* йцкуйцук
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

        start = 3
        end = len(text) - 3

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_01(self):
        text = """йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """# йцкуйцук
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

        start = 3
        end = len(text) - 3

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListBulletsSelectedPart_02(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

        start = 7
        end = len(text) - 3

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListBulletsSelectedPart_03(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

        start = 10
        end = len(text) - 3

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_02(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

        start = 7
        end = len(text) - 3

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_03(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

        start = 10
        end = len(text) - 3

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListBulletsSelectedPart_04(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """* йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        start = 0
        end = 0

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_04(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """# йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        start = 0
        end = 0

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListBulletsSelectedPart_05(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
* укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        start = 7
        end = 7

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_05(self):
        text = """йцукен
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
# укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        start = 7
        end = 7

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListBulletsSelectedPart_06(self):
        text = """* йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

        result = """** йцукен
** укеуке
** ывапвыап
** ывапвыапыап
** ывапываппа"""

        start = 0
        end = len(text)

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_06(self):
        text = """# йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

        result = """## йцукен
## укеуке
## ывапвыап
## ывапвыапыап
## ывапываппа"""

        start = 0
        end = len(text)

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListBulletsSelectedPart_07(self):
        text = """# йцукен
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

        result = """* # йцукен
* # укеуке
* # ывапвыап
* # ывапвыапыап
* # ывапываппа"""

        start = 0
        end = len(text)

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_07(self):
        text = """* йцукен
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

        result = """# * йцукен
# * укеуке
# * ывапвыап
# * ывапвыапыап
# * ывапываппа"""

        start = 0
        end = len(text)

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result)

    def testListBulletsSelectedPart_08(self):
        text = """йцукен
* укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
** укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        start = 7
        end = 7

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_BULLETS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def testListNumbersSelectedPart_08(self):
        text = """йцукен
# укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = """йцукен
## укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        start = 7
        end = 7

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection(start, end)

        Application.actionController.getAction(LIST_NUMBERS_STR_ID).run(None)

        self.assertEqual(self._getEditor().GetText(),
                         result,
                         self._getEditor().GetText())

    def test_heading1_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = ''
        for action_str, syntax in self._headingsSyntax:
            result = '{} '.format(syntax)

            editor.SetText(text)
            editor.SetSelection(0, 0)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             result)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             text)

    def test_heading1_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3'
        for action_str, syntax in self._headingsSyntax:
            result = '{} Строка 1\nСтрока 2\nСтрока 3'.format(syntax)

            editor.SetText(text)
            editor.SetSelection(5, 5)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             result)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             text)

    def test_heading1_03(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3'
        for action_str, syntax in self._headingsSyntax:
            result = 'Строка 1\n{} Строка 2\nСтрока 3'.format(syntax)

            editor.SetText(text)
            editor.SetSelection(10, 10)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             result)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             text)

    def test_heading1_04(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3'
        for action_str, syntax in self._headingsSyntax:
            result = '{syntax} Строка 1\n{syntax} Строка 2\nСтрока 3'.format(
                syntax=syntax)

            editor.SetText(text)
            editor.SetSelection(0, 10)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             result)

            actionController.getAction(action_str).run(None)
            self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                             text)

    def test_heading_switch_01(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3'

        editor.SetText(text)
        editor.SetSelection(0, 0)

        actionController.getAction(HEADING_1_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!! Строка 1\nСтрока 2\nСтрока 3')

        actionController.getAction(HEADING_2_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!!! Строка 1\nСтрока 2\nСтрока 3')

        actionController.getAction(HEADING_1_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!! Строка 1\nСтрока 2\nСтрока 3')

        actionController.getAction(HEADING_6_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!!!!!!! Строка 1\nСтрока 2\nСтрока 3')

        actionController.getAction(HEADING_5_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!!!!!! Строка 1\nСтрока 2\nСтрока 3')

        actionController.getAction(HEADING_5_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1\nСтрока 2\nСтрока 3')

    def test_heading_switch_02(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = 'Строка 1\nСтрока 2\nСтрока 3'

        editor.SetText(text)
        editor.SetSelection(0, 12)

        actionController.getAction(HEADING_1_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!! Строка 1\n!! Строка 2\nСтрока 3')

        actionController.getAction(HEADING_2_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!!! Строка 1\n!!! Строка 2\nСтрока 3')

        actionController.getAction(HEADING_1_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!! Строка 1\n!! Строка 2\nСтрока 3')

        actionController.getAction(HEADING_6_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!!!!!!! Строка 1\n!!!!!!! Строка 2\nСтрока 3')

        actionController.getAction(HEADING_5_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!!!!!! Строка 1\n!!!!!! Строка 2\nСтрока 3')

        actionController.getAction(HEADING_5_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         'Строка 1\nСтрока 2\nСтрока 3')

    def test_heading_switch_03(self):
        editor = self._getEditor()
        actionController = Application.actionController
        text = '! Строка 1\nСтрока 2\nСтрока 3'

        editor.SetText(text)
        editor.SetSelection(0, 0)

        actionController.getAction(HEADING_1_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '!! ! Строка 1\nСтрока 2\nСтрока 3')

        actionController.getAction(HEADING_1_STR_ID).run(None)
        self.assertEqual(editor.GetText().replace('\r\n', '\n'),
                         '! Строка 1\nСтрока 2\nСтрока 3')
