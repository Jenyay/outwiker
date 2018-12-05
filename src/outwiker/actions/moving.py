# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class GoToParentAction (BaseAction):
    """
    Go to the parent page action
    """
    stringId = u"GoToParent"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Go to parent page")

    @property
    def description(self):
        return _(u'Open parent page')

    def run(self, params):
        if (self._application.wikiroot is not None and
                self._application.selectedPage is not None and
                self._application.selectedPage.parent is not None):
            self._application.selectedPage = self._application.selectedPage.parent


class GoToFirstChildAction (BaseAction):
    """
    Go to the first child page action
    """
    stringId = u"GoToFirstChild"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Go to first child page")

    @property
    def description(self):
        return _(u'Open first child page')

    def run(self, params):
        if self._application.wikiroot is None:
            return

        if self._application.selectedPage is not None:
            if len(self._application.selectedPage.children) != 0:
                self._application.selectedPage = self._application.selectedPage.children[0]
        elif len(self._application.wikiroot.children) != 0:
            self._application.selectedPage = self._application.wikiroot.children[0]


class GoToNextSiblingAction (BaseAction):
    """
    Go to next sibling page action
    """
    stringId = u"GoToNextSibling"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Go to next page")

    @property
    def description(self):
        return _(u'Open next page')

    def run(self, params):
        if (self._application.wikiroot is None or
                self._application.selectedPage is None or
                self._application.selectedPage.parent is None):
            return

        siblings = self._application.selectedPage.parent.children
        self_pos = siblings.index(self._application.selectedPage)

        if self_pos < len(siblings) - 1:
            self._application.selectedPage = siblings[self_pos + 1]


class GoToPrevSiblingAction (BaseAction):
    """
    Go to previous sibling page action
    """
    stringId = u"GoToPrevSibling"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Go to previous page")

    @property
    def description(self):
        return _(u'Open previous page')

    def run(self, params):
        if (self._application.wikiroot is None or
                self._application.selectedPage is None or
                self._application.selectedPage.parent is None):
            return

        siblings = self._application.selectedPage.parent.children
        self_pos = siblings.index(self._application.selectedPage)

        if self_pos != 0:
            self._application.selectedPage = siblings[self_pos - 1]
