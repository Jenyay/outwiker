# -*- coding: utf-8 -*-

import wx

from outwiker.core.text import dictToStr
from outwiker.gui.guiconfig import GeneralGuiConfig


class BaseTableDialogController:
    def __init__(self, dialog, config):
        self._dialog = dialog
        self._config = GeneralGuiConfig(config)

    def _getCells(self):
        cell = "\n<td></td>"
        cells = "".join([cell] * self._dialog.colsCount)
        return cells

    def _getHCells(self):
        cell = "\n<th></th>"
        cells = "".join([cell] * self._dialog.colsCount)
        return cells

    def _getRows(self):
        cells = self._getCells()
        row = "\n<tr>{}\n</tr>".format(cells)

        if self._dialog.headerCells:
            hcells = self._getHCells()
            hrow = "\n<tr>{}\n</tr>".format(hcells)
            body = "".join([hrow] + [row] * (self._dialog.rowsCount - 1))
        else:
            body = "".join([row] * self._dialog.rowsCount)

        return body


class TableDialogController(BaseTableDialogController):
    def __init__(self, dialog, config):
        super(TableDialogController, self).__init__(dialog, config)
        self._dialog.colsCount = self._config.tableColsCount.value

    def showDialog(self):
        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._config.tableColsCount.value = self._dialog.colsCount

        return result

    def getResult(self):
        params = dictToStr(self._getTableParams())

        if params:
            params = " " + params

        begin = "<table{}>".format(params)
        body = self._getRows()
        end = "\n</table>"

        result = "".join([begin, body, end])
        return result

    def _getTableParams(self):
        """
        Return dictionary, where key - parameter name, value - parameter value
        """
        params = {}
        if self._dialog.borderWidth != 0:
            params["border"] = str(self._dialog.borderWidth)

        return params


class TableRowsDialogController(BaseTableDialogController):
    def __init__(self, dialog, config):
        super(TableRowsDialogController, self).__init__(dialog, config)
        self._dialog.colsCount = self._config.tableColsCount.value

    def showDialog(self):
        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._config.tableColsCount.value = self._dialog.colsCount

        return result

    def getResult(self):
        body = self._getRows().strip()
        return body
