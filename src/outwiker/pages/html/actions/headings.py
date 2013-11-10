#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class HtmlHeading1Action (BaseAction):
    """
    Заголовок первого уровня
    """
    stringId = u"HtmlHeading1"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"First-level heading")


    @property
    def description (self):
        return _(u"First-level heading for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<h1>", u"</h1>")


class HtmlHeading2Action (BaseAction):
    """
    Заголовок второго уровня
    """
    stringId = u"HtmlHeading2"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Second-level heading")


    @property
    def description (self):
        return _(u"Second-level heading for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<h2>", u"</h2>")


class HtmlHeading3Action (BaseAction):
    """
    Заголовок третьего уровня
    """
    stringId = u"HtmlHeading3"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle three")


    @property
    def description (self):
        return _(u"Subtitle three for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<h3>", u"</h3>")


class HtmlHeading4Action (BaseAction):
    """
    Заголовок четвертого уровня
    """
    stringId = u"HtmlHeading4"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle four")


    @property
    def description (self):
        return _(u"Subtitle four for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<h4>", u"</h4>")


class HtmlHeading5Action (BaseAction):
    """
    Заголовок пятого уровня
    """
    stringId = u"HtmlHeading5"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle five")


    @property
    def description (self):
        return _(u"Subtitle five for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<h5>", u"</h5>")


class HtmlHeading6Action (BaseAction):
    """
    Заголовок шестого уровня
    """
    stringId = u"HtmlHeading6"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle six")


    @property
    def description (self):
        return _(u"Subtitle six for HTML pages")


    @property
    def strid (self):
        return self.stringId


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"<h6>", u"</h6>")
