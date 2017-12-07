# -*- coding: utf-8 -*-

import wx

from outwiker.gui.preferences.configelements import BooleanElement, IntegerElement
from outwiker.core.application import Application
from wikiconfig import WikiConfig
from emptycontent import EmptyContent
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


class WikiPrefGeneralPanel(BasePrefPanel):
    def __init__(self, parent):
        super (WikiPrefGeneralPanel, self).__init__ (parent)

        self.__createGui()
        self.config = WikiConfig (Application.config)


    def __createGui (self):
        # Показывать ли результирующий HTML?
        self.htmlCodeCheckbox = wx.CheckBox(self, -1, _(u"Show HTML Code Tab"))

        # Highlight the wiki notation?
        self.colorizeWiki = wx.CheckBox(self, -1, _(u"Highlight the Wiki Notation"))

        # Размер миниатюр
        self.thumbSizeLabel = wx.StaticText(self, -1, _(u"Thumbnail Size"))
        self.thumbSize = wx.SpinCtrl(self, -1, "250", min=1, max=10000)

        # Шаблон для пустых страниц
        self.emptyTplLabel = wx.StaticText(self, -1, _(u"Template for empty page"))
        self.emptyTplTextCtrl = wx.TextCtrl(self, -1, "",
                                            style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_WORDWRAP)

        # Стиль ссылок по умолчанию (при создании через диалог)
        self.linkStyleLabel = wx.StaticText (self, label=_(u"Default link style"))
        self.linkStyleCombo = wx.ComboBox (self, -1, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.linkStyleCombo.AppendItems ([
            _(u"[[comment -> link]]"),
            _(u"[[link | comment]]")
        ])
        self.linkStyleCombo.SetSelection (0)

        self.__do_layout()


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableRow(5)
        mainSizer.AddGrowableCol(0)

        # Показывать ли результирующий HTML?
        mainSizer.Add(self.htmlCodeCheckbox, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        # Highlight the wiki notation?
        mainSizer.Add(self.colorizeWiki, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        # Размер миниатюр
        thumbSizer = wx.FlexGridSizer(1, 2, 0, 0)
        thumbSizer.AddGrowableCol(0)
        thumbSizer.AddGrowableCol(1)
        thumbSizer.Add(self.thumbSizeLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)
        thumbSizer.Add(self.thumbSize, 0, wx.ALL | wx.EXPAND, 2)
        mainSizer.Add(thumbSizer, 1, wx.EXPAND, 0)

        # Стиль ссылок по умолчанию (при создании через диалог)
        linkStyleSizer = wx.FlexGridSizer(1, 2, 0, 0)
        linkStyleSizer.AddGrowableCol(0)
        linkStyleSizer.AddGrowableCol(1)
        linkStyleSizer.Add (self.linkStyleLabel, 0,
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        linkStyleSizer.Add (self.linkStyleCombo, 0,
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, border=2)
        mainSizer.Add(linkStyleSizer, 1, wx.EXPAND, 0)

        # Шаблон для пустых страниц
        mainSizer.Add(self.emptyTplLabel, 0, wx.ALL, 4)
        mainSizer.Add(self.emptyTplTextCtrl, 0, wx.ALL | wx.EXPAND, 4)

        self.SetSizer(mainSizer)
        self.Layout()


    def LoadState(self):
        # Показывать ли вкладку с кодом HTML
        self.showHtmlCodeOption = BooleanElement (self.config.showHtmlCodeOptions, self.htmlCodeCheckbox)

        self.colorizeWiki.SetValue (self.config.colorizeSyntax.value)

        # Размер превьюшек по умолчанию
        self.thumbSizeOption = IntegerElement (self.config.thumbSizeOptions, self.thumbSize, 1, 10000)

        # Шаблон для пустых страниц
        emptycontent = EmptyContent (Application.config)
        self.emptyTplTextCtrl.SetValue (emptycontent.content)

        # Стиль ссылок по умолчанию
        linkStyle = self.config.linkStyleOptions.value
        self.linkStyleCombo.SetSelection (
            linkStyle if linkStyle >= 0 and linkStyle < self.linkStyleCombo.GetCount() else 0)


    def Save (self):
        changed = (self.showHtmlCodeOption.isValueChanged() or
                   self.thumbSizeOption.isValueChanged())

        self.showHtmlCodeOption.save()
        self.thumbSizeOption.save()

        self.config.colorizeSyntax.value = self.colorizeWiki.GetValue()

        emptycontent = EmptyContent (Application.config)
        emptycontent.content = self.emptyTplTextCtrl.GetValue()
        self.config.linkStyleOptions.value = self.linkStyleCombo.GetSelection()

        if changed:
            currpage = Application.wikiroot.selectedPage
            Application.wikiroot.selectedPage = None
            Application.wikiroot.selectedPage = currpage
