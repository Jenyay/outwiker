# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.actions.sortchildalpha import SortChildAlphabeticalAction
from outwiker.actions.sortsiblingsalpha import SortSiblingsAlphabeticalAction

from test.guitests.basemainwnd import BaseMainWndTest


class SortPagesTest(BaseMainWndTest):
    def testChildrenRoot (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot, u"Страница 3", [])
        factory.create (self.wikiroot, u"Страница 4", [])
        factory.create (self.wikiroot, u"Страница 5", [])
        factory.create (self.wikiroot, u"Страница 6", [])

        self.wikiroot[u"Страница 1"].order = 0
        self.wikiroot[u"Страница 5"].order = 1
        self.wikiroot[u"Страница 2"].order = 2
        self.wikiroot[u"Страница 6"].order = 3
        self.wikiroot[u"Страница 4"].order = 4
        self.wikiroot[u"Страница 3"].order = 5

        self.assertEqual (self.wikiroot[u"Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Страница 2"].order, 2)
        self.assertEqual (self.wikiroot[u"Страница 3"].order, 5)
        self.assertEqual (self.wikiroot[u"Страница 4"].order, 4)
        self.assertEqual (self.wikiroot[u"Страница 5"].order, 1)
        self.assertEqual (self.wikiroot[u"Страница 6"].order, 3)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot[u"Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Страница 2"].order, 1)
        self.assertEqual (self.wikiroot[u"Страница 3"].order, 2)
        self.assertEqual (self.wikiroot[u"Страница 4"].order, 3)
        self.assertEqual (self.wikiroot[u"Страница 5"].order, 4)
        self.assertEqual (self.wikiroot[u"Страница 6"].order, 5)


    def testChildrenRootEmpty (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None
        Application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)


    def testChildrenSort (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, u"Родитель", [])
        factory.create (parent, u"Страница 1", [])
        factory.create (parent, u"Страница 2", [])
        factory.create (parent, u"Страница 3", [])
        factory.create (parent, u"Страница 4", [])
        factory.create (parent, u"Страница 5", [])
        factory.create (parent, u"Страница 6", [])

        self.wikiroot[u"Родитель/Страница 1"].order = 0
        self.wikiroot[u"Родитель/Страница 5"].order = 1
        self.wikiroot[u"Родитель/Страница 2"].order = 2
        self.wikiroot[u"Родитель/Страница 6"].order = 3
        self.wikiroot[u"Родитель/Страница 4"].order = 4
        self.wikiroot[u"Родитель/Страница 3"].order = 5

        self.assertEqual (self.wikiroot[u"Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 2"].order, 2)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 3"].order, 5)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 4"].order, 4)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 5"].order, 1)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 6"].order, 3)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = parent

        Application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot[u"Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 2"].order, 1)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 3"].order, 2)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 4"].order, 3)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 5"].order, 4)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 6"].order, 5)


    def testChildrenEmpty (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, u"Родитель", [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = parent
        Application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)


    def testSiblingsRoot (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot, u"Страница 3", [])
        factory.create (self.wikiroot, u"Страница 4", [])
        factory.create (self.wikiroot, u"Страница 5", [])
        factory.create (self.wikiroot, u"Страница 6", [])

        self.wikiroot[u"Страница 1"].order = 0
        self.wikiroot[u"Страница 5"].order = 1
        self.wikiroot[u"Страница 2"].order = 2
        self.wikiroot[u"Страница 6"].order = 3
        self.wikiroot[u"Страница 4"].order = 4
        self.wikiroot[u"Страница 3"].order = 5

        self.assertEqual (self.wikiroot[u"Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Страница 2"].order, 2)
        self.assertEqual (self.wikiroot[u"Страница 3"].order, 5)
        self.assertEqual (self.wikiroot[u"Страница 4"].order, 4)
        self.assertEqual (self.wikiroot[u"Страница 5"].order, 1)
        self.assertEqual (self.wikiroot[u"Страница 6"].order, 3)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Application.actionController.getAction (SortSiblingsAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot[u"Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Страница 2"].order, 2)
        self.assertEqual (self.wikiroot[u"Страница 3"].order, 5)
        self.assertEqual (self.wikiroot[u"Страница 4"].order, 4)
        self.assertEqual (self.wikiroot[u"Страница 5"].order, 1)
        self.assertEqual (self.wikiroot[u"Страница 6"].order, 3)


    def testSiblingsChildren (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, u"Родитель", [])
        factory.create (parent, u"Страница 1", [])
        factory.create (parent, u"Страница 2", [])
        factory.create (parent, u"Страница 3", [])
        factory.create (parent, u"Страница 4", [])
        factory.create (parent, u"Страница 5", [])
        factory.create (parent, u"Страница 6", [])

        self.wikiroot[u"Родитель/Страница 1"].order = 0
        self.wikiroot[u"Родитель/Страница 5"].order = 1
        self.wikiroot[u"Родитель/Страница 2"].order = 2
        self.wikiroot[u"Родитель/Страница 6"].order = 3
        self.wikiroot[u"Родитель/Страница 4"].order = 4
        self.wikiroot[u"Родитель/Страница 3"].order = 5

        self.assertEqual (self.wikiroot[u"Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 2"].order, 2)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 3"].order, 5)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 4"].order, 4)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 5"].order, 1)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 6"].order, 3)

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Родитель/Страница 2"]

        Application.actionController.getAction (SortSiblingsAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot[u"Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 2"].order, 1)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 3"].order, 2)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 4"].order, 3)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 5"].order, 4)
        self.assertEqual (self.wikiroot[u"Родитель/Страница 6"].order, 5)


    def testSiblingsEmpty_01 (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, u"Родитель", [])

        Application.wikiroot = self.wikiroot
        Application.selectedPage = parent
        Application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)


    def testSiblingsEmpty_02 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None
        Application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)
