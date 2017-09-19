# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import urllib

from commandparams import PROTO_COMMAND, PROTO_TITLE, EXEC_BEGIN, TITLE_NAME


class HtmlMaker(object):
    """
    A base class for all HTML makers
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def createHtml(self, commandsList, paramsDict):
        pass

    def _createUrl(self, commandsList, paramsDict):
        urldict = {}

        for n, command in enumerate(commandsList):
            commandname = PROTO_COMMAND.format(number=n + 1)
            params_encoded = [param.encode(u'utf-8')
                              for param
                              in command.params]
            urldict[commandname] = [command.command.encode(u'utf-8')] + params_encoded

        urldict[PROTO_TITLE] = self._getTitle(commandsList, paramsDict).encode(u'utf-8')
        urlparams = urllib.urlencode(urldict, True)

        return u''.join([EXEC_BEGIN, u'?', urlparams])

    def _getTitle(self, commandsList, paramsDict):
        text = (paramsDict[TITLE_NAME]
                if TITLE_NAME in paramsDict
                else commandsList[0].command)

        if len(commandsList) > 1:
            text += u'...'

        return text


class HtmlMakerLink(HtmlMaker):
    """
    Create HTML code for (:exec:) command as link.
    """
    def createHtml(self, commandsList, paramsDict):
        if len(commandsList) == 0:
            return u''

        url = self._createUrl(commandsList, paramsDict)
        text = self._getTitle(commandsList, paramsDict)

        return u'<a href="{url}" class="extools-execlink">{text}</a>'.format(
            url=url, text=text)


class HtmlMakerButton(HtmlMaker):
    """
    Create HTML code for (:exec:) command as button.
    """
    def createHtml(self, commandsList, paramsDict):
        if len(commandsList) == 0:
            return u''

        url = self._createUrl(commandsList, paramsDict)
        text = self._getTitle(commandsList, paramsDict)

        return u'''<button onclick='location.href="{url}"' class="extools-execbutton">{text}</button>'''.format(url=url, text=text)
