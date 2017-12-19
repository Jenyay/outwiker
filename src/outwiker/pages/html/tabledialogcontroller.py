# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.commands import dictToStr


class BaseTableDialogController (object):
    def __init__ (self, dialog, config):
        self._dialog = dialog
        self._config = GeneralGuiConfig (config)


    def _getCells (self):
        cell = u'\n<td></td>'
        cells = u''.join ([cell] * self._dialog.colsCount)
        return cells


    def _getHCells (self):
        cell = u'\n<th></th>'
        cells = u''.join ([cell] * self._dialog.colsCount)
        return cells


    def _getRows (self):
        cells = self._getCells()
        row = u'\n<tr>{}\n</tr>'.format (cells)

        if self._dialog.headerCells:
            hcells = self._getHCells()
            hrow = u'\n<tr>{}\n</tr>'.format (hcells)
            body = u''.join ([hrow] + [row] * (self._dialog.rowsCount - 1))
        else:
            body = u''.join ([row] * self._dialog.rowsCount)

        return body



class TableDialogController (BaseTableDialogController):
    def __init__ (self, dialog, config):
        super (TableDialogController, self).__init__(dialog, config)
        self._dialog.colsCount = self._config.tableColsCount.value


    def showDialog (self):
        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._config.tableColsCount.value = self._dialog.colsCount

        return result


    def getResult (self):
        params = dictToStr (self._getTableParams ())

        if params:
            params = u' ' + params

        begin = u'<table{}>'.format (params)
        body = self._getRows()
        end = u'\n</table>'

        result = u''.join ([begin, body, end])
        return result


    def _getTableParams (self):
        """
        Return dictionary, where key - parameter name, value - parameter value
        """
        params = {}
        if self._dialog.borderWidth != 0:
            params[u'border'] = str (self._dialog.borderWidth)

        return params


class TableRowsDialogController (BaseTableDialogController):
    def __init__ (self, dialog, config):
        super (TableRowsDialogController, self).__init__(dialog, config)
        self._dialog.colsCount = self._config.tableColsCount.value


    def showDialog (self):
        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._config.tableColsCount.value = self._dialog.colsCount

        return result


    def getResult (self):
        body = self._getRows().strip()
        return body
