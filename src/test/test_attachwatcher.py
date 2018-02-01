# -*- coding: utf-8 -*-

import os
from tempfile import mkdtemp

from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.core.attachwatcher import AttachWatcher
from .utils import removeDir
from .basetestcases import BaseWxTestCase


class AttachWatcherTest(BaseWxTestCase):
    def setUp(self):
        super().setUp()
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
        super().tearDown()
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

        self.myYield()
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

        self.myYield()
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

        self.myYield()
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

        self.myYield()
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

        self.myYield()
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

        self.myYield()
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

        self.myYield()
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

        self.myYield()
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

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_empty_10_create_empty_attach_dir(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        Attachment(self._application.selectedPage).getAttachPath(True)

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_files_not_change_01(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_files_not_change_02(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = None

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = self.page_01

        self.myYield()
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

        self.myYield()
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

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_add_files_01(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._attach_files(self.page_01, ['add.png'])

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 1)

    def test_add_files_02(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._attach_files(self.page_01, ['add.png', 'dir.png'])

        self.myYield()
        watcher.clear()

        self.assertEqual(self._eventCount, 1)

    def test_add_files_03(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._attach_files(self.page_01, ['add.png'])
        self.myYield()

        self._attach_files(self.page_01, ['dir.png'])
        self.myYield()

        watcher.clear()

        self.assertEqual(self._eventCount, 2)

    def test_attach_touch_read(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01
        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        attach = Attachment(self.page_01)
        with open(attach.getFullPath('add.png')):
            pass

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_attach_touch_write(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01
        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        attach = Attachment(self.page_01)
        with open(attach.getFullPath('add.png'), 'w'):
            pass

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_attach_rename(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01
        self._attach_files(self.page_01, ['add.png'])

        attach = Attachment(self.page_01)
        src_fname = attach.getFullPath('add.png')
        dest_fname = attach.getFullPath('newname.png')

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        os.rename(src_fname, dest_fname)

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 1)

    def test_attach_delete(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01
        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        attach = Attachment(self.page_01)
        attach.removeAttach(['add.png'])

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 1)

    def test_switch_and_add_file(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        self._attach_files(self.page_01, ['add.png'])
        self._attach_files(self.page_02, ['add.png', 'dir.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        # Switch pages
        self._application.selectedPage = self.page_02
        self._attach_files(self.page_02, ['accept.png'])

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 1)

    def test_close_wiki(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.wikiroot = None
        self._attach_files(self.page_01, ['dir.png'])

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_unselect_page(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = None
        self._attach_files(self.page_01, ['dir.png'])

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_select_again(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = None
        self._attach_files(self.page_01, ['dir.png'])
        self._application.selectedPage = self.page_01

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_select_again_and_add(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self._application.selectedPage = None
        self._attach_files(self.page_01, ['dir.png'])
        self._application.selectedPage = self.page_01
        self._attach_files(self.page_01, ['accept.png'])

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 1)

    def test_rename_page_01(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self.page_01.title = 'Новый заголовок'

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_rename_page_02(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01
        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self.page_01.title = 'Новый заголовок'

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 0)

    def test_rename_page_03(self):
        self._application.wikiroot = self.wikiroot
        self._application.selectedPage = self.page_01
        self._attach_files(self.page_01, ['add.png'])

        watcher = AttachWatcher(self._application)
        watcher.initialize()

        self.page_01.title = 'Новый заголовок'
        self._attach_files(self.page_01, ['dir.png'])

        self.myYield()
        watcher.clear()
        self.assertEqual(self._eventCount, 1)
