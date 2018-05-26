# -*- coding: UTF-8 -*-

import wx
import logging

from outwiker.actions.openhelp import OpenHelpAction, OpenHelpParams
from outwiker.core.event import (EVENT_PRIORITY_MAX_CORE,
                                 EVENT_PRIORITY_MIN_CORE)
from outwiker.core.exceptions import PreferencesException
from outwiker.gui.guiconfig import PrefDialogConfig

from .preferencepanelinfo import PreferencePanelInfo
from .generalpanel import GeneralPanel
from .traypanel import TrayPanel
from .editorpanel import EditorPanel
from .spellpanel import SpellPanel
from .htmlrenderpanel import HtmlRenderPanel
from .textprintpanel import TextPrintPanel
from .pluginspanel import PluginsPanel
from .hotkeyspanel import HotKeysPanel
from .htmleditorpanel import HtmlEditorPanel
from .wikieditorpanel import WikiEditorPanel
from .iconsetpanel import IconsetPanel
from .tagspanel import TagsPanel
from .attachpanel import AttachPanel


logger = logging.getLogger('prefcontroller')


class PrefController (object):
    def __init__(self, application):
        self._application = application
        self._dialog = None

    def initialize(self):
        self._application.onPreferencesDialogCreate.bind(
            self.__onPrefDialogCreateFirst,
            EVENT_PRIORITY_MAX_CORE
        )

        self._application.onPreferencesDialogCreate.bind(
            self.__onPrefDialogCreateLast,
            EVENT_PRIORITY_MIN_CORE
        )

    def clear(self):
        self._application.onPreferencesDialogCreate -= self.__onPrefDialogCreateFirst
        self._application.onPreferencesDialogCreate -= self.__onPrefDialogCreateLast
        self._dialog = None

    def __onPrefDialogCreateFirst(self, dialog):
        self._dialog = dialog
        self.__createInterfaceGroup()
        self.__createEditorGroup()
        self.__createIconsetPage()
        self.__createPluginsPage()

        self._dialog.Bind(wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)
        self._dialog.Bind(wx.EVT_BUTTON, self.__onCancel, id=wx.ID_CANCEL)
        self._dialog.Bind(wx.EVT_BUTTON, self.__onHelp, id=wx.ID_HELP)

    def __onPrefDialogCreateLast(self, dialog):
        self.__expandAllPages()
        self._dialog.treeBook.SetSelection(0)

        self.__loadAllOptions()
        self.__setDialogPreperties()

    def __unbindFromDialog(self):
        self._dialog.Unbind(wx.EVT_BUTTON,
                            handler=self.__onOk,
                            id=wx.ID_OK)

        self._dialog.Unbind(wx.EVT_BUTTON,
                            handler=self.__onCancel,
                            id=wx.ID_CANCEL)

        self._dialog.Unbind(wx.EVT_BUTTON,
                            handler=self.__onHelp,
                            id=wx.ID_HELP)

    def __onCancel(self, event):
        self._application.onPreferencesDialogClose(self)
        self.__Destroy()

    def __onOk(self, event):
        try:
            self.__saveAll()
        except PreferencesException:
            pass

        self.__saveDialogPreperties()
        self._application.onPreferencesDialogClose(self._dialog)
        self.__Destroy()

    def __Destroy(self):
        """
        Destroy Preference Dialog

        :return:
            None
        """
        self.__unbindFromDialog()
        self._dialog.EndModal(wx.ID_OK)
        self._dialog.treeBook.Destroy()
        self._dialog.Destroy()

    def __onHelp(self, event):
        controller = self._application.actionController
        action = controller.getAction(OpenHelpAction.stringId)
        params = OpenHelpParams(u'page://settings')
        action.run(params)

    def __saveAll(self):
        """
        Сохранить настройки для всех страниц
        """
        treeBook = self._dialog.treeBook

        for pageIndex in range(treeBook.GetPageCount()):
            page = treeBook.GetPage(pageIndex)
            page.Save()

    def __saveDialogPreperties(self):
        config = PrefDialogConfig(self._application.config)
        clientSize = self._dialog.GetClientSize()

        config.width.value = clientSize[0]
        config.height.value = clientSize[1]

    def __createInterfaceGroup(self):
        """
        Создать страницы с подгруппой "Interface"
        """
        generalPage = GeneralPanel(self._dialog.treeBook)
        trayPage = TrayPanel(self._dialog.treeBook)
        htmlRenderPage = HtmlRenderPanel(self._dialog.treeBook)
        textPrintPage = TextPrintPanel(self._dialog.treeBook)
        hotkeysPage = HotKeysPanel(self._dialog.treeBook)
        tagsPage = TagsPanel(self._dialog.treeBook)
        attachPage = AttachPanel(self._dialog.treeBook)

        interfacePanelsList = [
            PreferencePanelInfo(generalPage, _(u"General")),
            PreferencePanelInfo(trayPage, _(u"Tray icon")),
            PreferencePanelInfo(htmlRenderPage, _(u"Preview")),
            PreferencePanelInfo(tagsPage, _(u"Tags cloud")),
            PreferencePanelInfo(attachPage, _(u"Attachments")),
            PreferencePanelInfo(hotkeysPage, _(u"Hotkeys")),
            PreferencePanelInfo(textPrintPage, _(u"Text Printout")),
        ]

        self._dialog.appendPreferenceGroup(_(u"Interface"),
                                           interfacePanelsList)

    def __createEditorGroup(self):
        """
        Создать страницы с подгруппой "Редактор"
        """
        editorPage = EditorPanel(self._dialog.treeBook)
        spellPage = SpellPanel(self._dialog.treeBook)
        htmlEditorPage = HtmlEditorPanel(self._dialog.treeBook)
        wikiEditorPage = WikiEditorPanel(self._dialog.treeBook)

        editorPanesList = [
            PreferencePanelInfo(editorPage, _(u"General")),
            PreferencePanelInfo(spellPage, _(u"Spell checking")),
            PreferencePanelInfo(htmlEditorPage, _(u"HTML Editor")),
            PreferencePanelInfo(wikiEditorPage, _(u"Wiki Editor")),
        ]

        self._dialog.appendPreferenceGroup(_(u"Editor"), editorPanesList)

    def __createPluginsPage(self):
        pluginsPage = PluginsPanel(self._dialog.treeBook)
        self._dialog.treeBook.AddPage(pluginsPage, _(u"Plugins"))

    def __createIconsetPage(self):
        iconsetPage = IconsetPanel(self._dialog.treeBook)
        self._dialog.treeBook.AddPage(iconsetPage, _(u"User's iconset"))

    def __setDialogPreperties(self):
        config = PrefDialogConfig(self._application.config)

        self._dialog.SetTitle(_("Preferences"))
        self._dialog.treeBook.SetMinSize((300, -1))

        self._dialog.Fit()
        fitWidth, fitHeight = self._dialog.GetSize()
        self._dialog.SetMinSize((fitWidth, fitHeight))
        self._dialog.SetClientSize((config.width.value, config.height.value))
        self.__centerDialog()

    def __centerDialog(self):
        """
        Расположить окно по центру родителя
        """
        selfWidth, selfHeight = self._dialog.GetSize()

        parentWidth, parentHeight = self._dialog.GetParent().GetSize()
        parentX, parentY = self._dialog.GetParent().GetPosition()

        posX = parentX + (parentWidth - selfWidth) / 2
        posY = parentY + (parentHeight - selfHeight) / 2

        self._dialog.SetPosition((posX, posY))

    def __loadAllOptions(self):
        """
        Загрузить настройки для всех страниц
        """
        for pageIndex in range(self._dialog.treeBook.GetPageCount()):
            page = self._dialog.treeBook.GetPage(pageIndex)
            page.LoadState()

    def __expandAllPages(self):
        """
        Развернуть все узлы в дереве настроек
        """
        for pageindex in range(self._dialog.treeBook.GetPageCount()):
            self._dialog.treeBook.ExpandNode(pageindex)
