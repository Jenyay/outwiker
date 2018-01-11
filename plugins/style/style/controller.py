# -*- coding: utf-8 -*-

from .stylecommand import StyleCommand


class Controller(object):
    def __init__(self, application):
        self._application = application
        self.STYLE_TOOL_ID = u"PLUGIN_STYLE_TOOL_ID"

    def initialize(self):
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare

    def destroy(self):
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare

    def __onWikiParserPrepare(self, parser):
        parser.addCommand(StyleCommand(parser))
