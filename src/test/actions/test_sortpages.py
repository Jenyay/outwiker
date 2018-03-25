# -*- coding: utf-8 -*-

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.actions.sortchildalpha import SortChildAlphabeticalAction
from outwiker.actions.sortsiblingsalpha import SortSiblingsAlphabeticalAction
from test.basetestcases import BaseOutWikerGUITest


class SortPagesTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testChildrenRoot (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, "Страница 1", [])
        factory.create (self.wikiroot, "Страница 2", [])
        factory.create (self.wikiroot, "Страница 3", [])
        factory.create (self.wikiroot, "Страница 4", [])
        factory.create (self.wikiroot, "Страница 5", [])
        factory.create (self.wikiroot, "Страница 6", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 5"].order = 1
        self.wikiroot["Страница 2"].order = 2
        self.wikiroot["Страница 6"].order = 3
        self.wikiroot["Страница 4"].order = 4
        self.wikiroot["Страница 3"].order = 5

        self.assertEqual (self.wikiroot["Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Страница 2"].order, 2)
        self.assertEqual (self.wikiroot["Страница 3"].order, 5)
        self.assertEqual (self.wikiroot["Страница 4"].order, 4)
        self.assertEqual (self.wikiroot["Страница 5"].order, 1)
        self.assertEqual (self.wikiroot["Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot["Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Страница 2"].order, 1)
        self.assertEqual (self.wikiroot["Страница 3"].order, 2)
        self.assertEqual (self.wikiroot["Страница 4"].order, 3)
        self.assertEqual (self.wikiroot["Страница 5"].order, 4)
        self.assertEqual (self.wikiroot["Страница 6"].order, 5)


    def testChildrenRootEmpty (self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)


    def testChildrenSort (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, "Родитель", [])
        factory.create (parent, "Страница 1", [])
        factory.create (parent, "Страница 2", [])
        factory.create (parent, "Страница 3", [])
        factory.create (parent, "Страница 4", [])
        factory.create (parent, "Страница 5", [])
        factory.create (parent, "Страница 6", [])

        self.wikiroot["Родитель/Страница 1"].order = 0
        self.wikiroot["Родитель/Страница 5"].order = 1
        self.wikiroot["Родитель/Страница 2"].order = 2
        self.wikiroot["Родитель/Страница 6"].order = 3
        self.wikiroot["Родитель/Страница 4"].order = 4
        self.wikiroot["Родитель/Страница 3"].order = 5

        self.assertEqual (self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Родитель/Страница 2"].order, 2)
        self.assertEqual (self.wikiroot["Родитель/Страница 3"].order, 5)
        self.assertEqual (self.wikiroot["Родитель/Страница 4"].order, 4)
        self.assertEqual (self.wikiroot["Родитель/Страница 5"].order, 1)
        self.assertEqual (self.wikiroot["Родитель/Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = parent

        self.application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Родитель/Страница 2"].order, 1)
        self.assertEqual (self.wikiroot["Родитель/Страница 3"].order, 2)
        self.assertEqual (self.wikiroot["Родитель/Страница 4"].order, 3)
        self.assertEqual (self.wikiroot["Родитель/Страница 5"].order, 4)
        self.assertEqual (self.wikiroot["Родитель/Страница 6"].order, 5)


    def testChildrenEmpty (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, "Родитель", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = parent
        self.application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)


    def testSiblingsRoot (self):
        factory = TextPageFactory()
        factory.create (self.wikiroot, "Страница 1", [])
        factory.create (self.wikiroot, "Страница 2", [])
        factory.create (self.wikiroot, "Страница 3", [])
        factory.create (self.wikiroot, "Страница 4", [])
        factory.create (self.wikiroot, "Страница 5", [])
        factory.create (self.wikiroot, "Страница 6", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 5"].order = 1
        self.wikiroot["Страница 2"].order = 2
        self.wikiroot["Страница 6"].order = 3
        self.wikiroot["Страница 4"].order = 4
        self.wikiroot["Страница 3"].order = 5

        self.assertEqual (self.wikiroot["Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Страница 2"].order, 2)
        self.assertEqual (self.wikiroot["Страница 3"].order, 5)
        self.assertEqual (self.wikiroot["Страница 4"].order, 4)
        self.assertEqual (self.wikiroot["Страница 5"].order, 1)
        self.assertEqual (self.wikiroot["Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction (SortSiblingsAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot["Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Страница 2"].order, 2)
        self.assertEqual (self.wikiroot["Страница 3"].order, 5)
        self.assertEqual (self.wikiroot["Страница 4"].order, 4)
        self.assertEqual (self.wikiroot["Страница 5"].order, 1)
        self.assertEqual (self.wikiroot["Страница 6"].order, 3)


    def testSiblingsChildren (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, "Родитель", [])
        factory.create (parent, "Страница 1", [])
        factory.create (parent, "Страница 2", [])
        factory.create (parent, "Страница 3", [])
        factory.create (parent, "Страница 4", [])
        factory.create (parent, "Страница 5", [])
        factory.create (parent, "Страница 6", [])

        self.wikiroot["Родитель/Страница 1"].order = 0
        self.wikiroot["Родитель/Страница 5"].order = 1
        self.wikiroot["Родитель/Страница 2"].order = 2
        self.wikiroot["Родитель/Страница 6"].order = 3
        self.wikiroot["Родитель/Страница 4"].order = 4
        self.wikiroot["Родитель/Страница 3"].order = 5

        self.assertEqual (self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Родитель/Страница 2"].order, 2)
        self.assertEqual (self.wikiroot["Родитель/Страница 3"].order, 5)
        self.assertEqual (self.wikiroot["Родитель/Страница 4"].order, 4)
        self.assertEqual (self.wikiroot["Родитель/Страница 5"].order, 1)
        self.assertEqual (self.wikiroot["Родитель/Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Родитель/Страница 2"]

        self.application.actionController.getAction (SortSiblingsAlphabeticalAction.stringId).run(None)

        self.assertEqual (self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual (self.wikiroot["Родитель/Страница 2"].order, 1)
        self.assertEqual (self.wikiroot["Родитель/Страница 3"].order, 2)
        self.assertEqual (self.wikiroot["Родитель/Страница 4"].order, 3)
        self.assertEqual (self.wikiroot["Родитель/Страница 5"].order, 4)
        self.assertEqual (self.wikiroot["Родитель/Страница 6"].order, 5)


    def testSiblingsEmpty_01 (self):
        factory = TextPageFactory()
        parent = factory.create (self.wikiroot, "Родитель", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = parent
        self.application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)


    def testSiblingsEmpty_02 (self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.application.actionController.getAction (SortChildAlphabeticalAction.stringId).run(None)
