# -*- coding: utf-8 -*-

from .lightboxcommand import LightboxCommand


class Controller(object):
    def __init__(self, application):
        self._application = application

    def initialize(self):
        self._application.onWikiParserPrepare += self._onWikiParserPrepare

    def destroy(self):
        self._application.onWikiParserPrepare -= self._onWikiParserPrepare

    def _onWikiParserPrepare(self, parser):
        parser.addCommand(LightboxCommand(parser))
