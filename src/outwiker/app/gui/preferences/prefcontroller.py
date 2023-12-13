# -*- coding: utf-8 -*-

import wx

from outwiker.app.actions.openhelp import OpenHelpAction, OpenHelpParams

from outwiker.app.gui.preferences.generalpanel import GeneralPanel
from outwiker.app.gui.preferences.mainwindowpanel import MainWindowPanel
from outwiker.app.gui.preferences.traypanel import TrayPanel
from outwiker.app.gui.preferences.editorpanel import EditorPanel
from outwiker.app.gui.preferences.spellpanel import SpellPanel
from outwiker.app.gui.preferences.htmlrenderpanel import HtmlRenderPanel
from outwiker.app.gui.preferences.textprintpanel import TextPrintPanel
from outwiker.app.gui.preferences.pluginspanel import PluginsPanel
from outwiker.app.gui.preferences.hotkeyspanel import HotKeysPanel
from outwiker.app.gui.preferences.htmleditorpanel import HtmlEditorPanel
from outwiker.app.gui.preferences.wikieditorpanel import WikiEditorPanel
from outwiker.app.gui.preferences.iconsetpanel import IconsetPanel
from outwiker.app.gui.preferences.tagspanel import TagsPanel
from outwiker.app.gui.preferences.attachpanel import AttachPanel
from outwiker.app.gui.preferences.colorspanel import ColorsPanel
from outwiker.app.gui.preferences.formatspanel import FormatsPanel

from outwiker.core.event import (EVENT_PRIORITY_MAX_CORE,
                                 EVENT_PRIORITY_MIN_CORE)
from outwiker.core.exceptions import PreferencesException

from outwiker.gui.guiconfig import PrefDialogConfig
from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo


