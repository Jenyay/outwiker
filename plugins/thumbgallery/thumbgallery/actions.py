# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction

from .thumbdialog import ThumbDialog
from .i18n import get_


class ThumbAction (BaseAction):
    """
    Описание действия
    """
    stringId = u"Thumbgallery_thumblist"

    def __init__(self, application):
        self._application = application
        global _
        _ = get_()

    @property
    def title(self):
        return _(u"Insert gallery (:thumbgallery:)")

    @property
    def description(self):
        return _(u"Insert (:thumbgallery:) wiki command to create the gallery.")

    def run(self, params):
        with ThumbDialog(self._application.mainWindow,
                         self._application.selectedPage,
                         self._application) as dlg:

            dlgResult = dlg.ShowModal()

            if dlgResult == wx.ID_OK:
                if dlg.isAllFiles:
                    self._insertFullGallery(dlg.columnsCount, dlg.thumbSize)
                else:
                    self._insertSelectedGallery(dlg.columnsCount,
                                                dlg.thumbSize,
                                                dlg.selectedFiles)

    def _insertSelectedGallery(self, columns, thumbsize, files):
        """
        Вставить в редактор шаблон для галереи,
            оформленной в виде таблицы с заданным количеством столбцов.
        columns - количество столбцов
        thumbsize - размер превьюшек(0 - размер по умолчанию)
        files - список файлов для галереи
        """
        params = self._getGalleryParams(columns, thumbsize)

        attachFiles = ["    Attach:" + fname for fname in files]
        filesString = u"\n".join(attachFiles)

        command = u'(:thumbgallery{params}:)\n{files}\n(:thumbgalleryend:)'.format(params=params, files=filesString)

        pageView = self._getPageView()
        pageView.codeEditor.replaceText(command)

    def _insertFullGallery(self, columns, thumbsize):
        """
        Вставить галерею из всех прикрепленных картинок
        thumbsize - размер превьюшек(0 - размер по умолчанию)
        """
        params = self._getGalleryParams(columns, thumbsize)

        command = u'(:thumbgallery{params}:)'.format(params=params)

        pageView = self._getPageView()
        pageView.codeEditor.replaceText(command)

    def _getGalleryParams(self, columns, thumbsize):
        result = u""
        if columns > 0:
            result += u" cols={columns}".format(columns=columns)

        if thumbsize > 0:
            result += u" px={size}".format(size=thumbsize)

        result = result.strip()
        if len(result) > 0:
            result = " " + result

        return result

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView
