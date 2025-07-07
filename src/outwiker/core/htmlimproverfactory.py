# -*- coding: utf-8 -*-

from .htmlimprover import BrHtmlImprover


class HtmlImproverInfo:
    """
    Information about single HtmlImprover
    """

    def __init__(self, key, obj, description):
        self.key = key
        self.obj = obj
        self.description = description


class HtmlImproverFactory:
    """
    Collection of the HTML improvers
    """

    def __init__(self, application):
        self._improvers = {}

        self._defaultImprover = "brimprover"

        self.add(self._defaultImprover, BrHtmlImprover(), _("Line Breaks (<br/>)"))

        application.onPrepareHtmlImprovers(self)

    def add(self, key, obj, description):
        assert key not in self._improvers
        self._improvers[key] = HtmlImproverInfo(key, obj, description)

    def __getitem__(self, name):
        return (
            self._improvers[name].obj
            if name in self._improvers
            else self._improvers[self._defaultImprover].obj
        )

    @property
    def names(self):
        return list(self._improvers.keys())

    def getDescription(self, name):
        return self._improvers[name].description
