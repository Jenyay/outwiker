# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class CloseTabAction (BaseAction):
    """
    Закрыть текущую вкладку
    """
    stringId = u"CloseTab"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Close Tab")


    @property
    def description (self):
        return _(u"Close current tab")

    def run(self, params):
        assert self._application.mainWindow is not None

        index = self._application.mainWindow.tabsController.getSelection()
        if index != -1:
            self._application.mainWindow.tabsController.closeTab(index)


class AddTabAction (BaseAction):
    """
    Добавить вкладку
    """
    stringId = u"AddTab"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Add Tab")

    @property
    def title (self):
        return _(u"Add Tab")


    @property
    def description (self):
        return _(u"Add tab")

    def run(self, params):
        assert self._application.mainWindow is not None
        self._application.mainWindow.tabsController.cloneTab()


class NextTabAction (BaseAction):
    """
    Перейти на следующую вкладку
    """
    stringId = u"NextTab"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Next Tab")


    @property
    def description (self):
        return _(u"Go to next tab")


    def run (self, params):
        assert self._application.mainWindow is not None
        self._application.mainWindow.tabsController.nextTab()



class PreviousTabAction (BaseAction):
    """
    Перейти на предыдущую вкладку
    """
    stringId = u"PreviousTab"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Previous Tab")


    @property
    def description (self):
        return _(u"Go to previous tab")


    def run (self, params):
        assert self._application.mainWindow is not None
        self._application.mainWindow.tabsController.previousTab()
