# -*- coding: UTF-8 -*-

from outwiker.gui.controllers.basecontroller import BaseController
from outwiker.core.event import EVENT_PRIORITY_MAX_CORE
from outwiker.core.factoryselector import FactorySelector

from preferencepanelinfo import PreferencePanelInfo
from generalpanel import GeneralPanel
from editorpanel import EditorPanel
from spellpanel import SpellPanel
from htmlrenderpanel import HtmlRenderPanel
from textprintpanel import TextPrintPanel
from pluginspanel import PluginsPanel
from hotkeyspanel import HotKeysPanel
from htmleditorpanel import HtmlEditorPanel
from wikieditorpanel import WikiEditorPanel
from iconsetpanel import IconsetPanel
from tagspanel import TagsPanel
from attachpanel import AttachPanel


class PrefController (BaseController):
    def __init__ (self, application):
        self._application = application
        self._dialog = None


    def initialize (self):
        self._application.onPreferencesDialogCreate.bind (
            self._onPrefDialogCreate,
            EVENT_PRIORITY_MAX_CORE
        )


    def clear (self):
        self._application.onPreferencesDialogCreate -= self._onPrefDialogCreate
        self._dialog = None


    def _onPrefDialogCreate (self, dialog):
        self._dialog = dialog
        self.__createInterfaceGroup ()
        self.__createEditorGroup ()
        self.__createPagesForPages ()
        self.__createIconsetPage ()
        self.__createPluginsPage ()


    def __createPagesForPages (self):
        """
        Создать страницы настроек для типов страниц
        """
        for factory in FactorySelector.getFactories():
            # Список экземпляров класса PreferencePanelInfo
            panelsList = factory.getPrefPanels(self._dialog.treeBook)

            if len (panelsList) > 0:
                self._dialog.appendPreferenceGroup (factory.title, panelsList)


    def __createInterfaceGroup (self):
        """
        Создать страницы с подгруппой "Interface"
        """
        generalPage = GeneralPanel (self._dialog.treeBook)
        htmlRenderPage = HtmlRenderPanel (self._dialog.treeBook)
        textPrintPage = TextPrintPanel (self._dialog.treeBook)
        hotkeysPage = HotKeysPanel (self._dialog.treeBook)
        tagsPage = TagsPanel (self._dialog.treeBook)
        attachPage = AttachPanel (self._dialog.treeBook)

        interfacePanelsList = [
            PreferencePanelInfo (generalPage, _(u"General")),
            PreferencePanelInfo (htmlRenderPage, _(u"Preview")),
            PreferencePanelInfo (tagsPage, _(u"Tags cloud")),
            PreferencePanelInfo (attachPage, _(u"Attachments")),
            PreferencePanelInfo (hotkeysPage, _(u"Hotkeys")),
            PreferencePanelInfo (textPrintPage, _(u"Text Printout")),
        ]

        self._dialog.appendPreferenceGroup (_(u"Interface"), interfacePanelsList)


    def __createEditorGroup (self):
        """
        Создать страницы с подгруппой "Редактор"
        """
        editorPage = EditorPanel (self._dialog.treeBook)
        spellPage = SpellPanel (self._dialog.treeBook)
        htmlEditorPage = HtmlEditorPanel (self._dialog.treeBook)
        wikiEditorPage = WikiEditorPanel (self._dialog.treeBook)

        editorPanesList = [
            PreferencePanelInfo (editorPage, _(u"General")),
            PreferencePanelInfo (spellPage, _(u"Spell checking")),
            PreferencePanelInfo (htmlEditorPage, _(u"HTML Editor")),
            PreferencePanelInfo (wikiEditorPage, _(u"Wiki Editor")),
        ]

        self._dialog.appendPreferenceGroup (_(u"Editor"), editorPanesList)


    def __createPluginsPage (self):
        pluginsPage = PluginsPanel (self._dialog.treeBook)
        self._dialog.treeBook.AddPage (pluginsPage, _(u"Plugins"))


    def __createIconsetPage (self):
        iconsetPage = IconsetPanel (self._dialog.treeBook)
        self._dialog.treeBook.AddPage (iconsetPage, _(u"User's iconset"))
