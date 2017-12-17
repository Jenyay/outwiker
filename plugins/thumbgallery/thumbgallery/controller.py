# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.system import getOS

from .thumblistcommand import ThumbListCommand
from .thumbgallerycommand import ThumbGalleryCommand
from .thumbdialog import ThumbDialog


class Controller (object):
    """
    Основные действия плагина собраны в этом классе
    """
    def __init__ (self, application):
        self.THUMBLIST_TOOL_ID = u"PLUGIN_THUMBLIST_TOOL_ID"
        self._application = application


    def __onWikiParserPrepare (self, parser):
        parser.addCommand (ThumbListCommand (parser))
        parser.addCommand (ThumbGalleryCommand (parser))


    def initialize (self, lang):
        global _
        _ = lang
        self._application.onWikiParserPrepare += self.__onWikiParserPrepare
        self._application.onPageViewCreate += self.__onPageViewCreate

        if self._isCurrentWikiPage:
            self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
        self._application.onPageViewCreate -= self.__onPageViewCreate

        if self._isCurrentWikiPage:
            self._getPageView().removeTool (self.THUMBLIST_TOOL_ID)


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if not self._isCurrentWikiPage:
            return

        pageView = self._getPageView()

        helpString = _(u"Thumbnails Gallery (:thumbgallery:)")

        pageView.addTool (pageView.commandsMenu,
                          self.THUMBLIST_TOOL_ID,
                          self._onInsertCommand,
                          helpString,
                          helpString,
                          self._getImagePath (u"gallery.png"),
                          False)


    def _onInsertCommand (self, event):
        """
        Событие при нажатии на кнопку вставки галереи
        """
        dlg = ThumbDialog (self._application.mainWindow,
                           self._application.selectedPage,
                           _,
                           self._application)

        # Вручную задизаблим главное окно из-за глюка под Linux,
        # где главное окно становится активным, если есть полоса прокрутки
        # в контроле CheckListBox
        self._application.mainWindow.Disable()
        dlgResult = dlg.ShowModal()
        self._application.mainWindow.Enable()
        self._application.mainWindow.Raise()

        if dlgResult == wx.ID_OK:
            if dlg.isAllFiles:
                self._insertFullGallery (dlg.columnsCount, dlg.thumbSize)
            else:
                self._insertSelectedGallery (dlg.columnsCount, dlg.thumbSize, dlg.selectedFiles)

        dlg.Destroy()


    def _insertSelectedGallery (self, columns, thumbsize, files):
        """
        Вставить в редактор шаблон для галереи, оформленной в виде таблицы с заданным количеством столбцов.
        columns - количество столбцов
        thumbsize - размер превьюшек (0 - размер по умолчанию)
        files - список файлов для галереи
        """
        params = self._getGalleryParams (columns, thumbsize)

        attachFiles = ["    Attach:" + fname for fname in files]
        filesString = u"\n".join (attachFiles)

        command = u'(:thumbgallery{params}:)\n{files}\n(:thumbgalleryend:)'.format (params=params, files=filesString)

        pageView = self._getPageView()
        pageView.codeEditor.replaceText (command)


    def _insertFullGallery (self, columns, thumbsize):
        """
        Вставить галерею из всех прикрепленных картинок
        thumbsize - размер превьюшек (0 - размер по умолчанию)
        """
        params = self._getGalleryParams (columns, thumbsize)

        command = u'(:thumbgallery{params}:)'.format (params=params)

        pageView = self._getPageView()
        pageView.codeEditor.replaceText (command)


    def _getGalleryParams (self, columns, thumbsize):
        result = u""
        if columns > 0:
            result += u" cols={columns}".format (columns=columns)

        if thumbsize > 0:
            result += u" px={size}".format (size=thumbsize)

        result = result.strip()
        if len (result) > 0:
            result = " " + result

        return result


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView


    def _getImagePath (self, fname):
        imagedir = str(os.path.join (os.path.dirname (__file__), "images"))
        return os.path.join (imagedir, fname)


    @property
    def _isCurrentWikiPage (self):
        return (self._application.selectedPage is not None and
                self._application.selectedPage.getTypeString() == u"wiki")
