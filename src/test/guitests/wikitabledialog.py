# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tabledialog import TableDialog
from outwiker.pages.wiki.tabledialogcontroller import TableDialogController


class WikiTableDialogTest (BaseMainWndTest):
    def setUp (self):
        super (WikiTableDialogTest, self).setUp()
        self._application = Application

        factory = WikiPageFactory()
        self._testpage = factory.create (self.wikiroot, u"Страница 1", [])


    def tearDown (self):
        super (WikiTableDialogTest, self).tearDown()


    def testDefault (self):
        suffix = u''
        dlg = TableDialog (self.wnd)
        Tester.dialogTester.appendOk()

        controller = TableDialogController (dlg, suffix, self._application.config)
        controller.showDialog()

        result = controller.getResult()

        validResult = u'''(:table:)
(:tableend:)'''

        self.assertEqual (result, validResult, result)
