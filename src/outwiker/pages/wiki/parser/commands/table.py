# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command


class TableCommand (Command):
    """
    Command for parsing text like

    (:table params:)
    (:row params:)
    (:cell params:) ...
    (:cell params:) ...
    ...
    (:cell params:) ...
    (:row params:)
    (:cell params:) ...
    (:cell params:) ...
    ...
    (:cell params:) ...
    ...
    (:tableend:)

    or

    (:table2 params:)
    (:row2 params:)
    (:cell2 params:) ...
    (:cell2 params:) ...
    ...
    (:cell2 params:) ...
    (:row2 params:)
    (:cell2 params:) ...
    (:cell2 params:) ...
    ...
    (:cell2 params:) ...
    ...
    (:table2end:)
    """
    def __init__ (self, parser, suffix=u''):
        """
        parser - parser instance
        """
        Command.__init__ (self, parser)
        self._suffix = suffix


    @property
    def name (self):
        return u'table' + self._suffix


    def execute (self, params, content):
        start = (u'<table>' if not params.strip()
                 else u'<table {}>'.format (params.strip()))
        end = u'</table>'
        body = u''

        result = start + body + end

        return result
