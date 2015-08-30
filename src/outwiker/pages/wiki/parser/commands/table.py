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
        super (TableCommand, self).__init__ (parser)
        self._suffix = suffix

        # For using by others commands (row, cell)
        self.firstRow = True
        self.firstCell = True


    @property
    def suffix (self):
        return self._suffix


    @property
    def name (self):
        return u'table' + self.suffix


    def execute (self, params, content):
        start = (u'<table>' if not params.strip()
                 else u'<table {}>'.format (params.strip()))
        end = u'</table>'

        rowCommand = RowCommand (self.parser, self)
        cellCommand = CellCommand (self.parser, self)

        self.parser.addCommand (rowCommand)
        self.parser.addCommand (cellCommand)

        try:
            body = self.parser.parseWikiMarkup (content)

            if not self.firstCell:
                body += u'</td>'

            if not self.firstRow:
                body += u'</tr>'
        finally:
            self.parser.removeCommand (rowCommand.name)
            self.parser.removeCommand (cellCommand.name)

        result = start + body + end

        result = result.replace (u'\n</tr>', u'</tr>')
        result = result.replace (u'\n<tr', u'<tr')
        result = result.replace (u'\n</td>', u'</td>')
        result = result.replace (u'\n<td', u'<td')

        self.firstRow = True
        self.firstCell = True

        return result



class RowCommand (Command):
    def __init__ (self, parser, table):
        super (RowCommand, self).__init__ (parser)
        self._table = table


    @property
    def name (self):
        return u'row' + self._table.suffix


    def execute (self, params, content):
        tag = u''

        if not self._table.firstCell:
            tag = u'</td>'

        if not self._table.firstRow:
            tag = tag + u'</tr>'

        tag += (u'<tr>' if not params.strip()
                else u'<tr {}>'.format (params.strip()))

        self._table.firstRow = False
        self._table.firstCell = True

        return tag



class CellCommand (Command):
    def __init__ (self, parser, table):
        super (CellCommand, self).__init__ (parser)
        self._table = table


    @property
    def name (self):
        return u'cell' + self._table.suffix


    def execute (self, params, content):
        tag = (u'<td>' if not params.strip()
               else u'<td {}>'.format (params.strip()))

        if self._table.firstRow:
            tag = u'<tr>' + tag
            self._table.firstRow = False

        if not self._table.firstCell:
            tag = u'</td>' + tag

        self._table.firstCell = False

        return tag
