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
        self._dialog.setPageTitle (self._page.title)
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
        Возвращает пустую строку, если newiud соответствует требованиям к идентификаторам.
        Возвращает строку с описанием ошибки, если что-то неверно.
        """
        otherpage = self._application.pageUidDepot[newiud]

        if (otherpage is not None and otherpage != self._page):
            return _(u"Same identifier exist already")

        regexp = re.compile (r"^[-\w,\$\.\+\!\*\(\):@|&=\?~\#\%]+$", re.I | re.U)
        match = regexp.match (newiud)

        if match is None:
            return _(u"Identifier contain invalid character")

        return u""
