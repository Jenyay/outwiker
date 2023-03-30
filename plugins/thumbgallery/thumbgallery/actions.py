# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

import wx

from outwiker.api.core.attachment import Attachment
from outwiker.api.gui.actions import BaseAction

from .thumbdialog import ThumbDialog
from .i18n import get_


class ThumbAction(BaseAction):
    """
    Описание действия
    """

    stringId = "Thumbgallery_thumblist"

    def __init__(self, application):
        self._application = application
        global _
        _ = get_()

    @property
    def title(self):
        return _("Gallery (:thumbgallery:)")

    @property
    def description(self):
        return _("Insert (:thumbgallery:) wiki command to create the gallery.")

    def run(self, params):
        with ThumbDialog(
            self._application.mainWindow,
            self._application.selectedPage,
            self._application,
        ) as dlg:
            dlgResult = dlg.ShowModal()

            if dlgResult == wx.ID_OK:
                self._insertSelectedGallery(
                    dlg.columnsCount, dlg.thumbSize, dlg.selectedFiles
                )

    def _insertSelectedGallery(self, columns: int, thumbsize: int, files: List[Path]):
        """
        Вставить в редактор шаблон для галереи,
            оформленной в виде таблицы с заданным количеством столбцов.
        columns - количество столбцов
        thumbsize - размер превьюшек(0 - размер по умолчанию)
        files - список файлов для галереи
        """
        page = self._application.selectedPage
        attach = Attachment(page)
        attach_root = attach.getAttachPath(create=False)

        params = self._getGalleryParams(columns, thumbsize)

        attachFiles = [
            '    Attach:"{}"'.format(fname.relative_to(attach_root)).replace("\\", "/")
            for fname in files
        ]

        filesString = "\n".join(attachFiles)

        command = "(:thumbgallery{params}:)\n{files}\n(:thumbgalleryend:)".format(
            params=params, files=filesString
        )

        pageView = self._getPageView()
        pageView.codeEditor.replaceText(command)

    def _insertFullGallery(self, columns, thumbsize):
        """
        Вставить галерею из всех прикрепленных картинок
        thumbsize - размер превьюшек(0 - размер по умолчанию)
        """
        params = self._getGalleryParams(columns, thumbsize)

        command = "(:thumbgallery{params}:)".format(params=params)

        pageView = self._getPageView()
        pageView.codeEditor.replaceText(command)

    def _getGalleryParams(self, columns, thumbsize):
        result = ""
        if columns > 0:
            result += " cols={columns}".format(columns=columns)

        if thumbsize > 0:
            result += " px={size}".format(size=thumbsize)

        result = result.strip()
        if len(result) > 0:
            result = " " + result

        return result

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView
