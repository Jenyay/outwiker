# -*- coding: utf-8 -*-

import os.path
from tempfile import mkdtemp
import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.commands import renameAttach
from outwiker.core.tree import WikiDocument
from outwiker.gui.tester import Tester, getButtonId
from outwiker.gui.dialogs.overwritedialog import OverwriteDialog
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class AttachRenameTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Tests for attachment rename
    """

    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, 'Страница 1', [])
        factory.create(self.wikiroot, 'Страница 2', [])
        factory.create(self.wikiroot['Страница 2'], 'Страница 3', [])

        self.page = self.wikiroot['Страница 2/Страница 3']

        filesPath = 'testdata/samplefiles/'
        self.files = ['accept.png', 'add.png']
        self.fullFilesPath = [os.path.join(
            filesPath, fname) for fname in self.files]

        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.application.wikiroot = self.wikiroot
        self.application.wikiroot.selectedPage = self.page

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testRenameOk(self):
        window = self.mainWindow
        page = self.page
        fname_src = 'accept.png'
        fname_new = 'accept_renamed.png'

        renameAttach(window, page, fname_src, fname_new)
        attach = Attachment(self.page)
        self.assertNotIn(fname_src, attach.getAttachRelative())
        self.assertIn(fname_new, attach.getAttachRelative())

    def testRenameSelf(self):
        window = self.mainWindow
        page = self.page
        fname = 'accept.png'

        renameAttach(window, page, fname, fname)
        attach = Attachment(self.page)
        self.assertIn(fname, attach.getAttachRelative())

    def testRenameCancelId(self):
        window = self.mainWindow
        page = self.page
        fname_src = 'accept.png'
        fname_new = 'add.png'

        Tester.dialogTester.appendCancel()

        renameAttach(window, page, fname_src, fname_new)
        attach = Attachment(self.page)
        self.assertIn(fname_src, attach.getAttachRelative())
        self.assertIn(fname_new, attach.getAttachRelative())

    def testRenameCancelButton(self):
        window = self.mainWindow
        page = self.page
        fname_src = 'accept.png'
        fname_new = 'add.png'

        Tester.dialogTester.append(getButtonId, "cancel")

        renameAttach(window, page, fname_src, fname_new)
        attach = Attachment(self.page)
        self.assertIn(fname_src, attach.getAttachRelative())
        self.assertIn(fname_new, attach.getAttachRelative())

    def testRenameOverwrite(self):
        window = self.mainWindow
        page = self.page
        fname_src = 'accept.png'
        fname_new = 'add.png'

        Tester.dialogTester.append(getButtonId, "overwrite")

        renameAttach(window, page, fname_src, fname_new)
        attach = Attachment(self.page)
        attach_list = attach.getAttachRelative()
        self.assertNotIn(fname_src, attach_list)
        self.assertIn(fname_new, attach_list)
        self.assertEqual(1, len(attach_list))
