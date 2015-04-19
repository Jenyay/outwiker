# -*- coding: UTF-8 -*-

import urllib

from commandparams import PROTO_COMMAND


class HtmlMakerLink (object):
    def __init__ (self):
        self._begin = u'exec://exec/'


    def _createUrl (self, commandsList, paramsDict):
        urldict = {}

        for n, command in enumerate (commandsList):
            commandname = PROTO_COMMAND.format (number = n + 1)
            params_encoded = [param.encode (u'utf-8') for param in command.params]
            urldict[commandname] = [command.command.encode (u'utf-8')] + params_encoded

        urlparams = urllib.urlencode (urldict, True)

        return u''.join ([self._begin, u'?', urlparams])


    def createHtml (self, commandsList, paramsDict):
        if len (commandsList) == 0:
            return u''

        url = self._createUrl (commandsList, paramsDict)
        text = commandsList[0].command
        if len (commandsList) > 1:
            text += u'...'

        return u'<a href="{url}">{text}</a>'.format (url=url, text=text)
