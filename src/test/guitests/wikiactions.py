#!/usr/bin/python
# -*- coding: UTF-8 -*-

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.actions.polyactionsid import *
from test.utils import removeWiki

class WikiActionsTest (BaseMainWndTest):
    """
    Тесты действий для викистраницы
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

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
                (HEADING_1_STR_ID, "!! ", ""),
                (HEADING_2_STR_ID, "!!! ", ""),
                (HEADING_3_STR_ID, "!!!! ", ""),
                (HEADING_4_STR_ID, "!!!!! ", ""),
                (HEADING_5_STR_ID, "!!!!!! ", ""),
                (HEADING_6_STR_ID, "!!!!!!! ", ""),
                (PREFORMAT_STR_ID, "[@", "@]"),
                (CODE_STR_ID, "@@", "@@"),
                (ANCHOR_STR_ID, "[[#", "]]"),
                (QUOTE_STR_ID, "[>", "<]"),
                ]

        self._replaceSyntax = [
                (HORLINE_STR_ID, u"----"),
                ]


        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory.create (self.wikiroot, u"Викистраница", [])
        WikiPageFactory.create (self.wikiroot, u"temp", [])

        # Страница, куда будем переключаться перед изменением содержимого основной страницы
        # Можно было бы вместо temppage использовать None, но тогда программе 
        # пришлось бы каждый раз удалять и создавать панели инструментов, что медленно
        self.temppage = self.wikiroot[u"temp"]
        self.testpage = self.wikiroot[u"Викистраница"]

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.testpage


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None
        removeWiki (self.path)


    def _getEditor (self):
        return Application.mainWindow.pagePanel.pageView.codeEditor


    def testTurnSyntaxEmpty (self):
        for syntax in self._turnSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = u""
            Application.selectedPage = self.testpage

            Application.actionController.getAction (syntax[0]).run(None)
            self.assertEqual (self._getEditor().GetText(), syntax[1] + syntax[2])


    def testTurnSyntaxSelectedAll (self):
        text = u"Бла-бла-бла"

        for syntax in self._turnSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection (0, len (text))

            Application.actionController.getAction (syntax[0]).run(None)
            self.assertEqual (self._getEditor().GetText(), syntax[1] + u"Бла-бла-бла" + syntax[2])


    def testTurnSyntaxSelectedPart (self):
        text = u"Бла-бла-бла"

        for syntax in self._turnSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection (4, 7)

            Application.actionController.getAction (syntax[0]).run(None)
            self.assertEqual (self._getEditor().GetText(), u"Бла-{}бла{}-бла".format (syntax[1], syntax[2]))


    def testReplaceSyntaxEmpty (self):
        for syntax in self._replaceSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = u""
            Application.selectedPage = self.testpage

            Application.actionController.getAction (syntax[0]).run(None)
            self.assertEqual (self._getEditor().GetText(), syntax[1])


    def testReplaceSyntaxSelectedAll (self):
        text = u"Бла-бла-бла"

        for syntax in self._replaceSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection (0, len (text))

            Application.actionController.getAction (syntax[0]).run(None)
            self.assertEqual (self._getEditor().GetText(), syntax[1])


    def testReplaceSyntaxSelectedPart (self):
        text = u"Бла-бла-бла"

        for syntax in self._replaceSyntax:
            Application.selectedPage = self.temppage
            self.testpage.content = text
            Application.selectedPage = self.testpage

            self._getEditor().SetSelection (4, 7)

            Application.actionController.getAction (syntax[0]).run(None)
            self.assertEqual (self._getEditor().GetText(), u"Бла-{}-бла".format (syntax[1]) )


    def testListBulletsEmpty (self):
        Application.selectedPage = self.temppage
        self.testpage.content = u""
        Application.selectedPage = self.testpage

        Application.actionController.getAction (LIST_BULLETS_STR_ID).run(None)
        self.assertEqual (self._getEditor().GetText(), u"* ")


    def testListNumbersEmpty (self):
        Application.selectedPage = self.temppage
        self.testpage.content = u""
        Application.selectedPage = self.testpage

        Application.actionController.getAction (LIST_NUMBERS_STR_ID).run(None)
        self.assertEqual (self._getEditor().GetText(), u"# ")


    def testListBulletsSelectedAll (self):
        text = u"""йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = u"""* йцкуйцук
* укеуке
* ывапвыап
* ывапвыапыап
* ывапываппа"""

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection (0, len (text))

        Application.actionController.getAction (LIST_BULLETS_STR_ID).run(None)
        self.assertEqual (self._getEditor().GetText(), result)


    def testListNumbersSelectedAll (self):
        text = u"""йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = u"""# йцкуйцук
# укеуке
# ывапвыап
# ывапвыапыап
# ывапываппа"""

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection (0, len (text))

        Application.actionController.getAction (LIST_NUMBERS_STR_ID).run(None)
        self.assertEqual (self._getEditor().GetText(), result)
