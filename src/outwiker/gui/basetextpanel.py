# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx
import wx.lib.newevent

from outwiker.actions.search import SearchAction, SearchNextAction, SearchPrevAction, SearchAndReplaceAction
from outwiker.actions.polyactionsid import (SPELL_ON_OFF_ID,
                                            LINE_DUPLICATE_ID,
                                            MOVE_SELECTED_LINES_UP_ID,
                                            MOVE_SELECTED_LINES_DOWN_ID)
from outwiker.core.system import getImagesDir
from outwiker.core.commands import MessageBox, pageExists
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.config import IntegerOption
from outwiker.core.tree import RootWikiPage
from outwiker.gui.basepagepanel import BasePagePanel
from outwiker.gui.buttonsdialog import ButtonsDialog
from outwiker.gui.guiconfig import EditorConfig


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

    @abstractmethod
    def SetCursorPosition (self, position):
        """
        Установить курсор в текстовом редакторе в положение position
        """
        pass

    @abstractmethod
    def GetCursorPosition (self):
        """
        Возвращает положение курсора в текстовом редакторе
        """
        pass

    @abstractmethod
    def _onLineDuplicate(self, params):
        """
        Handler for the LINE_DUPLICATE_ID polyaction
        """
        pass

    @abstractmethod
    def _onMoveSelectedLinesUp(self, params):
        """
        Handler for the MOVE_SELECTED_LINES_UP_ID polyaction
        """
        pass

    @abstractmethod
    def _onMoveSelectedLinesDown(self, params):
        """
        Handler for the MOVE_SELECTED_LINES_DOWN_ID polyaction
        """
        pass


    def __init__ (self, parent, *args, **kwds):
        super (BaseTextPanel, self).__init__ (parent, *args, **kwds)
        self._application = Application

        self.searchMenu = None

        # Предыдущее сохраненное состояние.
        # Используется для выявления изменения страницы внешними средствами
        self._oldContent = None

        # Диалог, который показывается, если страница изменена сторонними программами.
        # Используется для проверки того, что диалог уже показан и еще раз его показывать не надо
        self.externalEditDialog = None

        self.searchMenuIndex = 2
        self.imagesDir = getImagesDir()

        self._spellOnOffEvent, self.EVT_SPELL_ON_OFF = wx.lib.newevent.NewEvent()

        self._addSearchTools ()
        self._addSpellTools ()
        self._addEditTools ()

        self._application.onAttachmentPaste += self.onAttachmentPaste
        self._application.onPreferencesDialogClose += self.onPreferencesDialogClose

        self._onSetPage += self.__onSetPage


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
        if self.page is None:
            return

        if not pageExists (self.page):
            return

        if not self.page.isRemoved:
            self.checkForExternalEditAndSave()


    def checkForExternalEditAndSave (self):
        """
        Проверить, что страница не изменена внешними средствами
        """
        if self._oldContent is not None and self._oldContent != self.page.content:
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
        if self.externalEditDialog is None:
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
        if (page is None or
                page.isRemoved or
                page.readonly):
            return

        try:
            self._getCursorPositionOption(page).value = self.GetCursorPosition()
        except IOError, e:
            MessageBox (_(u"Can't save file %s") % (unicode (e.filename)),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return

        if self.__stringsAreEqual (page.content,
                                   self.GetContentFromGui()):
            return

        try:
            page.content = self.GetContentFromGui()
        except IOError, e:
            # TODO: Проверить под Windows
            MessageBox (_(u"Can't save file %s") % (unicode (e.filename)),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)


    def _getCursorPositionOption (self, page):
        section = RootWikiPage.sectionGeneral
        cursor_section = u"CursorPosition"
        default = 0

        return IntegerOption (page.params,
                              section,
                              cursor_section,
                              default)


    def _getAttachString (self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений
        """
        text = ""
        count = len (fnames)

        for n in range (count):
            text += Attachment.attachDir + "/" + fnames[n]
            if n != count - 1:
                text += "\n"

        return text


    def Clear (self):
        """
        Убрать за собой
        """
        self._application.actionController.getAction (SPELL_ON_OFF_ID).setFunc (None)
        self._application.actionController.getAction (LINE_DUPLICATE_ID).setFunc (None)
        self._application.actionController.getAction (MOVE_SELECTED_LINES_UP_ID).setFunc (None)
        self._application.actionController.getAction (MOVE_SELECTED_LINES_DOWN_ID).setFunc (None)

        self._application.onAttachmentPaste -= self.onAttachmentPaste
        self._application.onPreferencesDialogClose -= self.onPreferencesDialogClose
        self._onSetPage -= self.__onSetPage

        self.removeGui()
        super (BaseTextPanel, self).Clear()


    def removeGui (self):
        """
        Убрать за собой элементы управления
        """
        assert self.mainWindow is not None
        assert self.mainWindow.mainMenu.GetMenuCount() >= 3
        assert self.searchMenu is not None

        self._application.actionController.removeMenuItem (SearchAction.stringId)
        self._application.actionController.removeMenuItem (SearchAndReplaceAction.stringId)
        self._application.actionController.removeMenuItem (SearchNextAction.stringId)
        self._application.actionController.removeMenuItem (SearchPrevAction.stringId)
        self._application.actionController.removeMenuItem (SPELL_ON_OFF_ID)
        self._application.actionController.removeMenuItem (LINE_DUPLICATE_ID)
        self._application.actionController.removeMenuItem (MOVE_SELECTED_LINES_UP_ID)
        self._application.actionController.removeMenuItem (MOVE_SELECTED_LINES_DOWN_ID)

        if self.mainWindow.GENERAL_TOOLBAR_STR in self.mainWindow.toolbars:
            self._application.actionController.removeToolbarButton (SearchAction.stringId)
            self._application.actionController.removeToolbarButton (SearchAndReplaceAction.stringId)
            self._application.actionController.removeToolbarButton (SearchNextAction.stringId)
            self._application.actionController.removeToolbarButton (SearchPrevAction.stringId)
            self._application.actionController.removeToolbarButton (SPELL_ON_OFF_ID)

        self._removeAllTools()
        self.mainWindow.mainMenu.Remove (self.searchMenuIndex)
        self.searchMenu = None


    def _addSearchTools (self):
        assert self.mainWindow is not None
        self.searchMenu = wx.Menu()
        self.mainWindow.mainMenu.Insert (self.searchMenuIndex, self.searchMenu, _("Search"))

        toolbar = self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR]

        # Начать поиск на странице
        self._application.actionController.appendMenuItem (SearchAction.stringId, self.searchMenu)
        self._application.actionController.appendToolbarButton (SearchAction.stringId,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "local_search.png"),
                                                                fullUpdate=False)

        # Начать поиск и замену на странице
        self._application.actionController.appendMenuItem (SearchAndReplaceAction.stringId, self.searchMenu)
        self._application.actionController.appendToolbarButton (SearchAndReplaceAction.stringId,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "local_replace.png"),
                                                                fullUpdate=False)

        # Продолжить поиск вперед на странице
        self._application.actionController.appendMenuItem (SearchNextAction.stringId, self.searchMenu)

        # Продолжить поиск назад на странице
        self._application.actionController.appendMenuItem (SearchPrevAction.stringId, self.searchMenu)


    def _addSpellTools (self):
        generalToolbar = self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR]
        self._application.actionController.getAction (SPELL_ON_OFF_ID).setFunc (self._spellOnOff)

        self._application.actionController.appendMenuCheckItem (
            SPELL_ON_OFF_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        self._application.actionController.appendToolbarCheckButton (
            SPELL_ON_OFF_ID,
            generalToolbar,
            os.path.join (self.imagesDir, "spellcheck.png"),
            fullUpdate=False
        )

        enableSpell = EditorConfig (Application.config).spellEnabled.value
        self._application.actionController.check (SPELL_ON_OFF_ID, enableSpell)

    def _addEditTools (self):
        # Duplicate line
        self._application.actionController.getAction (LINE_DUPLICATE_ID).setFunc (self._onLineDuplicate)

        self._application.actionController.appendMenuItem (
            LINE_DUPLICATE_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Move selected lines up
        self._application.actionController.getAction (MOVE_SELECTED_LINES_UP_ID).setFunc (self._onMoveSelectedLinesUp)

        self._application.actionController.appendMenuItem (
            MOVE_SELECTED_LINES_UP_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

        # Move selected lines down
        self._application.actionController.getAction (MOVE_SELECTED_LINES_DOWN_ID).setFunc (self._onMoveSelectedLinesDown)

        self._application.actionController.appendMenuItem (
            MOVE_SELECTED_LINES_DOWN_ID,
            self._application.mainWindow.mainMenu.editMenu
        )

    def _spellOnOff (self, checked):
        EditorConfig (self._application.config).spellEnabled.value = checked

        event = self._spellOnOffEvent (checked=checked)
        wx.PostEvent (self, event)
