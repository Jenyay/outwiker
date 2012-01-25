#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from test.utils import removeWiki
from outwiker.core.tree import WikiDocument
from outwiker.core.application import ApplicationParams
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tagspanelcontroller import TagsPanelController


class TagsPanelTest (unittest.TestCase):
    def setUp (self):
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        TextPageFactory.create (self.wikiroot, u"Страница 1", [u"тег 1"])
        TextPageFactory.create (self.wikiroot, u"Страница 2", [u"тег 1", u"тег 2"])
        TextPageFactory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [u"тег 3"])
        TextPageFactory.create (self.wikiroot[u"Страница 2/Страница 3"], u"Страница 4", [])
        TextPageFactory.create (self.wikiroot[u"Страница 1"], u"Страница 5", [u"тег 4", u"тег 1"])


    def tearDown (self):
        removeWiki (self.path)


    def testCreateTagsPanelController (self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()

        self.assertEqual (panel.tags, [])

        controller = TagsPanelController (panel, application)

        self.assertTrue (u"тег 1" in panel.tags)
        self.assertTrue (u"тег 2" in panel.tags)
        self.assertTrue (u"тег 3" in panel.tags)
        self.assertTrue (u"тег 4" in panel.tags)

        self.assertEqual (panel.marks, [])


    def testSelectPage1(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        controller = TagsPanelController (panel, application)

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 1"]
        self.assertTrue (u"тег 1" in panel.marks)

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]
        self.assertTrue (u"тег 3" in panel.marks)

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 1/Страница 5"]
        self.assertTrue (u"тег 1" in panel.marks)
        self.assertTrue (u"тег 4" in panel.marks)

        self.wikiroot.selectedPage = None
        self.assertEqual (panel.marks, [])


    def testSelectPage2(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        controller = TagsPanelController (panel, application)

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 1"]
        self.assertTrue (u"тег 1" in panel.marks)

        application.wikiroot = None
        self.assertEqual (panel.marks, [])


    def testTagsChange (self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        controller = TagsPanelController (panel, application)

        self.wikiroot.selectedPage = self.wikiroot[u"Страница 1"]
        self.assertTrue (u"тег 1" in panel.marks)

        self.wikiroot[u"Страница 1"].tags = [u"тег 1", u"тег 2", u"тег 666"]
        self.assertTrue (u"тег 1" in panel.marks)
        self.assertTrue (u"тег 2" in panel.marks)
        self.assertTrue (u"тег 666" in panel.marks)



    def testChangeTags (self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot
        panel = FakeTagsPanel()
        controller = TagsPanelController (panel, application)

        self.wikiroot[u"Страница 2"].tags = [u"бла-бла-бла"]

        self.assertTrue (u"тег 1" in panel.tags)
        self.assertTrue (u"тег 2" not in panel.tags)
        self.assertTrue (u"тег 3" in panel.tags)
        self.assertTrue (u"тег 4" in panel.tags)
        self.assertTrue (u"бла-бла-бла" in panel.tags)


    def testPageRemove (self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot

        panel = FakeTagsPanel()
        controller = TagsPanelController (panel, application)

        self.wikiroot[u"Страница 2"].remove()

        self.assertTrue (u"тег 1" in panel.tags)
        self.assertTrue (u"тег 2" not in panel.tags)
        self.assertTrue (u"тег 3" not in panel.tags)
        self.assertTrue (u"тег 4" in panel.tags)


    def testPageCreate (self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot

        panel = FakeTagsPanel()
        controller = TagsPanelController (panel, application)

        TextPageFactory.create (self.wikiroot, u"Страница 10", [u"тег 10"])

        self.assertTrue (u"тег 10" in panel.tags)
        self.assertTrue (u"тег 1" in panel.tags)
        self.assertTrue (u"тег 2" in panel.tags)
        self.assertTrue (u"тег 3" in panel.tags)
        self.assertTrue (u"тег 4" in panel.tags)


    def testClear(self):
        application = ApplicationParams()
        application.wikiroot = self.wikiroot

        panel = FakeTagsPanel()
        controller = TagsPanelController (panel, application)

        self.assertTrue (len (panel.tags) > 0)

        application.wikiroot = None

        self.assertTrue (len (panel.tags) == 0)



class FakeTagsPanel (object):
    def __init__ (self):
        self.tags = []
        self.marks = []


    def Bind (self, eventClass, eventFunc):
        pass


    def clearTags (self):
        self.tags = []


    def setTags (self, tagsList):
        # tagsList должен быть экземпляром класса outwiker.core.tagslist.TagsList
        self.tags = tagsList.tags


    def clearMarks(self):
        self.marks = []


    def mark (self, tag, marked=True):
        if marked:
            self.__setMark (tag)
        else:
            self.__removeMark (tag)


    def __setMark (self, tag):
        self.marks.append (tag)


    def __removeMark (self, tag):
        self.marks.remove (tag)
