# -*- coding: UTF-8 -*-

from abc import abstractmethod

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

    def __init__(self, parser, suffix=u''):
        """
        parser - parser instance
        """
        super(TableCommand, self).__init__(parser)
        self._suffix = suffix

        # For using by others commands (row, cell)
        self.firstRow = True

        # None / td / th
        self.lastCellTag = None


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
        hcellCommand = HCellCommand (self.parser, self)

        self.parser.addCommand (rowCommand)
        self.parser.addCommand (cellCommand)
        self.parser.addCommand (hcellCommand)

        try:
            body = self.parser.parseWikiMarkup(content)

            if self.lastCellTag is not None:
                body += u'</{}>'.format(self.lastCellTag)

            if not self.firstRow:
                body += u'</tr>'
        finally:
            self.parser.removeCommand (rowCommand.name)
            self.parser.removeCommand (cellCommand.name)
            self.parser.removeCommand (hcellCommand.name)

        result = start + body + end

        result = result.replace (u'\n</tr>', u'</tr>')
        result = result.replace (u'\n<tr', u'<tr')
        result = result.replace (u'\n</td>', u'</td>')
        result = result.replace (u'\n<td', u'<td')
        result = result.replace (u'\n</th>', u'</th>')
        result = result.replace (u'\n<th', u'<th')

        self.firstRow = True
        self.lastCellTag = None

        return result



class RowCommand (Command):
    def __init__ (self, parser, table):
        super (RowCommand, self).__init__ (parser)
        self._table = table

    @property
    def name(self):
        return u'row' + self._table.suffix

    def execute(self, params, content):
        tag = u''

        if self._table.lastCellTag is not None:
            tag = u'</{}>'.format(self._table.lastCellTag)

        if not self._table.firstRow:
            tag = tag + u'</tr>'

        tag += (u'<tr>' if not params.strip()
                else u'<tr {}>'.format(params.strip()))

        self._table.firstRow = False
        self._table.lastCellTag = None

        result = tag + self.parser.parseWikiMarkup(content.strip())

        return result


class BaseCellCommand (Command):
    def __init__ (self, parser, table):
        super (BaseCellCommand, self).__init__ (parser)
        self._table = table

    @abstractmethod
    def _getTag(self):
        pass

    def execute(self, params, content):
        currentTag = self._getTag()

        tag = (u'<{}>'.format(currentTag) if not params.strip()
               else u'<{} {}>'.format(currentTag, params.strip()))

        if self._table.firstRow:
            tag = u'<tr>' + tag
            self._table.firstRow = False

        if self._table.lastCellTag is not None:
            tag = u'</{}>'.format(self._table.lastCellTag) + tag

        self._table.lastCellTag = currentTag

        tag = tag + self.parser.parseWikiMarkup(content.strip())
        return tag


class CellCommand (BaseCellCommand):

    @property
    def name(self):
        return u'cell' + self._table.suffix

    def _getTag(self):
        return u'td'


class HCellCommand (BaseCellCommand):

    @property
    def name(self):
        return u'hcell' + self._table.suffix

    def _getTag(self):
        return u'th'
