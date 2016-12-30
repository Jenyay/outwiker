# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest

from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.commands import copyTextToClipboard
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.gui.dialogs.linkdialog import LinkDialog
from outwiker.gui.tester import Tester
from outwiker.pages.html.htmllinkdialogcontroller import HtmlLinkDialogController
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.wikilinkdialogcontroller import WikiLinkDialogController
from outwiker.pages.wiki.wikipage import WikiPageFactory


class LinkDialogControllerTest(BaseMainWndTest):
    def setUp(self):
        super(LinkDialogControllerTest, self).setUp()
        copyTextToClipboard(u'')
        self._config = WikiConfig(Application.config)
        self._config.linkStyleOptions.value = 0

        self.files = [u'../test/samplefiles/accept.png',
                      u'../test/samplefiles/add.png',
                      u'../test/samplefiles/html.txt',
                      ]

        factory = WikiPageFactory()
        self._testpage = factory.create(self.wikiroot, u"Страница 1", [])

    def tearDown(self):
        super(LinkDialogControllerTest, self).tearDown()
        copyTextToClipboard(u'')

    def testEmpty_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, u'')
        self.assertEqual(controller.comment, u'')
        self.assertEqual(controller.linkResult, u'[[]]')

    def testEmpty_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)

        controller.showDialog()

        self.assertEqual(controller.link, u'')
        self.assertEqual(controller.comment, u'')
        self.assertEqual(controller.linkResult, u'<a href=""></a>')

    def testSelectedHttpLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'http://jenyay.net'

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, u'[[http://jenyay.net]]')

    def testSelectedHttpLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'http://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)

        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            u'<a href="http://jenyay.net">http://jenyay.net</a>')

    def testSelectedPageLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'page://__adsfadfasdf'

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, u'[[page://__adsfadfasdf]]')

    def testSelectedPageLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'page://__adsfadfasdf'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            u'<a href="page://__adsfadfasdf">page://__adsfadfasdf</a>')

    def testSelectedHttpsLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'https://jenyay.net'

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, u'[[https://jenyay.net]]')

    def testSelectedHttpsLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'https://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            u'<a href="https://jenyay.net">https://jenyay.net</a>')

    def testSelectedftpLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'ftp://jenyay.net'

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, u'[[ftp://jenyay.net]]')

    def testSelectedftpLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'ftp://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            u'<a href="ftp://jenyay.net">ftp://jenyay.net</a>')

    def testSelectedHttpLink2_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'HTTP://jenyay.net'

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, u'[[HTTP://jenyay.net]]')

    def testSelectedHttpLink2_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'HTTP://jenyay.net'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, selectedString)
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(
            controller.linkResult,
            u'<a href="HTTP://jenyay.net">HTTP://jenyay.net</a>')

    def testSelectedText_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'бла-бла-бла'

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, u'')
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, u'[[бла-бла-бла -> ]]')

    def testSelectedText_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'бла-бла-бла'

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, u'')
        self.assertEqual(controller.comment, selectedString)
        self.assertEqual(controller.linkResult, u'<a href="">бла-бла-бла</a>')

    def testClipboardHttpLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'http://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, u'[[http://jenyay.net]]')

    def testClipboardHttpLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'http://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            u'<a href="http://jenyay.net">http://jenyay.net</a>')

    def testClipboardHttpLink2_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'HTTP://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, u'[[HTTP://jenyay.net]]')

    def testClipboardHttpLink2_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'HTTP://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            u'<a href="HTTP://jenyay.net">HTTP://jenyay.net</a>')

    def testClipboardHttpsLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'https://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, u'[[https://jenyay.net]]')

    def testClipboardHttpsLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'https://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            u'<a href="https://jenyay.net">https://jenyay.net</a>')

    def testClipboardFtpLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'ftp://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, u'[[ftp://jenyay.net]]')

    def testClipboardFtpLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'ftp://jenyay.net'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            u'<a href="ftp://jenyay.net">ftp://jenyay.net</a>')

    def testClipboardPageLink_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'page://_asdfasdfasdf'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, u'[[page://_asdfasdfasdf]]')

    def testClipboardPageLink_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'page://_asdfasdfasdf'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            u'<a href="page://_asdfasdfasdf">page://_asdfasdfasdf</a>')

    def testClipboardAnchor_wiki(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'#anchor'
        copyTextToClipboard(clipboardText)

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(controller.linkResult, u'[[#anchor]]')

    def testClipboardAnchor_html(self):
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'#anchor'
        copyTextToClipboard(clipboardText)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertEqual(controller.link, clipboardText)
        self.assertEqual(controller.comment, clipboardText)
        self.assertEqual(
            controller.linkResult,
            u'<a href="#anchor">#anchor</a>')

    def testAttach_wiki(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn(u'Attach:accept.png', parent.linkText.GetItems())
        self.assertIn(u'Attach:add.png', parent.linkText.GetItems())
        self.assertIn(u'Attach:html.txt', parent.linkText.GetItems())

    def testAttach_html(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn(u'{}/accept.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn(u'{}/add.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn(u'{}/html.txt'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())

    def testSelectedAttach_wiki(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'Attach:add.png'

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn(u'Attach:accept.png', parent.linkText.GetItems())
        self.assertIn(u'Attach:add.png', parent.linkText.GetItems())
        self.assertIn(u'Attach:html.txt', parent.linkText.GetItems())

        self.assertEqual(controller.link, u'Attach:add.png')
        self.assertEqual(controller.comment, u'Attach:add.png')
        self.assertEqual(controller.linkResult, u'[[Attach:add.png]]')

        self.assertEqual(parent.linkText.GetValue(), u'Attach:add.png')

    def testSelectedAttach_html(self):
        Attachment(self._testpage).attach(self.files)
        parent = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'{}/add.png'.format(PAGE_ATTACH_DIR)

        controller = HtmlLinkDialogController(self._testpage,
                                              parent,
                                              selectedString)
        controller.showDialog()

        self.assertIn(u'{}/accept.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn(u'{}/add.png'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())
        self.assertIn(u'{}/html.txt'.format(PAGE_ATTACH_DIR),
                      parent.linkText.GetItems())

        self.assertEqual(controller.link,
                         u'{}/add.png'.format(PAGE_ATTACH_DIR))
        self.assertEqual(controller.comment,
                         u'{}/add.png'.format(PAGE_ATTACH_DIR))
        self.assertEqual(controller.linkResult,
                         u'<a href="{attach}/add.png">{attach}/add.png</a>'.format(attach=PAGE_ATTACH_DIR))

        self.assertEqual(parent.linkText.GetValue(),
                         u'{}/add.png'.format(PAGE_ATTACH_DIR))

    def testLinkStyle_01(self):
        self._config.linkStyleOptions.value = 0

        dlg = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              dlg,
                                              selectedString)
        dlg.link = u'Ссылка'
        dlg.comment = u'Коммент'

        controller.showDialog()

        self.assertEqual(controller.linkResult, u'[[Коммент -> Ссылка]]')

    def testLinkStyle_02(self):
        self._config.linkStyleOptions.value = 1

        dlg = LinkDialog(self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = WikiLinkDialogController(Application,
                                              self._testpage,
                                              dlg,
                                              selectedString)
        dlg.link = u'Ссылка'
        dlg.comment = u'Коммент'

        controller.showDialog()

        self.assertEqual(controller.linkResult, u'[[Ссылка | Коммент]]')
