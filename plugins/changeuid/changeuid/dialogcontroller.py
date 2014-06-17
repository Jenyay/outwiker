# -*- coding: UTF-8 -*-

import re


class DialogController (object):
    """
    Класс для управления диалогом InsertDialog
    """
    def __init__ (self, application, dialog, page):
        """
        dialog - экземпляр класса InsertDialog, который надо будет показать пользователю.
        page - текущая страница, для которой показывается диалог
        """
        assert page is not None
        assert dialog is not None
        assert application is not None

        self._application = application
        self._dialog = dialog
        self._page = page
        self._dialog.uid = self._application.pageUidDepot.createUid (self._page)
        self._dialog.uidValidator = self.validate


    def showDialog (self):
        """
        Метод показывает диалог и возвращает строку, соответствующую выбранным настройкам
        Если пользователь нажимает кнопку "Cancel", возвращается None
        """
        result = self._dialog.ShowModal()

        return result


    def validate (self, newiud):
        """
        Возвращает True, если newiud соответствует требованиям к идентификаторам и False в противном случае
        """
        otherpage = self._application.pageUidDepot[newiud]

        if (otherpage is not None and otherpage != self._page):
            return False

        regexp = re.compile (r"^[-\w,\$\.\+\!\*\(\):@|&=\?~\#\%]+$", re.I | re.U)
        match = regexp.match (newiud)

        return match is not None
