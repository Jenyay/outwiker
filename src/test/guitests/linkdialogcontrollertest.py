# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest

from outwiker.pages.wiki.wikilinkdialogcontroller import WikiLinkDialogController
from outwiker.pages.html.htmllinkdialogcontroller import HtmlLinkDialogController
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.gui.linkdialog import LinkDialog
from outwiker.core.commands import copyTextToClipboard
from outwiker.gui.tester import Tester
from outwiker.core.application import Application


class LinkDialogControllerTest (BaseMainWndTest):
    def setUp (self):
        super (LinkDialogControllerTest, self).setUp()
        copyTextToClipboard (u'')
        self._config = WikiConfig (Application.config)
        self._config.linkStyleOptions.value = 0


    def tearDown (self):
        super (LinkDialogControllerTest, self).tearDown()
        copyTextToClipboard (u'')


    def testEmpty_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, u'')
        self.assertEqual (controller.comment, u'')
        self.assertEqual (controller.linkResult, u'[[]]')


    def testEmpty_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, u'')
        self.assertEqual (controller.comment, u'')
        self.assertEqual (controller.linkResult, u'<a href=""></a>')


    def testSelectedHttpLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'http://jenyay.net'

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'[[http://jenyay.net]]')


    def testSelectedHttpLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'http://jenyay.net'

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'<a href="http://jenyay.net">http://jenyay.net</a>')


    def testSelectedPageLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'page://__adsfadfasdf'

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'[[page://__adsfadfasdf]]')


    def testSelectedPageLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'page://__adsfadfasdf'

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'<a href="page://__adsfadfasdf">page://__adsfadfasdf</a>')


    def testSelectedHttpsLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'https://jenyay.net'

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'[[https://jenyay.net]]')


    def testSelectedHttpsLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'https://jenyay.net'

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'<a href="https://jenyay.net">https://jenyay.net</a>')


    def testSelectedftpLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'ftp://jenyay.net'

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'[[ftp://jenyay.net]]')


    def testSelectedftpLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'ftp://jenyay.net'

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'<a href="ftp://jenyay.net">ftp://jenyay.net</a>')


    def testSelectedHttpLink2_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'HTTP://jenyay.net'

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'[[HTTP://jenyay.net]]')


    def testSelectedHttpLink2_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'HTTP://jenyay.net'

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'<a href="HTTP://jenyay.net">HTTP://jenyay.net</a>')


    def testSelectedText_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'бла-бла-бла'

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, u'')
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'[[бла-бла-бла -> ]]')


    def testSelectedText_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u'бла-бла-бла'

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, u'')
        self.assertEqual (controller.comment, selectedString)
        self.assertEqual (controller.linkResult, u'<a href="">бла-бла-бла</a>')


    def testClipboardHttpLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'http://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (controller.linkResult, u'[[http://jenyay.net]]')


    def testClipboardHttpLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'http://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (
            controller.linkResult,
            u'<a href="http://jenyay.net">http://jenyay.net</a>')


    def testClipboardHttpLink2_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'HTTP://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (controller.linkResult, u'[[HTTP://jenyay.net]]')


    def testClipboardHttpLink2_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'HTTP://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (
            controller.linkResult,
            u'<a href="HTTP://jenyay.net">HTTP://jenyay.net</a>')


    def testClipboardHttpsLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'https://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (controller.linkResult, u'[[https://jenyay.net]]')


    def testClipboardHttpsLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'https://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (
            controller.linkResult,
            u'<a href="https://jenyay.net">https://jenyay.net</a>')


    def testClipboardFtpLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'ftp://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (controller.linkResult, u'[[ftp://jenyay.net]]')


    def testClipboardFtpLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'ftp://jenyay.net'
        copyTextToClipboard (clipboardText)

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (
            controller.linkResult,
            u'<a href="ftp://jenyay.net">ftp://jenyay.net</a>')


    def testClipboardPageLink_wiki (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'page://_asdfasdfasdf'
        copyTextToClipboard (clipboardText)

        controller = WikiLinkDialogController (Application, parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (controller.linkResult, u'[[page://_asdfasdfasdf]]')


    def testClipboardPageLink_html (self):
        parent = LinkDialog (self.wnd)
        Tester.dialogTester.appendOk()
        selectedString = u''
        clipboardText = u'page://_asdfasdfasdf'
        copyTextToClipboard (clipboardText)

        controller = HtmlLinkDialogController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
        self.assertEqual (
            controller.linkResult,
            u'<a href="page://_asdfasdfasdf">page://_asdfasdfasdf</a>')
