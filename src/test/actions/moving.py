# -*- coding: UTF-8 -*-

import wx

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.actions.moving import GoToParentAction


class MovingActionTest (BaseMainWndTest):
    """
    Tests for moving on pages
    """
    def setUp (self):
        super (MovingActionTest, self).setUp()


    def tearDown (self):
        super (MovingActionTest, self).tearDown()


    def test_goToParent_01 (self):
        Application.wikiroot = None
        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, None)


    def test_goToParent_02 (self):
        self._createWikiPages()
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None
        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, None)


    def test_goToParent_03 (self):
        self._createWikiPages()
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]
        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, None)


    def test_goToParent_04 (self):
        self._createWikiPages()
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1/Страница 1 - 1"]
        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])


    def test_goToParent_05 (self):
        self._createWikiPages()
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1/Страница 1 - 4"]
        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])


    def test_goToParent_05 (self):
        self._createWikiPages()
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1/Страница 1 - 4/Страница 1 - 4 - 1"]

        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1/Страница 1 - 4"])

        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, self.wikiroot[u"Страница 1"])

        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, None)

        Application.actionController.getAction (GoToParentAction.stringId).run(None)
        self.assertEqual (Application.selectedPage, None)


    def _createWikiPages (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot, u"Страница 3", [])

        factory.create (self.wikiroot[u"Страница 1"], u"Страница 1 - 1", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 1 - 2", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 1 - 3", [])
        factory.create (self.wikiroot[u"Страница 1"], u"Страница 1 - 4", [])

        factory.create (self.wikiroot[u"Страница 1/Страница 1 - 4"], u"Страница 1 - 4 - 1", [])

        factory.create (self.wikiroot[u"Страница 2"], u"Страница 2 - 1", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 2 - 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 2 - 3", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 2 - 4", [])
