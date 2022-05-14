# -*- coding=utf-8 -*-

import unittest
from pathlib import Path

import wx

from outwiker.core.attachment import Attachment
from outwiker.actions.attachcreatesubdir import AttachCreateSubdirAction
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class AttachCreateSubdirTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Tests for the AttachCreateSubdirAction action
    """

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.page = TextPageFactory().create(self.wikiroot, "page", [])

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.page

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _getAction(self):
        return self.application.actionController.getAction(AttachCreateSubdirAction.stringId)

    def testSingleRun(self):
        action = self._getAction()
        attach = Attachment(self.page)

        action.run(None)

        root = Path(attach.getAttachPath(create=False))
        new_subdir = root / action.default_subdir_name

        self.assertTrue(root.exists())
        self.assertTrue(new_subdir.exists())
        self.assertTrue(new_subdir.is_dir())

    def testSingleSubdirRun(self):
        subdir = 'subdir'
        action = self._getAction()
        attach = Attachment(self.page)
        attach.createSubdir(subdir)
        self.page.currentAttachSubdir = subdir

        action.run(None)

        root = Path(attach.getAttachPath(create=False))
        new_subdir = root / subdir / action.default_subdir_name

        self.assertTrue(new_subdir.exists())
        self.assertTrue(new_subdir.is_dir())

    def testRepeatRun(self):
        action = self._getAction()
        attach = Attachment(self.page)

        action.run(None)
        action.run(None)
        action.run(None)

        root = Path(attach.getAttachPath(create=False))
        new_subdir_1 = root / action.default_subdir_name
        new_subdir_2 = root / (action.default_subdir_name + ' (1)')
        new_subdir_3 = root / (action.default_subdir_name + ' (2)')

        self.assertTrue(root.exists())
        self.assertTrue(new_subdir_1.exists())
        self.assertTrue(new_subdir_1.is_dir())

        self.assertTrue(new_subdir_2.exists())
        self.assertTrue(new_subdir_2.is_dir())

        self.assertTrue(new_subdir_3.exists())
        self.assertTrue(new_subdir_3.is_dir())

    def testFileExists(self):
        # Attached file has same name as new subdir
        action = self._getAction()
        attach = Attachment(self.page)

        root = Path(attach.getAttachPath(create=True))
        fname = root / action.default_subdir_name
        with open(fname, 'w'):
            pass

        action.run(None)

        new_subdir = root / (action.default_subdir_name + ' (1)')

        self.assertTrue(new_subdir.exists())
        self.assertTrue(new_subdir.is_dir())
