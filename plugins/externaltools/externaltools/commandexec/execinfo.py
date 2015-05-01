# -*- coding: UTF-8 -*-


class ExecInfo (object):
    """
    Contain single command.
        command - program for executing
        params - list of the program params
    """
    def __init__ (self, command, params):
        self.command = command
        self.params = params[:]
