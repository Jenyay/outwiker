# -*- coding: UTF-8 -*-

from outwiker.gui.linkdialogcontroller import LinkDialogContoller
from outwiker.core.commands import copyTextToClipboard
from .basemainwnd import BaseMainWndTest


class FakeLinkDialog (object):
    """
    Фальшивый диалог для вставки ссылок.
    """
    def __init__ (self, parent, link, comment):
        self.parent = parent
        self.link = link
        self.comment = comment


    def ShowModal (self):
        return None


    def Destroy(self):
        pass


class TestController (LinkDialogContoller):
    """
    Класс для тестирования контроллера, отвязанный от wxPython
    """
    def _createDialog (self, parent, link, comment):
        return FakeLinkDialog (parent, link, comment)


class LinkDialogControllerTest (BaseMainWndTest):
    def setUp (self):
        super (LinkDialogControllerTest, self).setUp()
        copyTextToClipboard (u"")


    def tearDown (self):
        super (LinkDialogControllerTest, self).tearDown()
        copyTextToClipboard (u"")


    def testEmpty (self):
        parent = None
        selectedString = u""

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, u"")
        self.assertEqual (controller.comment, u"")


    def testSelectedHttpLink (self):
        parent = None
        selectedString = u"http://jenyay.net"

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)


    def testSelectedPageLink (self):
        parent = None
        selectedString = u"page://__adsfadfasdf"

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)


    def testSelectedHttpsLink (self):
        parent = None
        selectedString = u"https://jenyay.net"

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)


    def testSelectedftpLink (self):
        parent = None
        selectedString = u"ftp://jenyay.net"

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)


    def testSelectedHttpLink2 (self):
        parent = None
        selectedString = u"HTTP://jenyay.net"

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, selectedString)
        self.assertEqual (controller.comment, selectedString)


    def testSelectedText (self):
        parent = None
        selectedString = u"бла-бла-бла"

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, u"")
        self.assertEqual (controller.comment, selectedString)


    def testClipboardHttpLink (self):
        parent = None
        selectedString = u""
        clipboardText = u"http://jenyay.net"
        copyTextToClipboard (clipboardText)

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)


    def testClipboardHttpLink2 (self):
        parent = None
        selectedString = u""
        clipboardText = u"HTTP://jenyay.net"
        copyTextToClipboard (clipboardText)

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)


    def testClipboardHttpsLink (self):
        parent = None
        selectedString = u""
        clipboardText = u"https://jenyay.net"
        copyTextToClipboard (clipboardText)

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)


    def testClipboardFtpLink (self):
        parent = None
        selectedString = u""
        clipboardText = u"ftp://jenyay.net"
        copyTextToClipboard (clipboardText)

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)


    def testClipboardPageLink (self):
        parent = None
        selectedString = u""
        clipboardText = u"page://_asdfasdfasdf"
        copyTextToClipboard (clipboardText)

        controller = TestController (parent, selectedString)
        controller.showDialog()

        self.assertEqual (controller.link, clipboardText)
        self.assertEqual (controller.comment, clipboardText)
