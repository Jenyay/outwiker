#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx

import outwiker.core.system
from outwiker.core.commands import MessageBox, openWiki, pageExists
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.gui.buttonsdialog import ButtonsDialog
from .basepagepanel import BasePagePanel


class BaseTextPanel (BasePagePanel):
    """
    Базовый класс для представления текстовых страниц и им подобных (где есть текстовый редактор)
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def GetContentFromGui(self):
        """
        Получить из интерфейса контент, который будет сохранен в файл __page.text
        """
        pass


    @abstractmethod
    def GetSearchPanel (self):
        """
        Вернуть панель поиска
        """
        pass

    
    def __init__ (self, parent, *args, **kwds):
        BasePagePanel.__init__ (self, parent, *args, **kwds)

        self.mainWindow = Application.mainWindow
        self.searchMenu = None

        # Предыдущее сохраненное состояние. 
        # Используется для выявления изменения страницы внешними средствами
        self._oldContent = None

        # Диалог, который показывается, если страница изменена сторонними программами.
        # Используется для проверки того, что диалог уже показан и еще раз его показывать не надо
        self.externalEditDialog = None

        self.ID_SEARCH = wx.NewId()
        self.ID_SEARCH_NEXT = wx.NewId()
        self.ID_SEARCH_PREV = wx.NewId()

        self.searchMenuIndex = 2
        self.imagesDir = outwiker.core.system.getImagesDir()

        self._addMenuItems ()
        self._addToolsItems ()

        Application.onAttachmentPaste += self.onAttachmentPaste
        Application.onPreferencesDialogClose += self.onPreferencesDialogClose
        # Application.onPageUpdate += self.onPageUpdate

        self._onSetPage += self.__onSetPage


    # def onPageUpdate (self, page):
    #     print "qqq"
    #     if page == Application.selectedPage:
    #         self.UpdateView(page)


    def __onSetPage (self, page):
        self.__updateOldContent()


    def __updateOldContent (self):
        self._oldContent = self.page.content


    def onPreferencesDialogClose (self, prefDialog):
        pass
    

    def Save (self):
        """
        Сохранить страницу
        """
        if self.page == None:
            return

        if not pageExists (self.page):
            return

        if not self.page.isRemoved:
            self.checkForExternalEditAndSave()


    def checkForExternalEditAndSave (self):
        """
        Проверить, что страница не изменена внешними средствами
        """
        if self._oldContent != None and self._oldContent != self.page.content:
            # Старое содержимое не совпадает с содержимым страницы.
            # Значит содержимое страницы кто-то изменил
            self.__externalEdit()
        else:
            self._savePageContent(self.page)
            self.__updateOldContent()


    def __externalEdit (self):
        """
        Спросить у пользователя, что делать, если страница изменилась внешними средствами
        """
        if self.externalEditDialog == None:
            result = self.__showExternalEditDialog()

            if result == 0:
                # Перезаписать
                self._savePageContent(self.page)
                self.__updateOldContent()
            elif result == 1:
                # Перезагрузить
                self.__updateOldContent()
                self.UpdateView(self.page)

    
    def __showExternalEditDialog (self):
        """
        Показать диалог о том, что страница изменена сторонними программами и вернуть результат диалога:
        0 - перезаписать
        1 - перезагрузить
        2 - ничего не делать
        """
        buttons = [_(u"Overwrite"), _("Load"), _("Cancel")]

        message = _(u'Page "%s" is changed by the external program') % self.page.title
        self.externalEditDialog = ButtonsDialog (self, 
                message,
                _(u"Owerwrite?"),
                buttons,
                default = 0,
                cancel = 2)
        
        result = self.externalEditDialog.ShowModal()
        self.externalEditDialog.Destroy()
        self.externalEditDialog = None

        return result


    def __stringsAreEqual (self, str1, str2):
        """
        Сравнение двух строк
        """
        return str1.replace ("\r\n", "\n") == str2.replace ("\r\n", "\n")


    def _savePageContent (self, page):
        """
        Сохранение содержимого страницы
        """
        if (page != None and 
                not page.isRemoved and 
                not page.readonly and
                not self.__stringsAreEqual (page.content, self.GetContentFromGui() ) ):

            try:
                page.content = self.GetContentFromGui()
            except IOError as e:
                # TODO: Проверить под Windows
                MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)
    

    def _getAttachString (self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений
        """
        text = ""
        count = len (fnames)

        for n in range (count):
            text += Attachment.attachDir + "/" + fnames[n]
            if n != count -1:
                text += "\n"

        return text

    
    def Clear (self):
        """
        Убрать за собой
        """
        Application.onAttachmentPaste -= self.onAttachmentPaste
        Application.onPreferencesDialogClose -= self.onPreferencesDialogClose
        self._onSetPage -= self.__onSetPage

        self.removeGui()


    def removeGui (self):
        """
        Убрать за собой элементы управления
        """
        assert self.mainWindow != None
        assert self.mainWindow.mainMenu.GetMenuCount() >= 3
        assert self.searchMenu != None

        #import traceback
        #traceback.print_stack()
        #print 

        self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH)
        self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH_NEXT)
        self.mainWindow.Unbind(wx.EVT_MENU, id=self.ID_SEARCH_PREV)

        self.mainWindow.mainMenu.Remove (self.searchMenuIndex)
        self.searchMenu = None

        self.mainWindow.mainToolbar.DeleteTool (self.ID_SEARCH)

    
    def _addMenuItems (self):
        """
        Добавить пункты меню
        """
        assert self.mainWindow != None

        self.searchMenu = wx.Menu()

        self.searchMenu.Append (self.ID_SEARCH, _(u"Search…\tCtrl+F"), "", wx.ITEM_NORMAL)
        self.searchMenu.Append (self.ID_SEARCH_NEXT, _(u"Find next\tF3"), "", wx.ITEM_NORMAL)
        self.searchMenu.Append (self.ID_SEARCH_PREV, _(u"Find previous\tShift+F3"), "", wx.ITEM_NORMAL)
        
        self.mainWindow.mainMenu.Insert (self.searchMenuIndex, self.searchMenu, _("&Search") )

        self.mainWindow.Bind(wx.EVT_MENU, self.onSearch, id=self.ID_SEARCH)
        self.mainWindow.Bind(wx.EVT_MENU, self.onSearchNext, id=self.ID_SEARCH_NEXT)
        self.mainWindow.Bind(wx.EVT_MENU, self.onSearchPrev, id=self.ID_SEARCH_PREV)
    

    def _addToolsItems (self):
        self.mainWindow.mainToolbar.AddLabelTool(self.ID_SEARCH, 
                _(u"Search"),
                wx.Bitmap(os.path.join (self.imagesDir, "local_search.png"), wx.BITMAP_TYPE_ANY), 
                wx.NullBitmap, 
                wx.ITEM_NORMAL, 
                _(u"Search"),
                "")

        self.mainWindow.mainToolbar.Realize()
    

    def _showSearchPanel (self, panel):
        if not panel.IsShown():
            panel.Show()
            panel.GetParent().Layout()


    def onSearch (self, event):
        panel = self.GetSearchPanel()
        if panel != None:
            self._showSearchPanel (panel)
            panel.startSearch()


    def onSearchNext (self, event):
        panel = self.GetSearchPanel()
        if panel != None:
            self._showSearchPanel (panel)
            panel.nextSearch()


    def onSearchPrev (self, event):
        panel = self.GetSearchPanel()
        if panel != None:
            self._showSearchPanel (panel)
            panel.prevSearch()
