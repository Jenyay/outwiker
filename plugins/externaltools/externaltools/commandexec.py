#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command


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
        params_dict = Command.parseParams (params)

        return u''


    # def _getNameParam (self, params_dict):
    #     name = params_dict[NAME_PARAM_NAME].strip() if NAME_PARAM_NAME in params_dict else u""
    #     return name
