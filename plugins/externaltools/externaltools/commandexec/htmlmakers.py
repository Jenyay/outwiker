# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import urllib.request
import urllib.parse
import urllib.error

from .commandparams import PROTO_COMMAND, PROTO_TITLE, EXEC_BEGIN, TITLE_NAME


class HtmlMaker(metaclass=ABCMeta):
    """
    A base class for all HTML makers
    """

    @abstractmethod
    def createHtml(self, commandsList, paramsDict):
        pass

    def _createUrl(self, commandsList, paramsDict):
        urldict = {}

        for n, command in enumerate(commandsList):
            commandname = PROTO_COMMAND.format(number=n + 1)
            params_encoded = [param.encode("utf-8") for param in command.params]
            urldict[commandname] = [command.command.encode("utf-8")] + params_encoded

        urldict[PROTO_TITLE] = self._getTitle(commandsList, paramsDict).encode("utf-8")
        urlparams = urllib.parse.urlencode(urldict, True)

        return "".join([EXEC_BEGIN, "?", urlparams])

    def _getTitle(self, commandsList, paramsDict):
        text = (
            paramsDict[TITLE_NAME]
            if TITLE_NAME in paramsDict
            else commandsList[0].command
        )

        if len(commandsList) > 1:
            text += "..."

        return text


class HtmlMakerLink(HtmlMaker):
    """
    Create HTML code for (:exec:) command as link.
    """

    def createHtml(self, commandsList, paramsDict):
        if len(commandsList) == 0:
            return ""

        url = self._createUrl(commandsList, paramsDict)
        text = self._getTitle(commandsList, paramsDict)

        return '<a href="{url}" class="extools-execlink">{text}</a>'.format(
            url=url, text=text
        )


class HtmlMakerButton(HtmlMaker):
    """
    Create HTML code for (:exec:) command as button.
    """

    def createHtml(self, commandsList, paramsDict):
        if len(commandsList) == 0:
            return ""

        url = self._createUrl(commandsList, paramsDict)
        text = self._getTitle(commandsList, paramsDict)

        return """<button onclick='location.href="{url}"' class="extools-execbutton">{text}</button>""".format(
            url=url, text=text
        )
