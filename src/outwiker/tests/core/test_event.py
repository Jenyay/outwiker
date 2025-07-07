# -*- coding: utf-8 -*-

"""
Тесты обработки событий
"""

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree, loadNotesTree
from outwiker.core.event import Event, CustomEvents
from outwiker.core.application import Application
from outwiker.core.events import (PAGE_UPDATE_CONTENT,
                                  PAGE_UPDATE_TAGS,
                                  PAGE_UPDATE_ICON)
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


class EventTest(unittest.TestCase):
    def setUp(self):
        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
        self.value4 = 0

    def event1(self):
        self.value1 = 1

    def event2(self, param):
        self.value2 = 2

    def event3(self, param):
        self.value3 = 3

    def event4(self, param):
        self.value4 += 1

    def eventAdd_1(self, param):
        param.append(1)

    def eventAdd_2(self, param):
        param.append(2)

    def eventAdd_3(self, param):
        param.append(3)

    def testAdd1(self):
        event = Event()
        event += self.event1

        event()

        self.assertEqual(self.value1, 1)
        self.assertEqual(self.value2, 0)

    def testAdd2(self):
        event = Event()
        event += self.event2

        event(111)

        self.assertEqual(self.value1, 0)
        self.assertEqual(self.value2, 2)

    def testAdd3(self):
        event = Event()
        event += self.event2
        event += self.event3

        event(111)

        self.assertEqual(self.value2, 2)
        self.assertEqual(self.value3, 3)

    def testAdd4(self):
        event = Event()
        event += self.event4
        event += self.event4

        event(111)

        self.assertEqual(self.value4, 1)

        event -= self.event4
        event -= self.event4
        event -= self.event4

    def testRemove1(self):
        event = Event()
        event += self.event1
        event -= self.event1

        event()

        self.assertEqual(self.value1, 0)

    def testRemove2(self):
        event = Event()
        event += self.event2
        event += self.event3
        event -= self.event2

        event(111)

        self.assertEqual(self.value2, 0)
        self.assertEqual(self.value3, 3)

    def testRemove3(self):
        event = Event()
        event -= self.event1

    def testClear1(self):
        event = Event()
        self.assertEqual(len(event), 0)

        event.clear()
        self.assertEqual(len(event), 0)

    def testClear2(self):
        event = Event()
        event += self.event1
        event += self.event2

        event.clear()
        self.assertEqual(len(event), 0)

        event(111)

        self.assertEqual(self.value1, 0)
        self.assertEqual(self.value2, 0)

    def testPriority_01(self):
        items = []
        event = Event()
        event.bind(self.eventAdd_1, 0)
        event(items)

        self.assertEqual(items, [1])

    def testPriority_02(self):
        items = []
        event = Event()
        event.bind(self.eventAdd_1, 0)
        event.bind(self.eventAdd_2, 0)
        event(items)

        self.assertEqual(items, [1, 2])

    def testPriority_03(self):
        items = []
        event = Event()
        event.bind(self.eventAdd_1, 0)
        event.bind(self.eventAdd_2, 0)
        event.bind(self.eventAdd_3, 0)
        event(items)

        self.assertEqual(items, [1, 2, 3])

    def testPriority_04(self):
        items = []
        event = Event()
        event.bind(self.eventAdd_1, 1)
        event.bind(self.eventAdd_2, 0)
        event(items)

        self.assertEqual(items, [1, 2])

    def testPriority_05(self):
        items = []
        event = Event()
        event.bind(self.eventAdd_1, 0)
        event.bind(self.eventAdd_2, 1)
        event(items)

        self.assertEqual(items, [2, 1])

    def testPriority_06(self):
        items = []
        event = Event()
        event.bind(self.eventAdd_1, 10)
        event.bind(self.eventAdd_2, 10)
        event.bind(self.eventAdd_3, 1)
        event(items)

        self.assertEqual(items, [1, 2, 3])

    def testPriority_07(self):
        items = []
        event = Event()
        event.bind(self.eventAdd_1, 10)
        event.bind(self.eventAdd_2, 10)
        event.bind(self.eventAdd_3, 20)
        event(items)

        self.assertEqual(items, [3, 1, 2])

    def testCustomEvent_01(self):
        cevent = CustomEvents()
        cevent.bind('event4', self.event4)

        cevent('event4', None)
        self.assertEqual(self.value4, 1)

        cevent('event4', None)
        self.assertEqual(self.value4, 2)

        cevent.unbind('event4', self.event4)

        cevent('event4', None)
        self.assertEqual(self.value4, 2)

    def testCustomEvent_02(self):
        cevent = CustomEvents()
        cevent.bind('event4', self.event4)

        cevent('event4', None)
        self.assertEqual(self.value4, 1)

        cevent('event4', None)
        self.assertEqual(self.value4, 2)

        cevent.clear('event4')

        cevent('event4', None)
        self.assertEqual(self.value4, 2)

    def testCustomEvent_03(self):
        cevent = CustomEvents()
        param = []
        cevent.bind('eventAdd1', self.eventAdd_1)
        cevent('eventAdd1', param)

        self.assertEqual(param, [1])
        cevent.clear('eventAdd1')

    def testCustomEvent_04(self):
        cevent = CustomEvents()
        cevent('unknown', None)


class EventsTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        self._application.wikiroot = None
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.isPageUpdate = False
        self.isPageCreate = False
        self.isTreeUpdate = False
        self.isPageSelect = False

        self.pageUpdateSender = None
        self.pageCreateSender = None
        self.treeUpdateSender = None
        self.pageSelectSender = None

        self.pageUpdateCount = 0
        self.pageCreateCount = 0
        self.treeUpdateCount = 0
        self.pageSelectCount = 0
        self.pageAttachChangeSubdirCount = 0

        self.prev_kwargs = None

        self._application.wikiroot = None

    def tearDown(self):
        self._application.wikiroot = None
        self._application.onAttachSubdirChanged -= self.pageAttachChangeSubdir
        self._application.onTreeUpdate -= self._onTreeUpdate
        self._application.onPageCreate -= self._onPageCreate
        self._application.onPageSelect -= self._onPageSelect
        self._application.onPageUpdate -= self._onPageUpdate
        removeDir(self.path)

    def _onPageUpdate(self, sender, **kwargs):
        self.isPageUpdate = True
        self.pageUpdateSender = sender
        self.pageUpdateCount += 1
        self.prev_kwargs = kwargs

    def _onPageCreate(self, sender):
        self.isPageCreate = True
        self.pageCreateSender = sender
        self.pageCreateCount += 1

    def _onTreeUpdate(self, sender):
        self.isTreeUpdate = True
        self.treeUpdateSender = sender
        self.treeUpdateCount += 1

    def _onPageSelect(self, sender):
        self.isPageSelect = True
        self.pageSelectSender = sender
        self.pageSelectCount += 1

    def pageAttachChangeSubdir(self, sender, params):
        self.pageAttachChangeSubdirCount += 1

    def testLoad_01(self):
        path = "testdata/samplewiki"
        self._application.onTreeUpdate += self._onTreeUpdate

        self.assertFalse(self.isTreeUpdate)
        loadNotesTree(path)

        self.assertFalse(self.isTreeUpdate)
        self.assertEqual(self.treeUpdateSender, None)
        self.assertEqual(self.treeUpdateCount, 0)

        self._application.onTreeUpdate -= self._onTreeUpdate

    def testCreateEvent(self):
        self._application.onTreeUpdate += self._onTreeUpdate
        self._application.onPageCreate += self._onPageCreate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertEqual(self.treeUpdateSender, None)

        self._application.wikiroot = rootwiki

        # Создаем страницу верхнего уровня(не считая корня)
        self.isPageCreate = False
        self.pageCreateSender = None

        TextPageFactory().create(rootwiki, "Страница 1", [])

        self.assertTrue(self.isPageCreate)
        self.assertEqual(self.pageCreateSender, rootwiki["Страница 1"])

        # Создаем еще одну страницу
        self.isPageCreate = False
        self.pageCreateSender = None

        TextPageFactory().create(rootwiki, "Страница 2", [])

        self.assertTrue(self.isPageCreate)
        self.assertEqual(self.pageCreateSender, rootwiki["Страница 2"])

        # Создаем подстраницу
        self.isPageCreate = False
        self.pageCreateSender = None

        TextPageFactory().create(rootwiki["Страница 2"], "Страница 3", [])

        self.assertTrue(self.isPageCreate)
        self.assertEqual(self.pageCreateSender,
                         rootwiki["Страница 2/Страница 3"])

        self._application.onTreeUpdate -= self._onTreeUpdate
        self._application.onPageCreate -= self._onPageCreate

    def testCreateNoEvent(self):
        self._application.onTreeUpdate += self._onTreeUpdate
        self._application.onPageCreate += self._onPageCreate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertEqual(self.treeUpdateSender, None)

        # Создаем страницу верхнего уровня(не считая корня)
        self.isPageCreate = False
        self.pageCreateSender = None

        TextPageFactory().create(rootwiki, "Страница 1", [])

        self.assertFalse(self.isPageCreate)
        self.assertEqual(self.pageCreateSender, None)

    def testUpdateContentEvent(self):
        """
        Тест на срабатывание событий при обновлении контента
        """
        self._application.onPageUpdate += self._onPageUpdate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])

        self._application.wikiroot = rootwiki

        # Изменим содержимое страницы
        rootwiki["Страница 1"].content = "1111"

        self.assertTrue(self.isPageUpdate)
        self.assertEqual(self.pageUpdateSender, rootwiki["Страница 1"])
        self.assertEqual(self.prev_kwargs["change"], PAGE_UPDATE_CONTENT)

        self._application.onPageUpdate -= self._onPageUpdate
        self._application.wikiroot = None

    def testUpdateContentNoEvent(self):
        """
        Тест на НЕсрабатывание событий при обновлении контента
        """
        self._application.onPageUpdate += self._onPageUpdate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])

        # Изменим содержимое страницы
        rootwiki["Страница 1"].content = "1111"

        self.assertFalse(self.isPageUpdate)
        self.assertEqual(self.pageUpdateSender, None)

        self._application.onPageUpdate -= self._onPageUpdate

    def testUpdateTagsEvent(self):
        """
        Тест на срабатывание событий при обновлении меток (тегов)
        """
        self._application.onPageUpdate += self._onPageUpdate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])

        self._application.wikiroot = rootwiki

        # Изменим содержимое страницы
        rootwiki["Страница 1"].tags = ["test"]

        self.assertTrue(self.isPageUpdate)
        self.assertEqual(self.pageUpdateSender, rootwiki["Страница 1"])
        self.assertEqual(self.prev_kwargs["change"], PAGE_UPDATE_TAGS)

        self._application.onPageUpdate -= self._onPageUpdate

    def testUpdateTagsNoEvent(self):
        """
        Тест на срабатывание событий при обновлении меток (тегов)
        """
        self._application.onPageUpdate += self._onPageUpdate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])

        # Изменим содержимое страницы
        rootwiki["Страница 1"].tags = ["test"]

        self.assertFalse(self.isPageUpdate)
        self.assertEqual(self.pageUpdateSender, None)

        self._application.onPageUpdate -= self._onPageUpdate

    def testUpdateIcon(self):
        """
        Тест на срабатывание событий при обновлении иконки
        """
        self._application.onPageUpdate += self._onPageUpdate
        self._application.onTreeUpdate += self._onTreeUpdate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])

        self._application.wikiroot = rootwiki

        # Изменим содержимое страницы
        rootwiki["Страница 1"].icon = "testdata/images/feed.gif"

        self.assertTrue(self.isPageUpdate)
        self.assertEqual(self.pageUpdateSender, rootwiki["Страница 1"])
        self.assertEqual(self.prev_kwargs["change"], PAGE_UPDATE_ICON)

        self.assertFalse(self.isTreeUpdate)

        self._application.onPageUpdate -= self._onPageUpdate
        self._application.onTreeUpdate -= self._onTreeUpdate

    def testUpdateIconNoEvent(self):
        """
        Тест на НЕсрабатывание событий при обновлении иконки,
        если не устанолен self._application.wikiroot
        """
        self._application.wikiroot = None

        self._application.onPageUpdate += self._onPageUpdate
        self._application.onTreeUpdate += self._onTreeUpdate

        removeDir(self.path)

        self.assertFalse(self.isTreeUpdate)
        self.assertFalse(self.isPageUpdate)
        self.assertFalse(self.isPageCreate)

        # Создаем вики
        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])

        self._application.wikiroot = rootwiki

        # Изменим содержимое страницы
        rootwiki["Страница 1"].icon = "testdata/images/feed.gif"

        self.assertTrue(self.isPageUpdate)
        self.assertEqual(self.pageUpdateSender, rootwiki["Страница 1"])

        self.assertFalse(self.isTreeUpdate)

        self._application.onPageUpdate -= self._onPageUpdate
        self._application.onTreeUpdate -= self._onTreeUpdate

    def testPageSelectCreate(self):
        self._application.onPageSelect += self._onPageSelect

        removeDir(self.path)

        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])
        TextPageFactory().create(rootwiki, "Страница 2", [])
        TextPageFactory().create(rootwiki["Страница 2"], "Страница 3", [])

        self._application.wikiroot = rootwiki

        self.assertEqual(rootwiki.selectedPage, None)

        rootwiki.selectedPage = rootwiki["Страница 1"]

        self.assertEqual(rootwiki.selectedPage, rootwiki["Страница 1"])
        self.assertEqual(self.isPageSelect, True)
        self.assertEqual(self.pageSelectSender, rootwiki["Страница 1"])
        self.assertEqual(self.pageSelectCount, 1)

        rootwiki.selectedPage = rootwiki["Страница 2/Страница 3"]

        self.assertEqual(rootwiki.selectedPage,
                         rootwiki["Страница 2/Страница 3"])
        self.assertEqual(self.isPageSelect, True)
        self.assertEqual(self.pageSelectSender,
                         rootwiki["Страница 2/Страница 3"])
        self.assertEqual(self.pageSelectCount, 2)

        self._application.onPageSelect -= self._onPageSelect

    def testPageSelectCreateNoEvent(self):
        self._application.onPageSelect += self._onPageSelect

        removeDir(self.path)

        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])
        TextPageFactory().create(rootwiki, "Страница 2", [])
        TextPageFactory().create(rootwiki["Страница 2"], "Страница 3", [])

        self._application.wikiroot = rootwiki

        self.assertEqual(rootwiki.selectedPage, None)

        rootwiki.selectedPage = rootwiki["Страница 1"]

        self.assertEqual(rootwiki.selectedPage, rootwiki["Страница 1"])
        self.assertEqual(self.isPageSelect, True)

    def testPageSelectLoad(self):
        self._application.onPageSelect += self._onPageSelect

        removeDir(self.path)

        rootwiki = createNotesTree(self.path)
        TextPageFactory().create(rootwiki, "Страница 1", [])
        TextPageFactory().create(rootwiki, "Страница 2", [])
        TextPageFactory().create(rootwiki["Страница 2"], "Страница 3", [])

        document = loadNotesTree(self.path)
        self._application.wikiroot = document

        self.assertEqual(document.selectedPage, None)

        document.selectedPage = document["Страница 1"]

        self.assertEqual(document.selectedPage, document["Страница 1"])
        self.assertEqual(self.isPageSelect, True)
        self.assertEqual(self.pageSelectSender, document["Страница 1"])
        self.assertEqual(self.pageSelectCount, 1)

        document.selectedPage = document["Страница 2/Страница 3"]

        self.assertEqual(document.selectedPage,
                         document["Страница 2/Страница 3"])
        self.assertEqual(self.isPageSelect, True)
        self.assertEqual(self.pageSelectSender,
                         document["Страница 2/Страница 3"])
        self.assertEqual(self.pageSelectCount, 2)

        self._application.onPageSelect -= self._onPageSelect

    def testChangeAttachSubdir(self):
        self._application.onAttachSubdirChanged += self.pageAttachChangeSubdir
        removeDir(self.path)

        rootwiki = createNotesTree(self.path)
        page = TextPageFactory().create(rootwiki, "Страница 1", [])
        self._application.wikiroot = rootwiki

        page.currentAttachSubdir = 'xxx'

        self.assertEqual(self.pageAttachChangeSubdirCount, 1)

        self._application.onAttachSubdirChanged -= self.pageAttachChangeSubdir
