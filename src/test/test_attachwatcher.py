# -*- coding: utf-8 -*-

import unittest
import os.path
from tempfile import mkdtemp

from outwiker.core.attachment import Attachment
from .utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.core.attachwatcher import AttachWatcher


class AttachWatcherTest(unittest.TestCase):
    def setUp(self):
        self._eventCount = 0
        self._application = Application
        self._application.onAttachListChanged += self._onAttachListChanged

        # Path to path with files
        self._sample_path = '../test/samplefiles'

        # Path to wiki
        self.path = mkdtemp(prefix='OutWiker AttachWatcherTest Тесты')
        self.wikiroot = WikiDocument.create(self.path)
        self.page_01 = TextPageFactory().create(self.wikiroot,
                                                "Страница 1",
                                                [])
        self.page_02 = TextPageFactory().create(self.wikiroot,
                                                "Страница 2",
                                                [])

    def tearDown(self):
        self._application.onAttachListChanged -= self._onAttachListChanged
        removeDir(self.path)

    def _onAttachListChanged(self, page, params):
        self._eventCount += 1

    def _attach_files(self, page, files_list):
        files_full = [os.path.join(self._sample_path, fname)
                      for fname
                      in files_list]

        attach = Attachment(page)
        attach.attach(files_full)

    def test_empty_01(self):
        '''
        Wiki is not added to Application
        '''
        watcher = AttachWatcher(self._application)
        watcher.initialize()
        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_02(self):
        '''
        Wiki added to Application _before_ AttachWatcher initializing.
        No selected pages.
        '''
        self._application.wikiroot = self.wikiroot

        watcher = AttachWatcher(self._application)
        watcher.initialize()
        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_03(self):
        '''
        Wiki added to Application _after_ AttachWatcher initializing.
        No selected pages.
        '''
        watcher = AttachWatcher(self._application)
        watcher.initialize()
        self._application.wikiroot = self.wikiroot
        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_04(self):
        '''
        Wiki added to Application _before_ AttachWatcher initializing.
        Selected page.
        '''
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()
        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_05(self):
        '''
        Wiki added to Application _after_ AttachWatcher initializing.
        Selected page.
        '''
        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_06(self):
        '''
        Change the selected page
        '''
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = None

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = self.page_01

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_07(self):
        '''
        Change the selected page
        '''
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = None

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_08(self):
        '''
        Change the selected page
        '''
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = self.page_02

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_09_close_wiki(self):
        '''
        Close current notes tree
        '''
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.wikiroot = None

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_empty_10_create_empty_attach_dir(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        Attachment(self._application.selectedPage).getAttachPath(True)

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_files_not_change_01(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_files_not_change_02(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = None

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = self.page_01

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_files_not_change_03(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = None

        self._attach_files(self.page_01, ['add.png'])
        self._attach_files(self.page_02, ['add.png', 'dir.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        # Switch pages
        self._application.selectedPage = self.page_01
        self._application.selectedPage = self.page_02

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_files_not_change_04(self):
        self._attach_files(self.page_01, ['add.png'])

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        # Close the wiki
        self._application.wikiroot = None

        watcher.clear()

        self.assertEqual(self._eventCount, 0)

    def test_add_files_01(self):

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._attach_files(self.page_01, ['add.png'])

        watcher.clear()

        self.assertEqual(self._eventCount, 1)

    def test_add_files_02(self):

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._attach_files(self.page_01, ['add.png', 'dir.png'])

        watcher.clear()

        self.assertEqual(self._eventCount, 1)

    def test_add_files_03(self):

        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._attach_files(self.page_01, ['add.png'])
        self._attach_files(self.page_01, ['dir.png'])

        watcher.clear()

        self.assertEqual(self._eventCount, 2)
