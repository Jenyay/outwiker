# -*- coding: utf-8 -*-

import os

import wx
import wx.lib.newevent

from outwiker.actions.search import (SearchAction,
                                     SearchNextAction,
                                     SearchPrevAction,
                                     SearchAndReplaceAction)
from outwiker.actions.polyactionsid import (SPELL_ON_OFF_ID,
                                            LINE_DUPLICATE_ID,
                                            MOVE_SELECTED_LINES_UP_ID,
                                            MOVE_SELECTED_LINES_DOWN_ID,
                                            DELETE_CURRENT_LINE,
                                            JOIN_LINES,
                                            DELETE_WORD_LEFT,
                                            DELETE_WORD_RIGHT,
                                            DELETE_LINE_LEFT,
                                            DELETE_LINE_RIGHT,
                                            GOTO_PREV_WORD,
                                            GOTO_NEXT_WORD,
                                            GOTO_PREV_WORD_SELECT,
                                            GOTO_NEXT_WORD_SELECT,
                                            GOTO_WORD_START,
                                            GOTO_WORD_END,
                                            CLIPBOARD_COPY_LINE,
                                            CLIPBOARD_CUT_LINE,
                                            CLIPBOARD_COPY_WORD,
                                            CLIPBOARD_CUT_WORD,
                                            )
from outwiker.core.system import getImagesDir
from outwiker.core.commands import MessageBox, pageExists, copyTextToClipboard
from outwiker.core.attachment import Attachment
from outwiker.core.config import IntegerOption
from outwiker.core.tree import RootWikiPage
from .basepagepanel import BasePagePanel
from .dialogs.buttonsdialog import ButtonsDialog
from .guiconfig import EditorConfig
from .defines import MENU_EDIT, TOOLBAR_GENERAL


