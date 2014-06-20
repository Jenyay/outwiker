# -*- coding: UTF-8 -*-

from basemainwnd import BaseMainWndTest
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.actions.polyactionsid import *
from test.utils import removeWiki


class HtmlActionsTest (BaseMainWndTest):
    """
    Тесты действий для HTML-страницы
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self._turnSyntax = [
            (BOLD_STR_ID, "<b>", "</b>"),
            (ITALIC_STR_ID, "<i>", "</i>"),
            (BOLD_ITALIC_STR_ID, "<b><i>", "</i></b>"),
            (UNDERLINE_STR_ID, "<u>", "</u>"),
            (STRIKE_STR_ID, "<strike>", "</strike>"),
            (SUBSCRIPT_STR_ID, "<sub>", "</sub>"),
            (SUPERSCRIPT_STR_ID, "<sup>", "</sup>"),
            (ALIGN_LEFT_STR_ID, '<div align="left">', '</div>'),
            (ALIGN_CENTER_STR_ID, '<div align="center">', '</div>'),
            (ALIGN_RIGHT_STR_ID, '<div align="right">', '</div>'),
            (ALIGN_JUSTIFY_STR_ID, '<div align="justify">', '</div>'),
            (HEADING_1_STR_ID, "<h1>", "</h1>"),
            (HEADING_2_STR_ID, "<h2>", "</h2>"),
            (HEADING_3_STR_ID, "<h3>", "</h3>"),
            (HEADING_4_STR_ID, "<h4>", "</h4>"),
            (HEADING_5_STR_ID, "<h5>", "</h5>"),
            (HEADING_6_STR_ID, "<h6>", "</h6>"),
            (PREFORMAT_STR_ID, "<pre>", "</pre>"),
            (CODE_STR_ID, "<code>", "</code>"),
            (ANCHOR_STR_ID, u'<a name="', u'"></a>'),
            (TABLE_STR_ID, u'<table>', u'</table>'),
            (TABLE_ROW_STR_ID, u'<tr>', u'</tr>'),
            (TABLE_CELL_STR_ID, u'<td>', u'</td>'),
            (QUOTE_STR_ID, u'<blockquote>', u'</blockquote>'),
            (IMAGE_STR_ID, u'<img src="', u'"/>'),
        ]

        self._replaceSyntax = [
            (HORLINE_STR_ID, u"<hr>"),
        ]

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)
        HtmlPageFactory().create (self.wikiroot, u"HTML-страница", [])
        HtmlPageFactory().create (self.wikiroot, u"temp", [])

        # Страница, куда будем переключаться перед изменением содержимого основной страницы
        # Можно было бы вместо temppage использовать None, но тогда программе
        # пришлось бы каждый раз удалять и создавать панели инструментов, что медленно
        self.temppage = self.wikiroot[u"temp"]
        self.testpage = self.wikiroot[u"HTML-страница"]

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
            self.assertEqual (self._getEditor().GetText(), u"Бла-{}-бла".format (syntax[1]))


    def testListBulletsEmpty (self):
        result = u"""<ul>
<li></li>
</ul>"""

        Application.selectedPage = self.temppage
        self.testpage.content = u""
        Application.selectedPage = self.testpage

        Application.actionController.getAction (LIST_BULLETS_STR_ID).run(None)
        self.assertEqual (self._getEditor().GetText(), result)


    def testListNumbersEmpty (self):
        result = u"""<ol>
<li></li>
</ol>"""

        Application.selectedPage = self.temppage
        self.testpage.content = u""
        Application.selectedPage = self.testpage

        Application.actionController.getAction (LIST_NUMBERS_STR_ID).run(None)
        self.assertEqual (self._getEditor().GetText(), result)


    def testListBulletsSelectedAll (self):
        text = u"""йцкуйцук
укеуке
ывапвыап
ывапвыапыап
ывапываппа"""

        result = u"""<ul>
<li>йцкуйцук</li>
<li>укеуке</li>
<li>ывапвыап</li>
<li>ывапвыапыап</li>
<li>ывапываппа</li>
</ul>"""

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

        result = u"""<ol>
<li>йцкуйцук</li>
<li>укеуке</li>
<li>ывапвыап</li>
<li>ывапвыапыап</li>
<li>ывапываппа</li>
</ol>"""

        Application.selectedPage = self.temppage
        self.testpage.content = text
        Application.selectedPage = self.testpage

        self._getEditor().SetSelection (0, len (text))

        Application.actionController.getAction (LIST_NUMBERS_STR_ID).run(None)
        self.assertEqual (self._getEditor().GetText(), result)
