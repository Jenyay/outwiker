# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class CloseTabAction(BaseAction):
    """
    Закрыть текущую вкладку
    """

    stringId = "CloseTab"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Close tab")

    @property
    def description(self):
        return _("Close current tab")

    def run(self, params):
        assert self._application.mainWindow is not None

        index = self._application.mainWindow.tabsController.getSelection()
        if index != -1:
            self._application.mainWindow.tabsController.closeTab(index)


class AddTabAction(BaseAction):
    """
    Добавить вкладку
    """

    stringId = "AddTab"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Add tab")

    @property
    def description(self):
        return _("Add tab")

    def run(self, params):
        assert self._application.mainWindow is not None
        self._application.mainWindow.tabsController.cloneTab()


class NextTabAction(BaseAction):
    """
    Перейти на следующую вкладку
    """

    stringId = "NextTab"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Next tab")

    @property
    def description(self):
        return _("Go to next tab")

    def run(self, params):
        assert self._application.mainWindow is not None
        self._application.mainWindow.tabsController.nextTab()


class PreviousTabAction(BaseAction):
    """
    Перейти на предыдущую вкладку
    """

    stringId = "PreviousTab"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Previous tab")

    @property
    def description(self):
        return _("Go to previous tab")

    def run(self, params):
        assert self._application.mainWindow is not None
        self._application.mainWindow.tabsController.previousTab()
