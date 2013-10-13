#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiHeading1Action (BaseAction):
    """
    Заголовок первого уровня
    """
    stringId = u"WikiHeading1"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"First-level heading")


    @property
    def description (self):
        return _(u"First-level heading for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"!! ", u"")


class WikiHeading2Action (BaseAction):
    """
    Заголовок второго уровня
    """
    stringId = u"WikiHeading2"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Second-level heading")


    @property
    def description (self):
        return _(u"Second-level heading for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"!!! ", u"")


class WikiHeading3Action (BaseAction):
    """
    Заголовок третьего уровня
    """
    stringId = u"WikiHeading3"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle three")


    @property
    def description (self):
        return _(u"Subtitle three for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"!!!! ", u"")


class WikiHeading4Action (BaseAction):
    """
    Заголовок четвертого уровня
    """
    stringId = u"WikiHeading4"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle four")


    @property
    def description (self):
        return _(u"Subtitle four for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"!!!!! ", u"")


class WikiHeading5Action (BaseAction):
    """
    Заголовок пятого уровня
    """
    stringId = u"WikiHeading5"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle five")


    @property
    def description (self):
        return _(u"Subtitle five for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"!!!!!! ", u"")


class WikiHeading6Action (BaseAction):
    """
    Заголовок шестого уровня
    """
    stringId = u"WikiHeading6"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Subtitle six")


    @property
    def description (self):
        return _(u"Subtitle six for wiki pages")
    

    @property
    def strid (self):
        return self.stringId
    
    
    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"!!!!!!! ", u"")
