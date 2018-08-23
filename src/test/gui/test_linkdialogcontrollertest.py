# -*- coding: utf-8 -*-

import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.commands import copyTextToClipboard
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.gui.dialogs.linkdialog import LinkDialog
from outwiker.gui.tester import Tester
from outwiker.pages.html.htmllinkdialogcontroller import HtmlLinkDialogController
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.wikilinkdialogcontroller import WikiLinkDialogController
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class LinkDialogControllerTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        copyTextToClipboard('')
        self._config = WikiConfig(self.application.config)
        self._config.linkStyleOptions.value = 0

        self.files = ['../test/samplefiles/accept.png',
                      '../test/samplefiles/add.png',
                      '../test/samplefiles/html.txt',
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

        self.assertIn('Attach:accept.png', parent.linkText.GetItems())
        self.assertIn('Attach:add.png', parent.linkText.GetItems())
        self.assertIn('Attach:html.txt', parent.linkText.GetItems())

    def testAttach_html(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = ''

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn('{}/accept.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn('{}/add.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn('{}/html.txt'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())

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

        self.assertIn('Attach:accept.png', parent.linkText.GetItems())
        self.assertIn('Attach:add.png', parent.linkText.GetItems())
        self.assertIn('Attach:html.txt', parent.linkText.GetItems())

        self.assertEqual(controller.link, 'Attach:add.png')
        self.assertEqual(controller.comment, 'Attach:add.png')
        self.assertEqual(controller.linkResult, '[[Attach:add.png]]')

        self.assertEqual(parent.linkText.GetValue(), 'Attach:add.png')

    def testSelectedAttach_html(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.mainWindow)
        Tester.dialogTester.appendOk()
        selectedString = '{}/add.png'.format(PAGE_ATTACH_DIR)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn('{}/accept.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn('{}/add.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn('{}/html.txt'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())

        self.assertEqual(controller.link,
                         '{}/add.png'.format(PAGE_ATTACH_DIR))
        self.assertEqual(controller.comment,
                         '{}/add.png'.format(PAGE_ATTACH_DIR))
        self.assertEqual(controller.linkResult,
                         '<a href="{attach}/add.png">{attach}/add.png</a>'.format(attach=PAGE_ATTACH_DIR))

        self.assertEqual(parent.linkText.GetValue(),
                         '{}/add.png'.format(PAGE_ATTACH_DIR))

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
