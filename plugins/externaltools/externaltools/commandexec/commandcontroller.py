# -*- coding: UTF-8 -*-

import urlparse
import subprocess

from outwiker.core.system import getOS

from commandexec import CommandExec
from commandparams import EXEC_BEGIN, PROTO_TITLE, PROTO_COMMAND


class CommandController (object):
    def __init__ (self, application):
        self._application = application

        # Enable (:exec:) command only in the "new" OutWiker version.
        # If Application has onLinkClick event
        self._enableExecCommand = u'onLinkClick' in dir (self._application)


    def initialize (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onHoverLink += self._onHoverLink
            self._application.onLinkClick += self._onLinkClick


    def destroy (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onHoverLink -= self._onHoverLink
            self._application.onLinkClick -= self._onLinkClick


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
            paramsDict = urlparse.parse_qs (str (params))
        except ValueError:
            return {}

        return paramsDict


    def _onHoverLink (self, page, params):
        if params.link is None:
            return

        urlparams = self._getParams (params.link)
        if PROTO_TITLE in urlparams:
            params.text = u'>>> ' + unicode (urlparams[PROTO_TITLE][0], "utf8")


    def _onLinkClick (self, page, params):
        if params.link is None:
            return

        urlparams = self._getParams (params.link)
        if not urlparams:
            return

        params.process = True

        comindex = 1
        comparams = PROTO_COMMAND.format (number = comindex)

        encoding = getOS().filesEncoding

        while comparams in urlparams:
            command = unicode (urlparams[comparams][0], "utf8").encode (encoding)
            params = [unicode (param, "utf8").encode (encoding)
                      for param
                      in urlparams[comparams][1:]]

            self._execute (command, params)

            comindex += 1
            comparams = PROTO_COMMAND.format (number = comindex)


    def _execute (self, command, params):
        try:
            subprocess.Popen ([command] + params)
        except (OSError, subprocess.CalledProcessError):
            pass
