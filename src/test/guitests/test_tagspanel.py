# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.core.application import ApplicationParams
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tagspanelcontroller import TagsPanelController


class TagsPanelTest(unittest.TestCase):
    def setUp(self):
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", ["тег 1"])
        factory.create(self.wikiroot, "Страница 2", ["тег 1", "тег 2"])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", ["тег 3"])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", ["тег 4", "тег 1"])

    def tearDown(self):
        removeDir(self.path)

    def testCreateTagsPanelController(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()

        self.assertEqual(panel.tags, [])

        TagsPanelController(panel, application)

        self.assertTrue("тег 1" in panel.tags)
        self.assertTrue("тег 2" in panel.tags)
        self.assertTrue("тег 3" in panel.tags)
        self.assertTrue("тег 4" in panel.tags)

        self.assertEqual(panel.marks, [])

    def testSelectPage1(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        TagsPanelController(panel, application)

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertTrue("тег 1" in panel.marks)

        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertTrue("тег 3" in panel.marks)

        self.wikiroot.selectedPage = self.wikiroot["Страница 1/Страница 5"]
        self.assertTrue("тег 1" in panel.marks)
        self.assertTrue("тег 4" in panel.marks)

        self.wikiroot.selectedPage = None
        self.assertEqual(panel.marks, [])

    def testSelectPage2(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        TagsPanelController(panel, application)

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertTrue("тег 1" in panel.marks)

        application.wikiroot = None
        self.assertEqual(panel.marks, [])

    def testTagsChange(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        TagsPanelController(panel, application)

        self.wikiroot.selectedPage = self.wikiroot["Страница 1"]
        self.assertTrue("тег 1" in panel.marks)

        self.wikiroot["Страница 1"].tags = ["тег 1", "тег 2", "тег 666"]
        self.assertTrue("тег 1" in panel.marks)
        self.assertTrue("тег 2" in panel.marks)
        self.assertTrue("тег 666" in panel.marks)

    def testChangeTags(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        TagsPanelController(panel, application)

        self.wikiroot["Страница 2"].tags = ["бла-бла-бла"]

        self.assertTrue("тег 1" in panel.tags)
        self.assertTrue("тег 2" not in panel.tags)
        self.assertTrue("тег 3" in panel.tags)
        self.assertTrue("тег 4" in panel.tags)
        self.assertTrue("бла-бла-бла" in panel.tags)

    def testPageRemove(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot

        panel = FakeTagsPanel()
        TagsPanelController(panel, application)

        self.wikiroot["Страница 2"].remove()

        self.assertTrue("тег 1" in panel.tags)
        self.assertTrue("тег 2" not in panel.tags)
        self.assertTrue("тег 3" not in panel.tags)
        self.assertTrue("тег 4" in panel.tags)

    def testPageCreate(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot

        panel = FakeTagsPanel()
        TagsPanelController(panel, application)

        TextPageFactory().create(self.wikiroot, "Страница 10", ["тег 10"])

        self.assertTrue("тег 10" in panel.tags)
        self.assertTrue("тег 1" in panel.tags)
        self.assertTrue("тег 2" in panel.tags)
        self.assertTrue("тег 3" in panel.tags)
        self.assertTrue("тег 4" in panel.tags)

    def testClear(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot

        panel = FakeTagsPanel()
        TagsPanelController(panel, application)

        self.assertTrue(len(panel.tags) > 0)

        application.wikiroot = None

        self.assertTrue(len(panel.tags) == 0)


class FakeTagsPanel(object):
    def __init__(self):
        self.tags = []
        self.marks = []

    def Bind(self, eventClass, eventFunc):
        pass

    def clearTags(self):
        self.tags = []

    def setTags(self, tagsList):
        # tagsList должен быть экземпляром класса outwiker.core.tagslist.TagsList
        self.tags = tagsList.tags

    def clearMarks(self):
        self.marks = []

    def mark(self, tag, marked=True):
        if marked:
            self.__setMark(tag)
        else:
            self.__removeMark(tag)

    def __setMark(self, tag):
        self.marks.append(tag)

    def __removeMark(self, tag):
        self.marks.remove(tag)
