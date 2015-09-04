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
        params = u''

        if params:
            begin = u'(:table{} {}:)'.format (self._suffix, params)
        else:
            begin = u'(:table{}:)'.format (self._suffix)

        end = u'\n(:table{}end:)'.format (self._suffix)

        body = u''

        result = u''.join ([begin, body, end])
        return result
