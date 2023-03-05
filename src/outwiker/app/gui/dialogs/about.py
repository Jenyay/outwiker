# -*- coding: utf-8 -*-

import wx

from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.controls.hyperlink import HyperLinkCtrl
from outwiker.gui.testeddialog import TestedDialog


class AboutDialog(TestedDialog):
    def __init__(self, currversion, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super().__init__(parent, style=style)

        self.titleLabel = wx.StaticText(self, -1, _("OutWiker"))
        self.versionTitleLabel = wx.StaticText(self, -1, _("Version:"))
        self.versionLabel = wx.StaticText(self, -1, "")
        self.notebook = wx.Notebook(self, -1, style=0)
        self.aboutPane = wx.Panel(self.notebook, -1)
        self.logo = wx.StaticBitmap(
            self.aboutPane,
            -1,
            wx.Bitmap(getBuiltinImagePath("outwiker_64x64.png"),
                      wx.BITMAP_TYPE_ANY)
        )

        self.description = wx.StaticText(
            self.aboutPane,
            -1,
            _("OutWiker is personal wiki system and tree notes outliner.")
        )

        self.license = wx.StaticText(self.aboutPane, -1, _("License: GPL 3"))

        self.siteLabel = wx.StaticText(
            self.aboutPane,
            -1,
            _("OutWiker's page:")
        )

        self.outwikerUrl = HyperLinkCtrl(
            self.aboutPane,
            -1,
            label=_("https://jenyay.net/Outwiker/English"),
            URL=_("https://jenyay.net/Outwiker/English")
        )

        self.contactsPane = wx.Panel(self.notebook, -1)

        self.email = HyperLinkCtrl(
            self.contactsPane,
            -1,
            label="jenyay.ilin@gmail.com",
            URL=_(u"mailto:jenyay.ilin@gmail.com")
        )

        self.twitter = HyperLinkCtrl(
            self.contactsPane,
            -1,
            label=_("Twitter"),
            URL=_("https://twitter.com/OutWiker")
        )

        self.vkontakte = HyperLinkCtrl(
            self.contactsPane,
            -1,
            label=_("Vkontakte group"),
            URL=_("https://vk.com/outwiker")
        )

        self.okButton = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()

        self.currversion = currversion
        self.versionLabel.SetLabel(str(self.currversion))

    def __set_properties(self):
        self.SetTitle(_("About"))
        self.SetSize((500, 350))
        self.titleLabel.SetFont(wx.Font(
            15,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_NORMAL,
            0,
            ""))
        self.description.SetMinSize((-1, 50))
        self.okButton.SetFocus()
        self.okButton.SetDefault()

    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableRow(2)
        main_sizer.AddGrowableCol(0)

        self._create_title(main_sizer)
        self._create_about_tab()
        self._create_contacts_tab()

        self.notebook.AddPage(self.aboutPane, _("About"))
        self.notebook.AddPage(self.contactsPane, _("Contacts"))
        main_sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 2)
        main_sizer.Add(self.okButton, 0, wx.ALL |
                       wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 4)
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre()

    def _create_about_tab(self):
        about_tab_sizer = wx.FlexGridSizer(cols=2)
        about_tab_right_column = wx.FlexGridSizer(cols=1)
        home_page_sizer = wx.FlexGridSizer(cols=2)

        about_tab_sizer.Add(self.logo,
                            flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL,
                            border=8)
        about_tab_right_column.Add(self.description,
                                   flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL,
                                   border=4)
        author = wx.StaticText(
            self.aboutPane, -1, _("Author: Ilin Eugeniy (aka Jenyay)"))
        about_tab_right_column.Add(author,
                                   flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                   border=2)
        about_tab_right_column.Add(self.license,
                                   flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                   border=2)
        home_page_sizer.Add(self.siteLabel,
                            flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                            border=2)
        home_page_sizer.Add(self.outwikerUrl,
                            flag=wx.ALL | wx.ALIGN_LEFT,
                            border=2)
        home_page_sizer.AddGrowableCol(1)
        about_tab_right_column.Add(home_page_sizer, flag=wx.EXPAND, border=0)
        about_tab_right_column.AddGrowableCol(0)
        about_tab_sizer.Add(about_tab_right_column, flag=wx.EXPAND, border=0)
        about_tab_sizer.AddGrowableRow(0)
        about_tab_sizer.AddGrowableCol(1)
        self.aboutPane.SetSizer(about_tab_sizer)

    def _create_title(self, main_sizer):
        main_sizer.Add(
            self.titleLabel,
            flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,
            border=2)
        title_sizer = wx.FlexGridSizer(cols=2)
        title_sizer.Add(self.versionTitleLabel,
                        flag=wx.ALL | wx.ALIGN_RIGHT,
                        border=2)
        title_sizer.Add(self.versionLabel, flag=wx.ALL, border=2)
        title_sizer.AddGrowableRow(0)
        title_sizer.AddGrowableCol(0)
        title_sizer.AddGrowableCol(1)
        main_sizer.Add(title_sizer, flag=wx.EXPAND, border=0)

    def _create_contacts_tab(self):
        contacts_tab_sizer = wx.FlexGridSizer(cols=1)
        contacts_tab_sizer.AddGrowableCol(0)
        contacts_tab_sizer.Add(self.email,
                               flag=wx.ALL | wx.ALIGN_CENTER,
                               border=2)
        contacts_tab_sizer.Add(self.twitter,
                               flag=wx.ALL | wx.ALIGN_CENTER,
                               border=2)
        contacts_tab_sizer.Add(self.vkontakte,
                               flag=wx.ALL | wx.ALIGN_CENTER,
                               border=2)
        self.contactsPane.SetSizer(contacts_tab_sizer)
