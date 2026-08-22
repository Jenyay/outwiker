# -*- coding: UTF-8 -*-

from abc import abstractmethod

from outwiker.pages.wiki.parser.command import Command


class TableCommand(Command):
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

    def __init__(self, parser, suffix=""):
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
    def suffix(self):
        return self._suffix

    @property
    def name(self):
        return "table" + self.suffix

    def execute(self, params, content):
        start = "<table>" if not params.strip() else "<table {}>".format(params.strip())
        end = "</table>"

        rowCommand = RowCommand(self.parser, self)
        cellCommand = CellCommand(self.parser, self)
        hcellCommand = HCellCommand(self.parser, self)

        self.parser.addCommand(rowCommand)
        self.parser.addCommand(cellCommand)
        self.parser.addCommand(hcellCommand)

        try:
            body = self.parser.parseWikiMarkup(content)

            if self.lastCellTag is not None:
                body += "</{}>".format(self.lastCellTag)

            if not self.firstRow:
                body += "</tr>"
        finally:
            self.parser.removeCommand(rowCommand.name)
            self.parser.removeCommand(cellCommand.name)
            self.parser.removeCommand(hcellCommand.name)

        result = start + body + end

        result = result.replace("\n</tr>", "</tr>")
        result = result.replace("\n<tr", "<tr")
        result = result.replace("\n</td>", "</td>")
        result = result.replace("\n<td", "<td")
        result = result.replace("\n</th>", "</th>")
        result = result.replace("\n<th", "<th")

        self.firstRow = True
        self.lastCellTag = None

        return result


class RowCommand(Command):
    def __init__(self, parser, table):
        super(RowCommand, self).__init__(parser)
        self._table = table

    @property
    def name(self):
        return "row" + self._table.suffix

    def execute(self, params, content):
        tag = ""

        if self._table.lastCellTag is not None:
            tag = "</{}>".format(self._table.lastCellTag)

        if not self._table.firstRow:
            tag = tag + "</tr>"

        tag += "<tr>" if not params.strip() else "<tr {}>".format(params.strip())

        self._table.firstRow = False
        self._table.lastCellTag = None

        result = tag + self.parser.parseWikiMarkup(content.strip())

        return result


class BaseCellCommand(Command):
    def __init__(self, parser, table):
        super(BaseCellCommand, self).__init__(parser)
        self._table = table

    @abstractmethod
    def _getTag(self):
        pass

    def execute(self, params, content):
        currentTag = self._getTag()

        tag = (
            "<{}>".format(currentTag)
            if not params.strip()
            else "<{} {}>".format(currentTag, params.strip())
        )

        if self._table.firstRow:
            tag = "<tr>" + tag
            self._table.firstRow = False

        if self._table.lastCellTag is not None:
            tag = "</{}>".format(self._table.lastCellTag) + tag

        self._table.lastCellTag = currentTag

        tag = tag + self.parser.parseWikiMarkup(content.strip())
        return tag


class CellCommand(BaseCellCommand):
    @property
    def name(self):
        return "cell" + self._table.suffix

    def _getTag(self):
        return "td"


class HCellCommand(BaseCellCommand):
    @property
    def name(self):
        return "hcell" + self._table.suffix

    def _getTag(self):
        return "th"
