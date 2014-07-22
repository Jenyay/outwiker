# -*- coding: UTF-8 -*-

import unittest
import datetime
import time

from outwiker.core.tree import WikiDocument
from outwiker.core.config import PageConfig
from outwiker.core.style import Style
from outwiker.core.attachment import Attachment
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from test.utils import removeWiki


class PageDateTimeTest (unittest.TestCase):
    def setUp (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        # Максимальная погрешность при расчете времени
        self._maxDelta = datetime.timedelta (seconds=5)

        self.rootwiki = WikiDocument.create (self.path)


    def tearDown(self):
        removeWiki (self.path)


    def testDeleteDate (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].params.remove_option (PageConfig.sectionName, PageConfig.datetimeParamName)
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, None)


    def testCreateDate_01 (self):
        now = datetime.datetime.now()
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])

        self.assertNotEqual (self.rootwiki[u"Страница 1"].datetime, None)
        self.assertNotEqual (self.rootwiki[u"Страница 1"].creationdatetime, None)

        delta = now - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)

        delta = now - self.rootwiki[u"Страница 1"].creationdatetime
        self.assertLess (delta, self._maxDelta)


    def testCreateDate_02 (self):
        page = TextPageFactory().create (self.rootwiki, u"Страница 1", [])

        time.sleep (0.1)
        page.content = u"Абырвалг"

        self.assertNotEqual (page.datetime, page.creationdatetime)


    def testCreateDate_03 (self):
        page = TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        creationDateTime = page.creationdatetime

        time.sleep (0.1)

        newwiki = WikiDocument.load (self.path, False)
        self.assertEqual (creationDateTime, newwiki[u"Страница 1"].creationdatetime)


    def testCreateDate_04 (self):
        page = TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        creationDateTime = page.creationdatetime

        time.sleep (0.1)

        newwiki = WikiDocument.load (self.path, False)
        newwiki[u"Страница 1"].content = u"Абырвалг"

        self.assertEqual (creationDateTime, newwiki[u"Страница 1"].creationdatetime)


    def testCreateDate_05 (self):
        page = TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        creationDateTime = page.creationdatetime

        time.sleep (0.1)
        page.content = u"111"

        newwiki = WikiDocument.load (self.path, False)
        newwiki[u"Страница 1"].content = u"Абырвалг"

        self.assertEqual (creationDateTime, newwiki[u"Страница 1"].creationdatetime)


    def testSetDate (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        newdate = datetime.datetime (2012, 8, 24)
        self.rootwiki[u"Страница 1"].datetime = newdate

        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)


    def testChangeContent (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        newdate = datetime.datetime (2012, 8, 24)
        self.rootwiki[u"Страница 1"].datetime = newdate

        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        self.rootwiki[u"Страница 1"].content = u"бла-бла-бла"

        delta = datetime.datetime.now() - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)


    def testLoadWiki (self):
        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        newdate = datetime.datetime (2012, 8, 24)
        self.rootwiki[u"Страница 1"].datetime = newdate

        newroot = WikiDocument.load (self.path)
        self.assertEqual (newroot[u"Страница 1"].datetime, newdate)


    def testOldContent (self):
        newdate = datetime.datetime (2012, 8, 24)
        newcontent = u"Бла-бла-бла"
        newcontent2 = u"Бла-бла-бла-бла-бла"
        now = datetime.datetime.now()

        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].content = newcontent
        self.rootwiki[u"Страница 1"].datetime = newdate

        self.rootwiki[u"Страница 1"].content = newcontent
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        self.rootwiki[u"Страница 1"].content = newcontent2

        delta = now - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)


    def testsavePage (self):
        newdate = datetime.datetime (2012, 8, 24)

        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].content = u"Бла-бла-бла"
        self.rootwiki[u"Страница 1"].datetime = newdate

        self.rootwiki[u"Страница 1"].save()
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)


    def testChangeOrder (self):
        newdate = datetime.datetime (2012, 8, 24)

        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].content = u"Бла-бла-бла"

        self.rootwiki[u"Страница 1"].datetime = newdate

        TextPageFactory().create (self.rootwiki, u"Страница 2", [])
        self.rootwiki[u"Страница 2"].content = u"Бла-бла"

        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        self.rootwiki[u"Страница 1"].order += 1
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)


    def testChangeIcon (self):
        newdate = datetime.datetime (2012, 8, 24)

        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].datetime = newdate

        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        self.rootwiki[u"Страница 1"].icon = "../test/images/feed.gif"

        delta = datetime.datetime.now() - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)


    def testChangeTags(self):
        newdate = datetime.datetime (2012, 8, 24)

        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].datetime = newdate

        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        # Установим новые теги
        self.rootwiki[u"Страница 1"].tags = [u"тег 1", u"тег 2", u"тег 3"]
        delta = datetime.datetime.now() - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)

        # Изменим теги на те же самые
        self.rootwiki[u"Страница 1"].datetime = newdate
        self.rootwiki[u"Страница 1"].tags = [u"тег 3", u"тег 1", u"тег 2"]
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        # Удалим теги
        self.rootwiki[u"Страница 1"].tags = []
        delta = datetime.datetime.now() - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)


    def testChangeStyle (self):
        exampleStyleDir = u"../test/styles/example_jblog/example_jblog"
        newdate = datetime.datetime (2012, 8, 24)

        HtmlPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].datetime = newdate

        style = Style()
        style.setPageStyle (self.rootwiki[u"Страница 1"], exampleStyleDir)

        delta = datetime.datetime.now() - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)


    def testChild (self):
        """
        Проверка на то, что добавление дочерней страницы не изменяет дату модификации
        """
        newdate = datetime.datetime (2012, 8, 24)
        newcontent = u"Бла-бла-бла"

        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].content = newcontent
        self.rootwiki[u"Страница 1"].datetime = newdate
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        TextPageFactory().create (self.rootwiki[u"Страница 1"], u"Страница 2", [])
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        self.rootwiki[u"Страница 1/Страница 2"].content = u"Бла-бла"
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)


    def testAttachment (self):
        newdate = datetime.datetime (2012, 8, 24)
        newcontent = u"Бла-бла-бла"

        TextPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.rootwiki[u"Страница 1"].content = newcontent
        self.rootwiki[u"Страница 1"].datetime = newdate
        self.assertEqual (self.rootwiki[u"Страница 1"].datetime, newdate)

        # Прикрепили файл - должна измениться дата страницы
        Attachment (self.rootwiki[u"Страница 1"]).attach ([u"../test/samplefiles/first.jpg"])
        delta = datetime.datetime.now() - self.rootwiki[u"Страница 1"].datetime
        self.assertLess (delta, self._maxDelta)

        self.rootwiki[u"Страница 1"].datetime = newdate

        # Удалили файл - должна измениться дата страницы
        Attachment (self.rootwiki[u"Страница 1"]).removeAttach ([u"first.jpg"])
        delta = datetime.datetime.now() - self.rootwiki[u"Страница 1"].datetime