class PrefController:
    def __init__(self, application):
        self._application = application
        self._dialog = None

    def initialize(self):
        self._application.onPreferencesDialogCreate.bind(
            self._onPrefDialogCreateFirst,
            EVENT_PRIORITY_MAX_CORE
        )

        self._application.onPreferencesDialogCreate.bind(
            self._onPrefDialogCreateLast,
            EVENT_PRIORITY_MIN_CORE
        )

    def clear(self):
        self._application.onPreferencesDialogCreate -= self._onPrefDialogCreateFirst
        self._application.onPreferencesDialogCreate -= self._onPrefDialogCreateLast
        self._dialog = None

    def _onPrefDialogCreateFirst(self, dialog):
        self._dialog = dialog
        self._createInterfaceGroup()
        self._createEditorGroup()
        self._createIconsetPage()
        self._createPluginsPage()
        self._createTextPrintoutPage()

        self._dialog.Bind(wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)
        self._dialog.Bind(wx.EVT_BUTTON, self._onCancel, id=wx.ID_CANCEL)
        self._dialog.Bind(wx.EVT_BUTTON, self._onHelp, id=wx.ID_HELP)

    def _onPrefDialogCreateLast(self, dialog):
        self._expandAllPages()
        self._dialog.treeBook.SetSelection(0)

        self._loadAllOptions()
        self._setDialogPreperties()

    def _onCancel(self, event):
        self._cancelAll()
        self._dialog.EndModal(wx.ID_CANCEL)

    def _onOk(self, event):
        try:
            self._saveAll()
        except PreferencesException:
            pass

        self._saveDialogPreperties()
        self._application.onPreferencesDialogClose(self._dialog)
        self._dialog.EndModal(wx.ID_OK)

    def _onHelp(self, event):
        controller = self._application.actionController
        action = controller.getAction(OpenHelpAction.stringId)
        params = OpenHelpParams(u'page://settings')
        action.run(params)

    def _saveAll(self):
        """
        Сохранить настройки для всех страниц
        """
        for page in self._dialog.pages:
            page.Save()

    def _cancelAll(self):
        """
        Оповестить все панели о том, что пользователь нажал кнопку Cancel
        """
        for page in self._dialog.pages:
            page.Cancel()

    def _saveDialogPreperties(self):
        config = PrefDialogConfig(self._application.config)
        clientSize = self._dialog.GetClientSize()

        config.width.value = clientSize[0]
        config.height.value = clientSize[1]

    def _createInterfaceGroup(self):
        """
        Создать страницы с подгруппой "Interface"
        """
        generalPage = GeneralPanel(self._dialog.treeBook, self._application)
        mainWindowPage = MainWindowPanel(
            self._dialog.treeBook, self._application)
        colorsPage = ColorsPanel(self._dialog.treeBook, self._application)
        trayPage = TrayPanel(self._dialog.treeBook, self._application)
        htmlRenderPage = HtmlRenderPanel(
            self._dialog.treeBook, self._application)
        hotkeysPage = HotKeysPanel(self._dialog.treeBook, self._application)
        tagsPage = TagsPanel(self._dialog.treeBook, self._application)
        attachPage = AttachPanel(self._dialog.treeBook, self._application)
        formatsPage = FormatsPanel(self._dialog.treeBook, self._application)

        interfacePanelsList = [
            PreferencePanelInfo(generalPage, _("General")),
            PreferencePanelInfo(mainWindowPage, _("Main window")),
            PreferencePanelInfo(colorsPage, _("Colors")),
            PreferencePanelInfo(trayPage, _("Tray icon")),
            PreferencePanelInfo(htmlRenderPage, _("Preview")),
            PreferencePanelInfo(tagsPage, _("Tags cloud")),
            PreferencePanelInfo(attachPage, _("Attachments")),
            PreferencePanelInfo(hotkeysPage, _("Hotkeys")),
            PreferencePanelInfo(formatsPage, _("Formats")),
        ]

        self._dialog.appendPreferenceGroup(_("Interface"),
                                           interfacePanelsList)

    def _createEditorGroup(self):
        """
        Создать страницы с подгруппой "Редактор"
        """
        editorPage = EditorPanel(self._dialog.treeBook, self._application)
        spellPage = SpellPanel(self._dialog.treeBook, self._application)
        htmlEditorPage = HtmlEditorPanel(
            self._dialog.treeBook, self._application)
        wikiEditorPage = WikiEditorPanel(
            self._dialog.treeBook, self._application)

        editorPanesList = [
            PreferencePanelInfo(editorPage, _("General")),
            PreferencePanelInfo(spellPage, _("Spell checking")),
            PreferencePanelInfo(htmlEditorPage, _("HTML editor")),
            PreferencePanelInfo(wikiEditorPage, _("Wiki editor")),
        ]

        self._dialog.appendPreferenceGroup(_("Editor"), editorPanesList)

    def _createPluginsPage(self):
        pluginsPage = PluginsPanel(self._dialog.treeBook, self._application)
        self._dialog.treeBook.AddPage(pluginsPage, _("Plugins"))

    def _createTextPrintoutPage(self):
        textPrintPage = TextPrintPanel(
            self._dialog.treeBook, self._application)
        self._dialog.treeBook.AddPage(textPrintPage, _("Text printout"))

    def _createIconsetPage(self):
        iconsetPage = IconsetPanel(self._dialog.treeBook)
        self._dialog.treeBook.AddPage(iconsetPage, _("User's iconset"))

    def _setDialogPreperties(self):
        config = PrefDialogConfig(self._application.config)

        self._dialog.SetTitle(_("Preferences"))
        self._dialog.treeBook.SetMinSize((300, -1))

        self._dialog.Fit()
        fitWidth, fitHeight = self._dialog.GetSize()
        self._dialog.SetMinSize((fitWidth, fitHeight))
        self._dialog.SetClientSize((config.width.value, config.height.value))
        self._centerDialog()

    def _centerDialog(self):
        """
        Расположить окно по центру родителя
        """
        selfWidth, selfHeight = self._dialog.GetSize()

        parentWidth, parentHeight = self._dialog.GetParent().GetSize()
        parentX, parentY = self._dialog.GetParent().GetPosition()

        posX = parentX + (parentWidth - selfWidth) / 2
        posY = parentY + (parentHeight - selfHeight) / 2

        self._dialog.SetPosition((posX, posY))

    def _loadAllOptions(self):
        """
        Загрузить настройки для всех страниц
        """
        for pageIndex in range(self._dialog.treeBook.GetPageCount()):
            page = self._dialog.treeBook.GetPage(pageIndex)
            page.LoadState()

    def _expandAllPages(self):
        """
        Развернуть все узлы в дереве настроек
        """
        for pageindex in range(self._dialog.treeBook.GetPageCount()):
            self._dialog.treeBook.ExpandNode(pageindex)
