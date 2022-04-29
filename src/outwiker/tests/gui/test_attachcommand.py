# -*- coding=utf-8 -*-

from pathlib import Path
from typing import List
import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.commands import attachFiles
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class AttachCommandTests(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.files_path = Path('testdata/samplefiles/')

        self.wikiroot = self.createWiki()
        factory = TextPageFactory()
        self.page = factory.create(self.wikiroot, 'Страница 1', [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.page

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _getFilesPath(self, files) -> List[str]:
        return [self.files_path / fname for fname in files]

    def testAttachSimple(self):
        files = ['image.png', 'add.png']
        files_full_path = self._getFilesPath(files)
        attachFiles(self.mainWindow, self.page, files_full_path)

        attach = Attachment(self.page)
        self.assertEqual(len(files), len(attach.getAttachFull()))

    def testAddAttaches(self):
        files_full_path_1 = self._getFilesPath(['image.png', 'add.png'])
        files_full_path_2 = self._getFilesPath(['accept.png'])
        attachFiles(self.mainWindow, self.page, files_full_path_1)
        attachFiles(self.mainWindow, self.page, files_full_path_2)

        attach = Attachment(self.page)
        self.assertEqual(len(files_full_path_1) + len(files_full_path_2),
                         len(attach.getAttachFull()))

    def testAttachDir(self):
        files_full_path = self._getFilesPath(['dir'])
        attachFiles(self.mainWindow, self.page, files_full_path)

        attach = Attachment(self.page)
        self.assertEqual(len(files_full_path), len(attach.getAttachFull()))

        attach_dir = Path(attach.getAttachPath())
        self.assertTrue((attach_dir / 'dir').is_dir())
        self.assertTrue((attach_dir / 'dir' / 'attach.png').exists())
        self.assertTrue((attach_dir / 'dir' / 'subdir').is_dir())
        self.assertTrue((attach_dir / 'dir' / 'subdir' / 'subdir2').is_dir())
        self.assertTrue((attach_dir / 'dir' / 'subdir' / 'subdir2' / 'image.png').exists())

    def testAttachSubdirRoot(self):
        files = ['image.png', 'add.png']
        files_full_path = self._getFilesPath(files)
        subdir = '.'
        attachFiles(self.mainWindow, self.page, files_full_path, subdir)

        attach = Attachment(self.page)
        self.assertEqual(len(files), len(attach.getAttachFull()))

    def testAttachSubDir(self):
        # Create __attach directory
        attach = Attachment(self.page)
        attach_dir = Path(attach.getAttachPath(create=True))

        # Create subdirectory
        subdir = 'dir'
        subdir_full = attach_dir / subdir
        subdir_full.mkdir()

        files_full_path = self._getFilesPath(['image.png', 'add.png'])
        attachFiles(self.mainWindow, self.page, files_full_path, subdir)

        self.assertTrue((subdir_full / 'image.png').exists())
        self.assertTrue((subdir_full / 'add.png').exists())

    def testAttachDirToSubDir(self):
        # Create __attach directory
        attach = Attachment(self.page)
        attach_dir = Path(attach.getAttachPath(create=True))

        # Create subdirectory
        subdir = 'dir'
        subdir_full = attach_dir / subdir
        subdir_full.mkdir()

        files_full_path = self._getFilesPath([Path('dir', 'subdir')])
        attachFiles(self.mainWindow, self.page, files_full_path, subdir)

        self.assertTrue((attach_dir / 'dir' / 'subdir').is_dir())
        self.assertTrue((attach_dir / 'dir' / 'subdir' / 'subdir2').is_dir())
        self.assertTrue((attach_dir / 'dir' / 'subdir' / 'subdir2' / 'image.png').exists())
