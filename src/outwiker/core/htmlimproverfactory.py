# -*- coding: UTF-8 -*-

from htmlimprover import BrHtmlImprover, ParagraphHtmlImprover


class HtmlImproverInfo (object):
    """
    Information about single HtmlImprover
    """
    def __init__ (self, key, obj, description):
        self.key = key
        self.obj = obj
        self.description = description



class HtmlImproverFactory (object):
    """
    Collection of the HTML improvers
    """
    def __init__ (self):
        self._improvers = {}

        self.add (u'brimprover',
                  BrHtmlImprover(),
                  _(u"Line Breaks"))

        self.add (u'pimprover',
                  ParagraphHtmlImprover(),
                  _(u"Paragraphs"))

        self._defaultImprover = u'brimprover'


    def add (self, key, obj, description):
        assert key not in self._improvers
        self._improvers[key] = HtmlImproverInfo (key, obj, description)


    def get (self, name):
        return (self._improvers[name].obj
                if name in self._improvers
                else self._improvers[self._defaultImprover].obj)


    def getDict (self):
        return self._improvers
