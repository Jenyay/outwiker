# -*- coding: utf-8 -*-

from .commandspoiler import SpoilerCommand


class Controller(object):
    def __init__(self, application):
        self._application = application
        self.__maxCommandIndex = 9

    def initialize(self):
        self._application.onWikiParserPrepare += self._onWikiParserPrepare

    def destroy(self):
        self._application.onWikiParserPrepare -= self._onWikiParserPrepare

    def _onWikiParserPrepare(self, parser):
        parser.addCommand(SpoilerCommand(parser, "spoiler", _))

        for index in range(self.__maxCommandIndex + 1):
            commandname = "spoiler{index}".format(index=index)
            parser.addCommand(SpoilerCommand(parser, commandname, _))
