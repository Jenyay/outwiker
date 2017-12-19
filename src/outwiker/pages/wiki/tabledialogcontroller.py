# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.core.commands import dictToStr


class BaseTableDialogController (object):
    def __init__ (self, dialog, suffix, config):
        """
        suffix - suffix for future table ('', '2', '3', etc)
        """
        self._dialog = dialog
        self._config = GeneralGuiConfig (config)
        self._suffix = suffix


    def _getCells (self):
        cell = u'\n(:cell{}:)'.format (self._suffix)
        cells = u''.join ([cell] * self._dialog.colsCount)
        return cells


    def _getHCells (self):
        cell = u'\n(:hcell{}:)'.format (self._suffix)
        cells = u''.join ([cell] * self._dialog.colsCount)
        return cells


    def _getRows (self):
        cells = self._getCells()
        row = u'\n(:row{}:)'.format (self._suffix) + cells

        if self._dialog.headerCells:
            hcells = self._getHCells()
            hrow = u'\n(:row{}:)'.format (self._suffix) + hcells
            body = u''.join ([hrow] + [row] * (self._dialog.rowsCount - 1))
        else:
            body = u''.join ([row] * self._dialog.rowsCount)

        return body



class TableDialogController (BaseTableDialogController):
    def __init__ (self, dialog, suffix, config):
        """
        suffix - suffix for future table ('', '2', '3', etc)
        """
        super (TableDialogController, self).__init__(dialog, suffix, config)

        self._dialog.colsCount = self._config.tableColsCount.value


    def showDialog (self):
        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._config.tableColsCount.value = self._dialog.colsCount

        return result


    def getResult (self):
        """
        Return wiki notation string with (:table:)...(:tableend:) commands
        """
        params = dictToStr (self._getTableParams ())

        if params:
            params = u' ' + params

        begin = u'(:table{}{}:)'.format (self._suffix, params)
        body = self._getRows()
        end = u'\n(:table{}end:)'.format (self._suffix)

        result = u''.join ([begin, body, end])
        return result


    def _getTableParams (self):
        """
        Return dictionary, where key - parameter name, value - parameter value
        """
        params = {}
        if self._dialog.borderWidth != 0:
            params['border'] = str (self._dialog.borderWidth)

        return params


class TableRowsDialogController (BaseTableDialogController):
    def __init__ (self, dialog, suffix, config):
        """
        suffix - suffix for future table ('', '2', '3', etc)
        """
        super (TableRowsDialogController, self).__init__(dialog, suffix, config)
        self._dialog.colsCount = self._config.tableColsCount.value


    def showDialog (self):
        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._config.tableColsCount.value = self._dialog.colsCount

        return result


    def getResult (self):
        """
        Return wiki notation string with (:row:)(:cell:)(:cell:)... commands
        """
        body = self._getRows().strip()
        return body
