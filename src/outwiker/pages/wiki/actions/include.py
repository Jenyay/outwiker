#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.attachment import Attachment
from outwiker.core.commands import MessageBox


class WikiIncludeAction (BaseAction):
    """
    Вставка команды для вставки содержимого прикрепленного файла
    """
    stringId = u"WikiInclude"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Include (:include ...:)")


    @property
    def description (self):
        return _(u"Insert (:include:) command")


    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        if len (Attachment (self._application.selectedPage).attachmentFull) == 0:
            MessageBox (_("Current page does not have any attachments"),
                    _(u"Error"), 
                    wx.OK | wx.ICON_INFORMATION)
            return

        with IncludeDialog (self._application.mainWindow, self._application) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
                codeEditor.replaceText (self._getCommandString (dlg) )


    def _getCommandString (self, dlg):
        params = []

        params.append ("Attach:" + dlg.selectedAttachment)

        if dlg.selectedEncoding != "utf-8":
            params.append ("encoding=" + '"' + dlg.selectedEncoding + '"')

        if dlg.escapeHtml:
            params.append ("htmlescape")

        if dlg.parseWiki:
            params.append ("wikiparse")

        return u"(:include {}:)".format (u" ".join (params))


class IncludeDialog (wx.Dialog):
    def __init__ (self, parent, application):
        super (IncludeDialog, self).__init__ (parent)
        self._application = application

        self.SetTitle (_(u"Insert (:include:) command"))

        self.__createGui ()
        self.__layout()


    @property
    def selectedAttachment (self):
        return self._attachComboBox.GetValue()


    @property
    def selectedEncoding (self):
        return self._encodingComboBox.GetValue()


    @property
    def escapeHtml (self):
        return self._escapeHtmlCheckBox.IsChecked()


    @property
    def parseWiki (self):
        return self._wikiParseCheckBox.IsChecked()


    def __createGui (self):
        # Выбор прикрепленного файла
        self._attachLabel = wx.StaticText (self, label = _(u"Select attachment"))

        self._attachComboBox = wx.ComboBox (self, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        self._fillAttaches (self._attachComboBox)
        if self._attachComboBox.GetCount() > 0:
            self._attachComboBox.SetSelection (0)

        # Кодировка
        self._encodingLabel = wx.StaticText (self, label = _(u"Encoding"))

        self._encodingComboBox = wx.ComboBox (self, style = wx.CB_DROPDOWN)
        self._fillEncodings (self._encodingComboBox)
        self._encodingComboBox.SetSelection (0)

        # Преобразовывать символы HTML?
        self._escapeHtmlCheckBox = wx.CheckBox (self, label=_(u"Convert symbols to HTML") )

        # Делать разбор викинотации?
        self._wikiParseCheckBox = wx.CheckBox (self, label=_(u"Parse wiki notation") )

        self._buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)


    def __layout (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        mainSizer.Add (self._attachLabel, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border = 2)
        mainSizer.Add (self._attachComboBox, 
                flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border = 2)

        mainSizer.Add (self._encodingLabel, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border = 2)
        mainSizer.Add (self._encodingComboBox, 
                flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border = 2)

        mainSizer.Add (self._escapeHtmlCheckBox, 
                flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border = 2)
        mainSizer.AddStretchSpacer()

        mainSizer.Add (self._wikiParseCheckBox, 
                flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border = 2)
        mainSizer.AddStretchSpacer()

        mainSizer.AddStretchSpacer()
        mainSizer.Add (self._buttonsSizer, 
                flag = wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 
                border = 2)

        self.SetSizer (mainSizer)
        self.Fit()


    def _fillEncodings (self, combobox):
        encodings = [
                u"utf-8",
                u"utf-16",
                u"windows-1251",
                u"koi8_r",
                u"koi8_u",
                u"cp866",
                u"mac_cyrillic",
                ]

        combobox.AppendItems (encodings)


    def _fillAttaches (self, combobox):
        selectedPage = self._application.selectedPage
        assert selectedPage != None

        attaches = Attachment(selectedPage).getAttachRelative()
        attaches.sort (Attachment.sortByName)

        combobox.AppendItems (attaches)
