# -*- coding: utf-8 -*-

import unittest

from outwiker.api.services.clipboard import copyTextToClipboard
from outwiker.core.attachment import Attachment
from outwiker.core.pageuiddepot import PageUidDepot
from outwiker.gui.dialogs.linkdialog import LinkDialog
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.wikilinkdialogcontroller import WikiLinkDialogController
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class LinkDialogControllerWikiTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        copyTextToClipboard('')
        self._config = WikiConfig(self.application.config)
        self._config.linkStyleOptions.value = 0

        self.files = ['testdata/samplefiles/accept.png',
                      'testdata/samplefiles/add.png',
                      'testdata/samplefiles/html.txt',
                      ]

        factory = WikiPageFactory()
        self._testpage = factory.create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        copyTextToClipboard('')

    def testEmpty(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, '')
        self.assertEqual(controller.comment, '')
        self.assertEqual(controller.linkResult, '[[]]')

    def testSelectedHttpLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'https://jenyay.net'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, '[[https://jenyay.net]]')

    def testSelectedPageLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'page://__adsfadfasdf'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, '[[page://__adsfadfasdf]]')

    def testSelectedHttpsLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'https://jenyay.net'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, '[[https://jenyay.net]]')

    def testSelectedftpLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'ftp://jenyay.net'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, '[[ftp://jenyay.net]]')

    def testSelectedHttpLink2(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'HTTPS://jenyay.net'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, '[[HTTPS://jenyay.net]]')

    def testSelectedText(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'бла-бла-бла'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, '')
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, '[[бла-бла-бла -> ]]')

    def testClipboardHttpLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'https://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, '[[https://jenyay.net]]')

    def testClipboardHttpLink2(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'HTTPS://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, '[[HTTPS://jenyay.net]]')

    def testClipboardHttpsLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'https://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, '[[https://jenyay.net]]')

    def testClipboardFtpLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'ftp://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, '[[ftp://jenyay.net]]')

    def testClipboardPageLink(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'page://_asdfasdfasdf'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, '[[page://_asdfasdfasdf]]')

    def testClipboardExitedPageLink(self):
        page_uid = PageUidDepot().createUid(self._testpage)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'page://{uid}'.format(uid=page_uid)
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, self._testpage.display_title)
        self.assertEqual(controller.linkResult,
                         '[[{title} -> page://{uid}]]'.format(title=self._testpage.display_title,
                                                              uid=page_uid))

    def testClipboardExitedPageAliasLink(self):
        self._testpage.alias = 'A page with an alias'
        page_uid = PageUidDepot().createUid(self._testpage)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'page://{uid}'.format(uid=page_uid)
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, self._testpage.display_title)
        self.assertEqual(controller.linkResult,
                         '[[{title} -> page://{uid}]]'.format(title=self._testpage.display_title,
                                                              uid=page_uid))

    def testClipboardAnchor(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = '#anchor'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, '[[#anchor]]')

    def testAttach(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn('accept.png', parent.linkText.GetItems())
        self.assertIn('add.png', parent.linkText.GetItems())
        self.assertIn('html.txt', parent.linkText.GetItems())

    def testAttach_subdir(self):
        subdir = 'subdir 1/subdir 2'

        attach = Attachment(self._testpage)
        attach.createSubdir(subdir)

        attach.attach(self.files)
        attach.attach(self.files, subdir)

        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()
        dialog_files = [fname.replace('\\', '/')
                        for fname in parent.linkText.GetItems()]

        self.assertIn('subdir 1/subdir 2/accept.png', dialog_files)
        self.assertIn('subdir 1/subdir 2/add.png', dialog_files)
        self.assertIn('subdir 1/subdir 2/html.txt', dialog_files)
        self.assertIn('subdir 1/subdir 2/accept.png', dialog_files)
        self.assertIn('subdir 1/subdir 2/add.png', dialog_files)
        self.assertIn('subdir 1/subdir 2/html.txt', dialog_files)

    def testAttach_hidden_subdir(self):
        hidden_subdir = '__thumb'
        attach = Attachment(self._testpage)
        attach.attach(self.files)
        attach.createSubdir(hidden_subdir)

        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertNotIn(hidden_subdir, parent.linkText.GetItems())

    def testSelectedAttach(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'Attach:add.png'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, 'Attach:add.png')
        self.assertEqual(controller.comment, 'Attach:add.png')
        self.assertEqual(controller.linkResult, '[[Attach:add.png]]')

        self.assertEqual(parent.linkText.GetValue(), 'add.png')

    def testSelectedAttachSingleQuotes(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = "Attach:'add.png'"

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, "Attach:'add.png'")
        self.assertEqual(controller.comment, "Attach:'add.png'")
        self.assertEqual(controller.linkResult, "[[Attach:'add.png']]")

        self.assertEqual(parent.linkText.GetValue(), 'add.png')

    def testSelectedAttachDoubleQuotes(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'Attach:"add.png"'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, 'Attach:"add.png"')
        self.assertEqual(controller.comment, 'Attach:"add.png"')
        self.assertEqual(controller.linkResult, '[[Attach:"add.png"]]')

        self.assertEqual(parent.linkText.GetValue(), 'add.png')

    def testSelectedAttach_subdir_back_slash_sigle_quotes(self):
        subdir = 'subdir 1/subdir 2'

        attach = Attachment(self._testpage)
        attach.createSubdir(subdir)
        attach.attach(self.files, subdir)

        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = "Attach:'subdir 1\\subdir 2\\add.png'"

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link.replace('\\', '/'),
                        "Attach:'subdir 1/subdir 2/add.png'")

        self.assertEqual(controller.comment.replace('\\', '/'),
                         "Attach:'subdir 1/subdir 2/add.png'")

        self.assertEqual(controller.linkResult.replace('\\', '/'),
                         "[[Attach:'subdir 1/subdir 2/add.png']]")

        self.assertEqual(parent.linkText.GetValue().replace('\\', '/'),
                         'subdir 1/subdir 2/add.png')

    def testSelectedAttach_subdir_back_slash_double_quotes(self):
        subdir = 'subdir 1/subdir 2'

        attach = Attachment(self._testpage)
        attach.createSubdir(subdir)
        attach.attach(self.files, subdir)

        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'Attach:"subdir 1\\subdir 2\\add.png"'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link.replace('\\', '/'),
                        'Attach:"subdir 1/subdir 2/add.png"')

        self.assertEqual(controller.comment.replace('\\', '/'),
                         'Attach:"subdir 1/subdir 2/add.png"')

        self.assertEqual(controller.linkResult.replace('\\', '/'),
                         '[[Attach:"subdir 1/subdir 2/add.png"]]')

        self.assertEqual(parent.linkText.GetValue().replace('\\', '/'),
                         'subdir 1/subdir 2/add.png')

    def testSelectedAttach_subdir_forward_slash(self):
        subdir = 'subdir 1/subdir 2'

        attach = Attachment(self._testpage)
        attach.createSubdir(subdir)
        attach.attach(self.files, subdir)

        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'Attach:"subdir 1/subdir 2/add.png"'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link.replace('\\', '/'),
                         'Attach:"subdir 1/subdir 2/add.png"')

        self.assertEqual(controller.comment.replace('\\', '/'),
                         'Attach:"subdir 1/subdir 2/add.png"')

        self.assertEqual(controller.linkResult.replace('\\', '/'),
                         '[[Attach:"subdir 1/subdir 2/add.png"]]')

        self.assertEqual(parent.linkText.GetValue().replace('\\', '/'),
                         'subdir 1/subdir 2/add.png')

    def testLinkStyle_01(self):
        self._config.linkStyleOptions.value = 0

        dlg = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              dlg,
                                              selectedString)
        dlg.link = 'Ссылка'
        dlg.comment = 'Коммент'

        controller.showDialog()

        self.assertEqual(controller.linkResult, '[[Коммент -> Ссылка]]')

    def testLinkStyle_02(self):
        self._config.linkStyleOptions.value = 1

        dlg = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              dlg,
                                              selectedString)
        dlg.link = 'Ссылка'
        dlg.comment = 'Коммент'

        controller.showDialog()

        self.assertEqual(controller.linkResult, '[[Ссылка | Коммент]]')
