# -*- coding: UTF-8 -*-

from commandexec import CommandExec


class CommandController (object):
    def __init__ (self, application):
        self._application = application

        # Enable (:exec:) command only in the "new" OutWiker version.
        # If Application has onLinkClick event
        self._enableExecCommand = u'onLinkClick' in dir (self._application)


    def initialize (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare


    def destroy (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare


    def __onWikiParserPrepare (self, parser):
        """
        Teh event occures before parsing. Add the (:exec:) command
        """
        parser.addCommand (CommandExec (parser))
