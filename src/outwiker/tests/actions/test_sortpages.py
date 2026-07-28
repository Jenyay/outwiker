# -*- coding: utf-8 -*-

from datetime import datetime
import unittest

from outwiker.app.actions.sortchild import (
    SortChildAlphabeticalAction,
    SortChildByCreationDateAscAction,
    SortChildByCreationDateDescAction,
    SortChildByModifiedDateAscAction,
    SortChildByModifiedDateDescAction,
)
from outwiker.app.actions.sortsiblings import (
    SortSiblingsAlphabeticalAction,
    SortSiblingsByCreationDateAscAction,
    SortSiblingsByCreationDateDescAction,
    SortSiblingsByModifiedDateAscAction,
    SortSiblingsByModifiedDateDescAction,
)
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class SortPagesTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_alphabetatical_children_root(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])
        factory.create(self.wikiroot, "Страница 4", [])
        factory.create(self.wikiroot, "Страница 5", [])
        factory.create(self.wikiroot, "Страница 6", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 5"].order = 1
        self.wikiroot["Страница 2"].order = 2
        self.wikiroot["Страница 6"].order = 3
        self.wikiroot["Страница 4"].order = 4
        self.wikiroot["Страница 3"].order = 5

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 5)
        self.assertEqual(self.wikiroot["Страница 4"].order, 4)
        self.assertEqual(self.wikiroot["Страница 5"].order, 1)
        self.assertEqual(self.wikiroot["Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(
            SortChildAlphabeticalAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 1)
        self.assertEqual(self.wikiroot["Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Страница 4"].order, 3)
        self.assertEqual(self.wikiroot["Страница 5"].order, 4)
        self.assertEqual(self.wikiroot["Страница 6"].order, 5)

    def test_alphabetatical_children_root_empty(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.application.actionController.getAction(
            SortChildAlphabeticalAction.stringId
        ).run(None)

    def test_alphabetatical_ehildren_sort(self):
        factory = TextPageFactory()
        parent = factory.create(self.wikiroot, "Родитель", [])
        factory.create(parent, "Страница 1", [])
        factory.create(parent, "Страница 2", [])
        factory.create(parent, "Страница 3", [])
        factory.create(parent, "Страница 4", [])
        factory.create(parent, "Страница 5", [])
        factory.create(parent, "Страница 6", [])

        self.wikiroot["Родитель/Страница 1"].order = 0
        self.wikiroot["Родитель/Страница 5"].order = 1
        self.wikiroot["Родитель/Страница 2"].order = 2
        self.wikiroot["Родитель/Страница 6"].order = 3
        self.wikiroot["Родитель/Страница 4"].order = 4
        self.wikiroot["Родитель/Страница 3"].order = 5

        self.assertEqual(self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Родитель/Страница 2"].order, 2)
        self.assertEqual(self.wikiroot["Родитель/Страница 3"].order, 5)
        self.assertEqual(self.wikiroot["Родитель/Страница 4"].order, 4)
        self.assertEqual(self.wikiroot["Родитель/Страница 5"].order, 1)
        self.assertEqual(self.wikiroot["Родитель/Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = parent

        self.application.actionController.getAction(
            SortChildAlphabeticalAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Родитель/Страница 2"].order, 1)
        self.assertEqual(self.wikiroot["Родитель/Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Родитель/Страница 4"].order, 3)
        self.assertEqual(self.wikiroot["Родитель/Страница 5"].order, 4)
        self.assertEqual(self.wikiroot["Родитель/Страница 6"].order, 5)

    def test_alphabetatical_children_empty(self):
        factory = TextPageFactory()
        parent = factory.create(self.wikiroot, "Родитель", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = parent
        self.application.actionController.getAction(
            SortChildAlphabeticalAction.stringId
        ).run(None)

    def test_alphabetatical_siblings_root(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])
        factory.create(self.wikiroot, "Страница 4", [])
        factory.create(self.wikiroot, "Страница 5", [])
        factory.create(self.wikiroot, "Страница 6", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 5"].order = 1
        self.wikiroot["Страница 2"].order = 2
        self.wikiroot["Страница 6"].order = 3
        self.wikiroot["Страница 4"].order = 4
        self.wikiroot["Страница 3"].order = 5

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 5)
        self.assertEqual(self.wikiroot["Страница 4"].order, 4)
        self.assertEqual(self.wikiroot["Страница 5"].order, 1)
        self.assertEqual(self.wikiroot["Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(
            SortSiblingsAlphabeticalAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)
        self.assertEqual(self.wikiroot["Страница 3"].order, 5)
        self.assertEqual(self.wikiroot["Страница 4"].order, 4)
        self.assertEqual(self.wikiroot["Страница 5"].order, 1)
        self.assertEqual(self.wikiroot["Страница 6"].order, 3)

    def test_alphabetatical_siblings_children(self):
        factory = TextPageFactory()
        parent = factory.create(self.wikiroot, "Родитель", [])
        factory.create(parent, "Страница 1", [])
        factory.create(parent, "Страница 2", [])
        factory.create(parent, "Страница 3", [])
        factory.create(parent, "Страница 4", [])
        factory.create(parent, "Страница 5", [])
        factory.create(parent, "Страница 6", [])

        self.wikiroot["Родитель/Страница 1"].order = 0
        self.wikiroot["Родитель/Страница 5"].order = 1
        self.wikiroot["Родитель/Страница 2"].order = 2
        self.wikiroot["Родитель/Страница 6"].order = 3
        self.wikiroot["Родитель/Страница 4"].order = 4
        self.wikiroot["Родитель/Страница 3"].order = 5

        self.assertEqual(self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Родитель/Страница 2"].order, 2)
        self.assertEqual(self.wikiroot["Родитель/Страница 3"].order, 5)
        self.assertEqual(self.wikiroot["Родитель/Страница 4"].order, 4)
        self.assertEqual(self.wikiroot["Родитель/Страница 5"].order, 1)
        self.assertEqual(self.wikiroot["Родитель/Страница 6"].order, 3)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Родитель/Страница 2"]

        self.application.actionController.getAction(
            SortSiblingsAlphabeticalAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Родитель/Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Родитель/Страница 2"].order, 1)
        self.assertEqual(self.wikiroot["Родитель/Страница 3"].order, 2)
        self.assertEqual(self.wikiroot["Родитель/Страница 4"].order, 3)
        self.assertEqual(self.wikiroot["Родитель/Страница 5"].order, 4)
        self.assertEqual(self.wikiroot["Родитель/Страница 6"].order, 5)

    def test_alphabetatical_siblings_empty_01(self):
        factory = TextPageFactory()
        parent = factory.create(self.wikiroot, "Родитель", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = parent
        self.application.actionController.getAction(
            SortChildAlphabeticalAction.stringId
        ).run(None)

    def test_alphabetatical_siblings_empty_02(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None
        self.application.actionController.getAction(
            SortChildAlphabeticalAction.stringId
        ).run(None)

    def test_creation_date_asc_children(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].creationdatetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].creationdatetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].creationdatetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(
            SortChildByCreationDateAscAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 2"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 1"].order, 2)

    def test_creation_date_desc_children(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].creationdatetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].creationdatetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].creationdatetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(
            SortChildByCreationDateDescAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)

    def test_modified_date_asc_children(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].datetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].datetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].datetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(
            SortChildByModifiedDateAscAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 2"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 1"].order, 2)

    def test_modified_date_desc_children(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].datetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].datetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].datetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(
            SortChildByModifiedDateDescAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)

    def test_creation_date_asc_siblings(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].creationdatetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].creationdatetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].creationdatetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(
            SortSiblingsByCreationDateAscAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 2"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 1"].order, 2)

    def test_creation_date_desc_siblings(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].creationdatetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].creationdatetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].creationdatetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(
            SortSiblingsByCreationDateDescAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)

    def test_modified_date_asc_siblings(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].datetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].datetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].datetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(
            SortSiblingsByModifiedDateAscAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 2"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 1"].order, 2)

    def test_modified_date_desc_siblings(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])

        self.wikiroot["Страница 1"].order = 0
        self.wikiroot["Страница 2"].order = 1
        self.wikiroot["Страница 3"].order = 2

        self.wikiroot["Страница 1"].datetime = datetime(2026, 7, 15)
        self.wikiroot["Страница 2"].datetime = datetime(2026, 7, 13)
        self.wikiroot["Страница 3"].datetime = datetime(2026, 7, 14)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(
            SortSiblingsByModifiedDateDescAction.stringId
        ).run(None)

        self.assertEqual(self.wikiroot["Страница 1"].order, 0)
        self.assertEqual(self.wikiroot["Страница 3"].order, 1)
        self.assertEqual(self.wikiroot["Страница 2"].order, 2)
