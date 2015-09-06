# -*- coding: UTF-8 -*-


class TableDialogController (object):
    def __init__ (self, dialog, suffix, config):
        """
        suffix - suffix for future table ('', '2', '3', etc)
        """
        self._dialog = dialog
        self._config = config
        self._suffix = suffix


    def showDialog (self):
        result = self._dialog.ShowModal()
        return result


    def getResult (self):
        """
        Return wiki notation string with (:table:)...(:tableend:) commands
        """
        params = self.dictToStr (self._getTableParams ())

        if params:
            begin = u'(:table{} {}:)'.format (self._suffix, params)
        else:
            begin = u'(:table{}:)'.format (self._suffix)

        cell = u'\n(:cell{}:)'.format (self._suffix)
        cells = u''.join ([cell] * self._dialog.colsCount)

        row = u'\n(:row{}:)'.format (self._suffix) + cells

        body = u''.join ([row] * self._dialog.rowsCount)

        end = u'\n(:table{}end:)'.format (self._suffix)


        result = u''.join ([begin, body, end])
        return result


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


    def _getTableParams (self):
        """
        Return dictionary, where key - parameter name, value - parameter value
        """
        params = {}
        if self._dialog.borderWidth != 0:
            if self._dialog.borderWidth != 1:
                params[u'border'] = unicode (self._dialog.borderWidth)

        return params
