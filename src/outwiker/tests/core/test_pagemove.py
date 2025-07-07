# -*- coding: utf-8 -*-
"""
Тесты на перемещение заметок по дереву
"""

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.exceptions import DuplicateTitle, TreeException
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment

from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


class MoveTest(unittest.TestCase):
    """
    Тест для проверки перемещения заметок по дереву
    """

    def setUp(self):
        # Количество срабатываний особытий при обновлении страницы
        self.treeUpdateCount = 0
        self.treeUpdateSender = None
        self._application = Application()

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wiki = createNotesTree(self.path)

        factory = TextPageFactory()
        factory.create(self.wiki, "Страница 1", [])
        factory.create(self.wiki, "Страница 2", [])
        factory.create(self.wiki["Страница 2"], "Страница 3", [])
        factory.create(self.wiki["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wiki["Страница 1"], "Страница 5", [])
        factory.create(self.wiki, "страница 4", [])
        factory.create(self.wiki, "страница 444", [])

        self._application.wikiroot = None

    def tearDown(self):
        removeDir(self.path)
        self._application.wikiroot = None

    def onTreeUpdate(self, sender):
        self.treeUpdateCount += 1
        self.treeUpdateSender = sender

    def test1(self):
        self.treeUpdateCount = 0
        self._application.wikiroot = self.wiki

        self._application.onTreeUpdate += self.onTreeUpdate

        self.wiki["Страница 1/Страница 5"].moveTo(self.wiki)

        self.assertEqual(self.treeUpdateCount, 1)

        self.assertEqual(len(self.wiki["Страница 1"]), 0)
        self.assertEqual(len(self.wiki), 5)
        self.assertEqual(self.wiki["Страница 5"].title, "Страница 5")
        self.assertEqual(self.wiki["Страница 5"].parent, self.wiki)
        self.assertEqual(self.wiki["Страница 5"].parent, self.wiki)
        self.assertEqual(self.wiki["Страница 5"].subpath, "Страница 5")

        self._application.onTreeUpdate += self.onTreeUpdate

    def testNoEvent(self):
        self.treeUpdateCount = 0
        self._application.wikiroot = None

        self._application.onTreeUpdate += self.onTreeUpdate

        self.wiki["Страница 1/Страница 5"].moveTo(self.wiki)

        self.assertEqual(self.treeUpdateCount, 0)

        self.assertEqual(len(self.wiki["Страница 1"]), 0)
        self.assertEqual(len(self.wiki), 5)
        self.assertEqual(self.wiki["Страница 5"].title, "Страница 5")
        self.assertEqual(self.wiki["Страница 5"].parent, self.wiki)
        self.assertEqual(self.wiki["Страница 5"].parent, self.wiki)
        self.assertEqual(self.wiki["Страница 5"].subpath, "Страница 5")

        self._application.onTreeUpdate += self.onTreeUpdate

    def test2(self):
        self.wiki["Страница 1"].moveTo(self.wiki["Страница 2/Страница 3"])

        self.assertEqual(self.wiki["Страница 1"], None)
        self.assertTrue(
            os.path.exists(
                os.path.join(self.wiki["Страница 2/Страница 3"].path,
                             "Страница 1")
            )
        )

        self.assertEqual(len(self.wiki["Страница 2/Страница 3"]), 2)
        self.assertEqual(len(self.wiki), 3)
        self.assertEqual(self.wiki["Страница 2/Страница 3/Страница 1"].title,
                         "Страница 1")
        self.assertEqual(
            self.wiki["Страница 2/Страница 3/Страница 1/Страница 5"].title,
            "Страница 5"
        )
        self.assertEqual(
            self.wiki["Страница 2/Страница 3/Страница 1"].subpath,
            "Страница 2/Страница 3/Страница 1"
        )

        self.assertEqual(
            self.wiki["Страница 2/Страница 3/Страница 1/Страница 5"].subpath,
            "Страница 2/Страница 3/Страница 1/Страница 5")

    def test3(self):
        self.assertRaises(
            DuplicateTitle,
            self.wiki["Страница 2/Страница 3/Страница 4"].moveTo,
            self.wiki
        )

    def test4(self):
        self.wiki["страница 4"].moveTo(self.wiki["страница 444"])

        self.assertEqual(self.wiki["страница 4"], None)
        self.assertTrue(os.path.exists(
            os.path.join(self.wiki["страница 444"].path,
                         "страница 4")))
        self.assertEqual(len(self.wiki["страница 444"]), 1)
        self.assertEqual(self.wiki["страница 444/страница 4"].title,
                         "страница 4")

    def testMoveToSelf(self):
        self.assertRaises(TreeException,
                          self.wiki["Страница 1"].moveTo,
                          self.wiki["Страница 1"])

        self.assertNotEqual(self.wiki["Страница 1"], None)
        self.assertEqual(len(self.wiki), 4)

    def testMoveToChild1(self):
        self.assertRaises(TreeException,
                          self.wiki["Страница 2"].moveTo,
                          self.wiki["Страница 2/Страница 3"])

        self.assertNotEqual(self.wiki["Страница 2"], None)
        self.assertEqual(len(self.wiki), 4)

    def testMoveToChild2(self):
        self.assertRaises(TreeException,
                          self.wiki["Страница 2"].moveTo,
                          self.wiki["Страница 2/Страница 3/Страница 4"])

        self.assertNotEqual(self.wiki["Страница 2"], None)
        self.assertEqual(len(self.wiki), 4)

    def testMoveInvalid(self):
        """
        А что, если кто-то блокирует папку с заметкой?
        """
        page = self.wiki["Страница 1"]
        attachname = "add.png"

        attach = Attachment(page)
        attach.attach([os.path.join("testdata/samplefiles", attachname)])

        # Откроем на запись файл в папке с вложениями,
        # чтобы нельзя было переместить папку
        with open(attach.getFullPath("lock.tmp", True), "w"):
            try:
                page.moveTo(self.wiki["Страница 2/Страница 3"])
            except TreeException:
                # Если не удалось переместить страницу
                self.assertEqual(
                    self.wiki["Страница 2/Страница 3/Страница 1"],
                    None
                )
                self.assertNotEqual(self.wiki["Страница 1"], None)
                self.assertEqual(len(self.wiki["Страница 2/Страница 3"]), 1)

                self.assertTrue(os.path.exists(page.path))
                self.assertFalse(os.path.exists(
                    os.path.join(self.wiki["Страница 2/Страница 3"].path,
                                 "Страница 1")))

                self.assertTrue(os.path.exists(attach.getFullPath(attachname)))
            else:
                # А если страницу переместить удалось, то проверим,
                # что она действительно перенеслась
                self.assertEqual(self.wiki["Страница 1"], None)
                self.assertTrue(
                    os.path.exists(
                        os.path.join(
                            self.wiki["Страница 2/Страница 3"].path,
                            "Страница 1")
                    )
                )

                self.assertEqual(len(self.wiki["Страница 2/Страница 3"]), 2)
                self.assertEqual(len(self.wiki), 3)
                self.assertEqual(
                    self.wiki["Страница 2/Страница 3/Страница 1"].title,
                    "Страница 1"
                )
                self.assertEqual(
                    self.wiki["Страница 2/Страница 3/Страница 1/Страница 5"].title,
                    "Страница 5"
                )
                self.assertEqual(
                    self.wiki["Страница 2/Страница 3/Страница 1"].subpath,
                    "Страница 2/Страница 3/Страница 1")
                self.assertEqual(
                    self.wiki["Страница 2/Страница 3/Страница 1/Страница 5"].subpath,
                    "Страница 2/Страница 3/Страница 1/Страница 5")
