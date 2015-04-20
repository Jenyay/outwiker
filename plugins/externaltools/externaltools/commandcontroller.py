# -*- coding: UTF-8 -*-

import urlparse

from commandexec import CommandExec
from commandparams import EXEC_BEGIN, PROTO_TITLE


class CommandController (object):
    def __init__ (self, application):
        self._application = application

        # Enable (:exec:) command only in the "new" OutWiker version.
        # If Application has onLinkClick event
        self._enableExecCommand = u'onLinkClick' in dir (self._application)


    def initialize (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onHoverLink += self.__onHoverLink


    def destroy (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onHoverLink -= self.__onHoverLink


    def __onWikiParserPrepare (self, parser):
        """
        Teh event occures before parsing. Add the (:exec:) command
        """
        parser.addCommand (CommandExec (parser))


    def _getParams (self, url):
        """
        Return dictionary with params from url.
        Every value in dictionary is list
        """
        if (url is None or
                not url.startswith (EXEC_BEGIN)):
            return {}

        startpos = url.find (u'?')

        if startpos == -1 or startpos == len (url) - 1:
            return {}

        params = url[startpos + 1:]

        try:
            paramsDict = urlparse.parse_qs (params)
        except ValueError:
            return {}

        return paramsDict


    def __onHoverLink (self, page, link, title):
        if link is None:
            return

        urlparams = self._getParams (link)
        if PROTO_TITLE in urlparams:
            title[0] = u'>>> ' + urlparams[PROTO_TITLE][0]
