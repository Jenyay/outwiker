# -*- coding: utf-8 -*-

import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.commands import copyTextToClipboard
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.core.pageuiddepot import PageUidDepot
from outwiker.gui.dialogs.linkdialog import LinkDialog
from outwiker.gui.tester import Tester
from outwiker.pages.html.htmllinkdialogcontroller import HtmlLinkDialogController
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class LinkDialogControllerHtmlTest(unittest.TestCase, BaseOutWikerGUIMixin):
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

        factory = HtmlPageFactory()
        self._testpage = factory.create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)
        copyTextToClipboard('')

    def testEmpty_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)

        controller.showDialog()

        self.assertEqual(controller.link, '')
        self.assertEqual(controller.comment, '')
        self.assertEqual(controller.linkResult, '<a href=""></a>')

    def testSelectedHttpLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'https://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)

        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            '<a href="https://jenyay.net">https://jenyay.net</a>')

    def testSelectedPageLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'page://__adsfadfasdf'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            '<a href="page://__adsfadfasdf">page://__adsfadfasdf</a>')

    def testSelectedHttpsLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'https://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            '<a href="https://jenyay.net">https://jenyay.net</a>')

    def testSelectedftpLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'ftp://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            '<a href="ftp://jenyay.net">ftp://jenyay.net</a>')

    def testSelectedHttpLink2_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'HTTPS://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            '<a href="HTTPS://jenyay.net">HTTPS://jenyay.net</a>')

    def testSelectedText_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = 'бла-бла-бла'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, '')
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, '<a href="">бла-бла-бла</a>')

    def testClipboardHttpLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'https://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            '<a href="https://jenyay.net">https://jenyay.net</a>')

    def testClipboardHttpLink2_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'HTTPS://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            '<a href="HTTPS://jenyay.net">HTTPS://jenyay.net</a>')

    def testClipboardHttpsLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'https://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            '<a href="https://jenyay.net">https://jenyay.net</a>')

    def testClipboardFtpLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'ftp://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            '<a href="ftp://jenyay.net">ftp://jenyay.net</a>')

    def testClipboardPageLink_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'page://_asdfasdfasdf'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            '<a href="page://_asdfasdfasdf">page://_asdfasdfasdf</a>')

    def testClipboardExitedPageLink_html(self):
        page_uid = PageUidDepot().createUid(self._testpage)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'page://{uid}'.format(uid=page_uid)
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, self._testpage.display_title)
        self.assertEqual(
            controller.linkResult,
            '<a href="page://{uid}">{title}</a>'.format(uid=page_uid,
                                                        title=self._testpage.display_title))

    def testClipboardExitedWithAliasPageLink_html(self):
        self._testpage.alias = 'Tha page with an alias'
        page_uid = PageUidDepot().createUid(self._testpage)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = 'page://{uid}'.format(uid=page_uid)
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, self._testpage.display_title)
        self.assertEqual(
            controller.linkResult,
            '<a href="page://{uid}">{title}</a>'.format(uid=page_uid,
                                                        title=self._testpage.display_title))

    def testClipboardAnchor_html(self):
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''
        clipboardText = '#anchor'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            '<a href="#anchor">#anchor</a>')

    def testAttach_html(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn('accept.png', parent.linkText.GetItems())
        self.assertIn('add.png', parent.linkText.GetItems())
        self.assertIn('html.txt', parent.linkText.GetItems())

    def testSelectedAttach_html(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = '{}/add.png'.format(PAGE_ATTACH_DIR)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn('accept.png', parent.linkText.GetItems())
        self.assertIn('add.png', parent.linkText.GetItems())
        self.assertIn('html.txt', parent.linkText.GetItems())

        self.assertEqual(controller.link,
                         '{}/add.png'.format(PAGE_ATTACH_DIR))
        self.assertEqual(controller.comment,
                         '{}/add.png'.format(PAGE_ATTACH_DIR))
        self.assertEqual(controller.linkResult,
                         '<a href="{attach}/add.png">{attach}/add.png</a>'.format(attach=PAGE_ATTACH_DIR))

        self.assertEqual(parent.linkText.GetValue(), 'add.png')
