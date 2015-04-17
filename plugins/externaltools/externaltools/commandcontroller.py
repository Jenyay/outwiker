# -*- coding: UTF-8 -*-

from commandexec import CommandExec


class CommandController (object):
    def __init__ (self, application):
        self._application = application


    def initialize (self):
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare


    def destroy (self):
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare


    def __onWikiParserPrepare (self, parser):
        """
        Teh event occures before parsing. Add the (:exec:) command
        """
        parser.addCommand (CommandExec (parser))
