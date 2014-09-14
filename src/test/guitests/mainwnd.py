# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.pages.text.textpage import TextPageFactory

from .basemainwnd import BaseMainWndTest


class MainWndTest(BaseMainWndTest):
    def setUp (self):
        BaseMainWndTest.setUp (self)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])
        factory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [])


    def testProperties (self):
        self.assertNotEqual (None, self.wnd.treePanel.panel)
        self.assertNotEqual (None, self.wnd.pagePanel)
        self.assertNotEqual (None, self.wnd.attachPanel)
        self.assertNotEqual (None, self.wnd.mainMenu)
        self.assertNotEqual (None, self.wnd.toolbars)
        self.assertNotEqual (None, self.wnd.statusbar)
        self.assertNotEqual (None, self.wnd.taskBarIcon)

        self.assertNotEqual (None, self.wnd.mainWindowConfig)
        self.wnd.mainToolbar.Realize()


    def testTitle1 (self):
        conf = MainWindowConfig (Application.config)
        conf.titleFormat.value = u"OutWiker - {page} - {file}"

        self.assertEqual (self.wnd.GetTitle(), u"OutWiker")

        Application.wikiroot = self.wikiroot
        self.assertEqual (self.wnd.GetTitle(), u"OutWiker -  - Пример вики бла-бла-бла")

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 1"]
        self.assertEqual (self.wnd.GetTitle(), u"OutWiker - Страница 1 - Пример вики бла-бла-бла")

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]
        self.assertEqual (self.wnd.GetTitle(), u"OutWiker - Страница 3 - Пример вики бла-бла-бла")


    def testTitle2 (self):
        conf = MainWindowConfig (Application.config)
        conf.titleFormat.value = u"{file} - {page} - OutWiker"

        self.assertEqual (self.wnd.GetTitle(), u"OutWiker")

        Application.wikiroot = self.wikiroot
        self.assertEqual (self.wnd.GetTitle(), u"Пример вики бла-бла-бла -  - OutWiker")

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 1"]
        self.assertEqual (self.wnd.GetTitle(), u"Пример вики бла-бла-бла - Страница 1 - OutWiker")

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]
        self.assertEqual (self.wnd.GetTitle(), u"Пример вики бла-бла-бла - Страница 3 - OutWiker")