class BaseTextPanel(BasePagePanel):
    """
    Базовый класс для представления текстовых страниц и им подобных
    (где есть текстовый редактор)
    """
    def __init__(self, parent, application):
        super(BaseTextPanel, self).__init__(parent, application)

        self._baseTextPolyactions = [
            SPELL_ON_OFF_ID,
            LINE_DUPLICATE_ID,
            MOVE_SELECTED_LINES_UP_ID,
            MOVE_SELECTED_LINES_DOWN_ID,
            DELETE_CURRENT_LINE,
            JOIN_LINES,
            DELETE_WORD_LEFT,
            DELETE_WORD_RIGHT,
            DELETE_LINE_LEFT,
            DELETE_LINE_RIGHT,
            GOTO_PREV_WORD,
            GOTO_NEXT_WORD,
            GOTO_PREV_WORD_SELECT,
            GOTO_NEXT_WORD_SELECT,
            GOTO_WORD_START,
            GOTO_WORD_END,
            CLIPBOARD_COPY_LINE,
            CLIPBOARD_CUT_LINE,
            CLIPBOARD_COPY_WORD,
            CLIPBOARD_CUT_WORD,
        ]

        self.searchMenu = None

        # Added in outwiker.gui 1.2
        self.wordMenu = None
        self.wordMenuItem = None

        # Added in outwiker.gui 1.2
        self.linesMenu = None
        self.linesMenuItem = None

        # Предыдущее сохраненное состояние.
        # Используется для выявления изменения страницы внешними средствами
        self._oldContent = None

        # Диалог, который показывается, если страница изменена
        # сторонними программами.
        # Используется для проверки того, что диалог уже показан и
        # еще раз его показывать не надо
        self.externalEditDialog = None

        # List of the tuples: (menu, MenuItem)
        self._menuSeparators = []

        self.searchMenuIndex = 2
        self.imagesDir = getImagesDir()

        self._spellOnOffEvent, self.EVT_SPELL_ON_OFF = wx.lib.newevent.NewEvent()

        self._addSearchTools()
        self._addSpellTools()

        editMenu = self._application.mainWindow.menuController[MENU_EDIT]
        sepMenuItem = editMenu.AppendSeparator()
        self._menuSeparators.append((editMenu, sepMenuItem))

        self._addWordTools()
        self._addLinesTools()

        self._application.onAttachmentPaste += self.onAttachmentPaste
        self._application.onPreferencesDialogClose += self.onPreferencesDialogClose

        self._onSetPage += self.__onSetPage

    def GetContentFromGui(self):
        """
        Получить из интерфейса контент, который будет сохранен в файл
        __page.text
        """
        pass

    def GetSearchPanel(self):
        """
        Вернуть панель поиска
        """
        pass

    def SetCursorPosition(self, position):
        """
        Установить курсор в текстовом редакторе в положение position
        """
        pass

    def GetCursorPosition(self):
        """
        Возвращает положение курсора в текстовом редакторе
        """
        pass

    def GetEditor(self):
        """
        Return text editor from panel. It used for common polyactions.
        """
        pass

    def __onSetPage(self, page):
        self.__updateOldContent()

    def __updateOldContent(self):
        self._oldContent = self.page.content

    def onPreferencesDialogClose(self, prefDialog):
        pass

    def Save(self):
        """
        Сохранить страницу
        """
        if self.page is None:
            return

        if not pageExists(self.page):
            return

        if not self.page.isRemoved:
            self.checkForExternalEditAndSave()

    def checkForExternalEditAndSave(self):
        """
        Проверить, что страница не изменена внешними средствами
        """
        if(self._oldContent is not None and
                self._oldContent != self.page.content):
            # Старое содержимое не совпадает с содержимым страницы.
            # Значит содержимое страницы кто-то изменил
            self.__externalEdit()
        else:
            self._savePageContent(self.page)
            self.__updateOldContent()

    def __externalEdit(self):
        """
        Спросить у пользователя, что делать, если страница изменилась
        внешними средствами
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

    def __showExternalEditDialog(self):
        """
        Показать диалог о том, что страница изменена сторонними программами и
        вернуть результат диалога:
            0 - перезаписать
            1 - перезагрузить
            2 - ничего не делать
        """
        buttons = [_(u"Overwrite"), _("Load"), _("Cancel")]

        message = _(u'Page "%s" is changed by the external program') % self.page.title
        self.externalEditDialog = ButtonsDialog(self,
                                                message,
                                                _(u"Owerwrite?"),
                                                buttons,
                                                default=0,
                                                cancel=2)

        result = self.externalEditDialog.ShowModal()
        self.externalEditDialog.Destroy()
        self.externalEditDialog = None

        return result

    def __stringsAreEqual(self, str1, str2):
        """
        Сравнение двух строк
        """
        return str1.replace("\r\n", "\n") == str2.replace("\r\n", "\n")

    def _savePageContent(self, page):
        """
        Сохранение содержимого страницы
        """
        if page is None or page.isRemoved or page.readonly:
            return

        try:
            self._getCursorPositionOption(page).value = self.GetCursorPosition()
        except IOError as e:
            MessageBox(_(u"Can't save file %s") % (str(e.filename)),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)
            return

        newContent = self.GetContentFromGui()
        if self.__stringsAreEqual(page.content, newContent):
            return

        try:
            page.content = newContent
        except IOError as e:
            # TODO: Проверить под Windows
            MessageBox(_(u"Can't save file %s") % (str(e.filename)),
                       _(u"Error"),
                       wx.ICON_ERROR | wx.OK)

    def _getCursorPositionOption(self, page):
        section = RootWikiPage.sectionGeneral
        cursor_section = u"CursorPosition"
        default = 0

        return IntegerOption(page.params,
                             section,
                             cursor_section,
                             default)

    def _getAttachString(self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при
        вставке выбранных прикрепленных файлов из панели вложений
        """
        text = ""
        count = len(fnames)

        for n in range(count):
            text += Attachment.attachDir + "/" + fnames[n]
            if n != count - 1:
                text += "\n"

        return text

    def Clear(self):
        """
        Убрать за собой
        """

        actionController = self._application.actionController
        [actionController.getAction(item).setFunc(None)
         for item
         in self._baseTextPolyactions]

        self._application.onAttachmentPaste -= self.onAttachmentPaste
        self._application.onPreferencesDialogClose -= self.onPreferencesDialogClose
        self._onSetPage -= self.__onSetPage

        self.removeGui()
        super(BaseTextPanel, self).Clear()

    def removeGui(self):
        """
        Убрать за собой элементы управления
        """
        assert self.mainWindow is not None
        assert self.searchMenu is not None

        mainMenu = self._application.mainWindow.menuController.getRootMenu()
        assert mainMenu.GetMenuCount() >= 3

        actionController = self._application.actionController
        [actionController.removeMenuItem(item)
         for item
         in self._baseTextPolyactions]

        actionController.removeMenuItem(SearchAction.stringId)
        actionController.removeMenuItem(SearchAndReplaceAction.stringId)
        actionController.removeMenuItem(SearchNextAction.stringId)
        actionController.removeMenuItem(SearchPrevAction.stringId)

        if TOOLBAR_GENERAL in self.mainWindow.toolbars:
            actionController.removeToolbarButton(SearchAction.stringId)
            actionController.removeToolbarButton(SearchAndReplaceAction.stringId)
            actionController.removeToolbarButton(SearchNextAction.stringId)
            actionController.removeToolbarButton(SearchPrevAction.stringId)
            actionController.removeToolbarButton(SPELL_ON_OFF_ID)

        self._removeAllTools()

        mainMenu.Remove(self.searchMenuIndex)
        editMenu = self._application.mainWindow.menuController[MENU_EDIT]
        editMenu.Remove(self.wordMenuItem)
        editMenu.Remove(self.linesMenuItem)

        [item[0].Remove(item[1]) for item in self._menuSeparators]

        self.searchMenu = None
        self.wordMenuItem = None
        self.wordMenu = None
        self.linesMenuItem = None
        self.linesMenu = None
        self._menuSeparators = []

    def onAttachmentPaste(self, fnames):
        """
        Пользователь хочет вставить ссылки на приаттаченные файлы
        """
        pass

    def _addSearchTools(self):
        assert self.mainWindow is not None
        self.searchMenu = wx.Menu()
        mainMenu = self._application.mainWindow.menuController.getRootMenu()
        mainMenu.Insert(self.searchMenuIndex, self.searchMenu, _("Search"))

        toolbar = self.mainWindow.toolbars[TOOLBAR_GENERAL]

        # Начать поиск на странице
        self._application.actionController.appendMenuItem(SearchAction.stringId, self.searchMenu)
        self._application.actionController.appendToolbarButton(
            SearchAction.stringId,
            toolbar,
            os.path.join(self.imagesDir, "local_search.png"),
            fullUpdate=False)

        # Начать поиск и замену на странице
        self._application.actionController.appendMenuItem(
            SearchAndReplaceAction.stringId,
            self.searchMenu)

        self._application.actionController.appendToolbarButton(
            SearchAndReplaceAction.stringId,
            toolbar,
            os.path.join(self.imagesDir, "local_replace.png"),
            fullUpdate=False)

        # Продолжить поиск вперед на странице
        self._application.actionController.appendMenuItem(
            SearchNextAction.stringId,
            self.searchMenu)

        # Продолжить поиск назад на странице
        self._application.actionController.appendMenuItem(
            SearchPrevAction.stringId,
            self.searchMenu)

    def _addSpellTools(self):
        generalToolbar = self.mainWindow.toolbars[TOOLBAR_GENERAL]
        editMenu = self._application.mainWindow.menuController[MENU_EDIT]
        self._application.actionController.getAction(SPELL_ON_OFF_ID).setFunc(self._spellOnOff)

        self._application.actionController.appendMenuCheckItem(SPELL_ON_OFF_ID,
                                                               editMenu)

        self._application.actionController.appendToolbarCheckButton(
            SPELL_ON_OFF_ID,
            generalToolbar,
            os.path.join(self.imagesDir, "spellcheck.png"),
            fullUpdate=False
        )

        enableSpell = EditorConfig(self._application.config).spellEnabled.value
        self._application.actionController.check(SPELL_ON_OFF_ID, enableSpell)

    def _addWordTools(self):
        self.wordMenu = wx.Menu()

        # Copy word to clipboard
        self._application.actionController.getAction(CLIPBOARD_COPY_WORD).setFunc(self._copyCurrentWordToClipboard)

        self._application.actionController.appendMenuItem(
            CLIPBOARD_COPY_WORD,
            self.wordMenu
        )

        # Cut word to clipboard
        self._application.actionController.getAction(CLIPBOARD_CUT_WORD).setFunc(self._cutCurrentWordToClipboard)

        self._application.actionController.appendMenuItem(
            CLIPBOARD_CUT_WORD,
            self.wordMenu
        )

        # Delete word left
        self._application.actionController.getAction(DELETE_WORD_LEFT).setFunc(lambda params: self.GetEditor().DelWordLeft())

        self._application.actionController.appendMenuItem(
            DELETE_WORD_LEFT,
            self.wordMenu
        )

        # Delete word right
        self._application.actionController.getAction(DELETE_WORD_RIGHT).setFunc(lambda params: self.GetEditor().DelWordRight())

        self._application.actionController.appendMenuItem(
            DELETE_WORD_RIGHT,
            self.wordMenu
        )

        self.wordMenu.AppendSeparator()

        # Go to start of the current word
        self._application.actionController.getAction(GOTO_WORD_START).setFunc(lambda params: self.GetEditor().GotoWordStart())

        self._application.actionController.appendMenuItem(
            GOTO_WORD_START,
            self.wordMenu
        )

        # Go to end of the current word
        self._application.actionController.getAction(GOTO_WORD_END).setFunc(lambda params: self.GetEditor().GotoWordEnd())

        self._application.actionController.appendMenuItem(
            GOTO_WORD_END,
            self.wordMenu
        )

        # Go to previous word
        self._application.actionController.getAction(GOTO_PREV_WORD).setFunc(lambda params: self.GetEditor().WordLeft())

        self._application.actionController.appendMenuItem(
            GOTO_PREV_WORD,
            self.wordMenu
        )

        # Go to next word
        self._application.actionController.getAction(GOTO_NEXT_WORD).setFunc(lambda params: self.GetEditor().WordRight())

        self._application.actionController.appendMenuItem(
            GOTO_NEXT_WORD,
            self.wordMenu
        )

        # Go to previous word and select
        self._application.actionController.getAction(GOTO_PREV_WORD_SELECT).setFunc(lambda params: self.GetEditor().WordLeftExtend())

        self._application.actionController.appendMenuItem(
            GOTO_PREV_WORD_SELECT,
            self.wordMenu
        )

        # Go to next word and select
        self._application.actionController.getAction(GOTO_NEXT_WORD_SELECT).setFunc(lambda params: self.GetEditor().WordRightExtend())

        self._application.actionController.appendMenuItem(
            GOTO_NEXT_WORD_SELECT,
            self.wordMenu
        )

        editMenu = self._application.mainWindow.menuController[MENU_EDIT]
        self.wordMenuItem = editMenu.AppendSubMenu(self.wordMenu, _(u'Word'))

    def _addLinesTools(self):
        self.linesMenu = wx.Menu()

        # Copy the current line to clipboard
        self._application.actionController.getAction(CLIPBOARD_COPY_LINE).setFunc(self._copyCurrentLineToClipboard)

        self._application.actionController.appendMenuItem(
            CLIPBOARD_COPY_LINE,
            self.linesMenu
        )

        # Cut the current line to clipboard
        self._application.actionController.getAction(CLIPBOARD_CUT_LINE).setFunc(self._cutCurrentLineToClipboard)

        self._application.actionController.appendMenuItem(
            CLIPBOARD_CUT_LINE,
            self.linesMenu
        )

        # Delete the current line line
        self._application.actionController.getAction(DELETE_CURRENT_LINE).setFunc(lambda params: self.GetEditor().LineDelete())

        self._application.actionController.appendMenuItem(
            DELETE_CURRENT_LINE,
            self.linesMenu
        )

        # Duplicate the current line
        self._application.actionController.getAction(LINE_DUPLICATE_ID).setFunc(lambda params: self.GetEditor().LineDuplicate())

        self._application.actionController.appendMenuItem(
            LINE_DUPLICATE_ID,
            self.linesMenu
        )

        # Move selected lines up
        self._application.actionController.getAction(MOVE_SELECTED_LINES_UP_ID).setFunc(lambda params: self.GetEditor().MoveSelectedLinesUp())

        self._application.actionController.appendMenuItem(
            MOVE_SELECTED_LINES_UP_ID,
            self.linesMenu
        )

        # Move selected lines down
        self._application.actionController.getAction(MOVE_SELECTED_LINES_DOWN_ID).setFunc(lambda params: self.GetEditor().MoveSelectedLinesDown())

        self._application.actionController.appendMenuItem(
            MOVE_SELECTED_LINES_DOWN_ID,
            self.linesMenu
        )

        # Join Lines
        self._application.actionController.getAction(JOIN_LINES).setFunc(lambda params: self.GetEditor().JoinLines())

        self._application.actionController.appendMenuItem(
            JOIN_LINES,
            self.linesMenu
        )

        # Delete line to start
        self._application.actionController.getAction(DELETE_LINE_LEFT).setFunc(lambda params: self.GetEditor().DelLineLeft())

        self._application.actionController.appendMenuItem(
            DELETE_LINE_LEFT,
            self.linesMenu
        )

        # Delete line to end
        self._application.actionController.getAction(DELETE_LINE_RIGHT).setFunc(lambda params: self.GetEditor().DelLineRight())

        self._application.actionController.appendMenuItem(
            DELETE_LINE_RIGHT,
            self.linesMenu
        )

        editMenu = self._application.mainWindow.menuController[MENU_EDIT]
        self.linesMenuItem = editMenu.AppendSubMenu(self.linesMenu,
                                                    _(u'Lines'))

    def _spellOnOff(self, checked):
        EditorConfig(self._application.config).spellEnabled.value = checked
        event = self._spellOnOffEvent(checked=checked)
        wx.PostEvent(self, event)

    def _copyCurrentLineToClipboard(self, params):
        editor = self.GetEditor()
        line = editor.GetCurrentLine()
        text = editor.GetLine(line)
        copyTextToClipboard(text)

    def _cutCurrentLineToClipboard(self, params):
        editor = self.GetEditor()
        line = editor.GetCurrentLine()
        text = editor.GetLine(line)
        editor.LineDelete()
        copyTextToClipboard(text)

    def _copyCurrentWordToClipboard(self, params):
        editor = self.GetEditor()
        pos = editor.GetCurrentPosition()
        word = editor.GetWord(pos)
        copyTextToClipboard(word)

    def _cutCurrentWordToClipboard(self, params):
        editor = self.GetEditor()
        self._copyCurrentWordToClipboard(params)
        pos = editor.GetCurrentPosition()

        word_start = editor.WordStartPosition(pos)
        word_end = editor.WordEndPosition(pos)
        editor.SetSelection(word_start, word_end)
        editor.replaceText(u'')

    def SetFocus(self):
        self.GetEditor().SetFocus()
