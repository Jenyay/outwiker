# -*- coding: utf-8 -*-

from unittest import TestCase

from outwiker.pages.wiki.linkcreator import LinkCreator
from outwiker.pages.wiki.wikiconfig import WikiConfig
from test.basetestcases import BaseOutWikerMixin


class WikiLinkCreatorTest(BaseOutWikerMixin, TestCase):
    def setUp(self):
        self.initApplication()
        self.config = WikiConfig(self.application.config)
        self.config.linkStyleOptions.value = 0

    def tearDown(self):
        self.destroyApplication()

    def testCreateStyle0(self):
        comment = "Бла-бла-бла"
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Бла-бла-бла -> Ссылко бла-бла-бла]]")

    def testCreateStyle1(self):
        self.config.linkStyleOptions.value = 1
        comment = "Бла-бла-бла"
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла | Бла-бла-бла]]")

    def testCreateStyleInvalid(self):
        self.config.linkStyleOptions.value = 100
        comment = "Бла-бла-бла"
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Бла-бла-бла -> Ссылко бла-бла-бла]]")

    def testEmptyComment0(self):
        comment = ""
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testEmptyComment1(self):
        self.config.linkStyleOptions.value = 1
        comment = ""
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testLinkComment0(self):
        comment = "Ссылко бла-бла-бла"
        link = comment

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testLinkComment1(self):
        self.config.linkStyleOptions.value = 1
        comment = "Ссылко бла-бла-бла"
        link = comment

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testLinkCommentInvalid(self):
        self.config.linkStyleOptions.value = 100
        comment = "Ссылко бла-бла-бла"
        link = comment

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testEmptyCommentStrip0(self):
        comment = "  "
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testEmptyCommentStrip1(self):
        self.config.linkStyleOptions.value = 1
        comment = "   "
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testLinkCommentStrip0(self):
        comment = "   Ссылко бла-бла-бла     "
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")

    def testLinkCommentStrip1(self):
        self.config.linkStyleOptions.value = 1
        comment = "   Ссылко бла-бла-бла     "
        link = "Ссылко бла-бла-бла"

        creator = LinkCreator(self.config)
        text = creator.create(link, comment)

        self.assertEqual(text, "[[Ссылко бла-бла-бла]]")
