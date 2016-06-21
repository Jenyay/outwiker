# -*- coding: UTF-8 -*-

import unittest

from outwiker.pages.wiki.linkcreator import LinkCreator
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.core.application import Application


class WikiLinkCreatorTest(unittest.TestCase):
    def setUp(self):
        self.config = WikiConfig(Application.config)
        self.config.linkStyleOptions.value = 0

    def tearDown(self):
        self.config.linkStyleOptions.value = 0

    def testCreateStyle0(self):
        comment = u"Бла-бла-бла"
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Бла-бла-бла -> Ссылко бла-бла-бла]]")

    def testCreateStyle1(self):
        self.config.linkStyleOptions.value = 1
        comment = u"Бла-бла-бла"
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла | Бла-бла-бла]]")

    def testCreateStyleInvalid(self):
        self.config.linkStyleOptions.value = 100
        comment = u"Бла-бла-бла"
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Бла-бла-бла -> Ссылко бла-бла-бла]]")

    def testEmptyComment0(self):
        comment = u""
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testEmptyComment1(self):
        self.config.linkStyleOptions.value = 1
        comment = u""
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testLinkComment0(self):
        comment = u"Ссылко бла-бла-бла"
        link = comment

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testLinkComment1(self):
        self.config.linkStyleOptions.value = 1
        comment = u"Ссылко бла-бла-бла"
        link = comment

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testLinkCommentInvalid(self):
        self.config.linkStyleOptions.value = 100
        comment = u"Ссылко бла-бла-бла"
        link = comment

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testEmptyCommentStrip0(self):
        comment = u"  "
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testEmptyCommentStrip1(self):
        self.config.linkStyleOptions.value = 1
        comment = u"   "
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testLinkCommentStrip0(self):
        comment = u"   Ссылко бла-бла-бла     "
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")

    def testLinkCommentStrip1(self):
        self.config.linkStyleOptions.value = 1
        comment = u"   Ссылко бла-бла-бла     "
        link = u"Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, u"[[Ссылко бла-бла-бла]]")
