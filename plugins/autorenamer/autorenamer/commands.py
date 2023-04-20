# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.wikiparser import Command
from .renamer import Renamer


class AutoRenameTagCommand(Command):
    def __init__(self, application, parser):
        super().__init__(parser)
        self._application = application
        self._renamer = Renamer(application)

    @property
    def name(self):
        return "autorename"

    def execute(self, params, content):
        self._renamer.RenamePage(True)
        return ""
