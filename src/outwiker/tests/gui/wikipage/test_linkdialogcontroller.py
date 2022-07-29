# -*- coding: utf-8 -*-

import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.commands import copyTextToClipboard
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

    def testEmpty_wiki(self):
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

    def testSelectedHttpLink_wiki(self):
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

    def testSelectedPageLink_wiki(self):
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

    def testSelectedHttpsLink_wiki(self):
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

    def testSelectedftpLink_wiki(self):
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

    def testSelectedHttpLink2_wiki(self):
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

    def testSelectedText_wiki(self):
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

    def testClipboardHttpLink_wiki(self):
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

    def testClipboardHttpLink2_wiki(self):
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

    def testClipboardHttpsLink_wiki(self):
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

    def testClipboardFtpLink_wiki(self):
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

    def testClipboardPageLink_wiki(self):
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

    def testClipboardExitedPageLink_wiki(self):
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

    def testClipboardExitedPageAliasLink_wiki(self):
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

    def testClipboardAnchor_wiki(self):
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

    def testAttach_wiki(self):
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

    def testSelectedAttach_wiki(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'Attach:add.png'

        controller = WikiLinkDialogController(self.application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn('accept.png', parent.linkText.GetItems())
        self.assertIn('add.png', parent.linkText.GetItems())
        self.assertIn('html.txt', parent.linkText.GetItems())

        self.assertEqual(controller.link, 'Attach:add.png')
        self.assertEqual(controller.comment, 'Attach:add.png')
        self.assertEqual(controller.linkResult, '[[Attach:add.png]]')

        self.assertEqual(parent.linkText.GetValue(), 'add.png')

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
