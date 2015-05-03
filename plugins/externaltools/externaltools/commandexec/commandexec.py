# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command

from commandexecparser import CommandExecParser
from htmlmakers import HtmlMakerLink


class CommandExec (Command):
    """
    Command (:exec:) for execute custom tools from wiki page
    """
    def __init__ (self, parser):
        super (CommandExec, self).__init__ (parser)


    @property
    def name (self):
        """
        Return command name
        """
        return u"exec"


    def execute (self, params, content):
        """
        Run command.
        The method returns link which will replace the command notation
        """
        paramsDict = Command.parseParams (params)

        commandParser = CommandExecParser (self.parser.page)
        commandsList = commandParser.parse (content)

        htmlMaker = self._createHtmlMaker (paramsDict)
        html = htmlMaker.createHtml (commandsList, paramsDict)

        return html


    @staticmethod
    def _createHtmlMaker (paramsDict):
        htmlMaker = HtmlMakerLink ()
        return htmlMaker
