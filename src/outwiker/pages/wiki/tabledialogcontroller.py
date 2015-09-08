# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.guiconfig import GeneralGuiConfig


class BaseTableDialogController (object):
    def __init__ (self, dialog, suffix, config):
        """
        suffix - suffix for future table ('', '2', '3', etc)
        """
        self._dialog = dialog
        self._config = GeneralGuiConfig (config)
        self._suffix = suffix


    @staticmethod
    def dictToStr (paramsDict):
        items = []
        for name, value in paramsDict.items():
            valueStr = unicode (value)

            hasSingleQuote = u"'" in valueStr
            hasDoubleQuote = u'"' in valueStr

            if hasSingleQuote and hasDoubleQuote:
                valueStr = valueStr.replace (u'"', u'\\"')
                quote = u'"'
            elif hasDoubleQuote:
                quote = u"'"
            else:
                quote = u'"'

            paramStr = u'{name}={quote}{value}{quote}'.format (
                name = name,
                quote = quote,
                value = valueStr
            )

            items.append (paramStr)

        items.sort()
        return u', '.join (items)


    def _getCells (self):
        cell = u'\n(:cell{}:)'.format (self._suffix)
        cells = u''.join ([cell] * self._dialog.colsCount)
        return cells


    def _getRows (self):
        cells = self._getCells()
        row = u'\n(:row{}:)'.format (self._suffix) + cells
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
        params = self.dictToStr (self._getTableParams ())

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
            if self._dialog.borderWidth != 1:
                params[u'border'] = unicode (self._dialog.borderWidth)

        return params
