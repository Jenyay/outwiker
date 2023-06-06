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
        self.aboutLogo = wx.StaticBitmap(
            self.aboutPane,
            -1,
            wx.Bitmap(getBuiltinImagePath("outwiker_64x64.png"), wx.BITMAP_TYPE_ANY),
        )

        self.description = wx.StaticText(
            self.aboutPane,
            -1,
            _("OutWiker is personal wiki system and tree notes outliner."),
        )

        self.license = wx.StaticText(self.aboutPane, -1, _("License: GPL 3"))

        self.outwikerUrlLabel = wx.StaticText(self.aboutPane, -1, _("OutWiker's home page"))
        self.outwikerTelegramLabel = wx.StaticText(self.aboutPane, -1, _("Telegram group"))
        self.outwikerVKLabel = wx.StaticText(self.aboutPane, -1, _("VK group"))
        self.outwikerGithubLabel = wx.StaticText(self.aboutPane, -1, _("Sources on github"))
        self.outwikerCrowdinLabel = wx.StaticText(self.aboutPane, -1, _("OutWiker localizations"))

        self.outwikerUrl = HyperLinkCtrl(
            self.aboutPane,
            -1,
            label=_("https://jenyay.net/Outwiker/English"),
            URL=_("https://jenyay.net/Outwiker/English"),
        )

        self.outwikerTelegram = HyperLinkCtrl(
            self.aboutPane,
            -1,
            label=_("https://t.me/outwiker"),
            URL=_("https://t.me/outwiker"),
        )

        self.outwikerVK = HyperLinkCtrl(
            self.aboutPane,
            -1,
            label=_("https://vk.com/outwiker"),
            URL=_("https://vk.com/outwiker"),
        )

        self.outwikerGithub = HyperLinkCtrl(
            self.aboutPane,
            -1,
            label=_("https://github.com/Jenyay/outwiker"),
            URL=_("https://github.com/Jenyay/outwiker"),
        )

        self.outwikerCrowdin = HyperLinkCtrl(
            self.aboutPane,
            -1,
            label=_("https://crowdin.com/project/outwiker"),
            URL=_("https://crowdin.com/project/outwiker"),
        )

        self.contactsPane = wx.Panel(self.notebook, -1)

        self.authorEmailLabel = wx.StaticText(self.contactsPane, -1, _("Email"))
        self.authorHomeSiteLabel = wx.StaticText(self.contactsPane, -1, _("Home site"))
        self.authorTelegramLabel = wx.StaticText(self.contactsPane, -1, _("Telegram group"))
        self.authorGithubLabel = wx.StaticText(self.contactsPane, -1, _("Github page"))

        self.authorEmail = HyperLinkCtrl(
            self.contactsPane,
            -1,
            label=_("jenyay.ilin@gmail.com"),
            URL=_("mailto:jenyay.ilin@gmail.com"),
        )

        self.authorHomeSite = HyperLinkCtrl(
            self.contactsPane,
            -1,
            label=_("https://jenyay.net"),
            URL=_("https://jenyay.net"),
        )

        self.authorTelegram = HyperLinkCtrl(
            self.contactsPane,
            -1,
            label=_("https://t.me/jenyaynet"),
            URL=_("https://t.me/jenyaynet"),
        )

        self.authorGithub = HyperLinkCtrl(
            self.contactsPane,
            -1,
            label=_("https://github.com/Jenyay"),
            URL=_("https://github.com/Jenyay"),
        )

        self.okButton = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()

        self.currversion = currversion
        self.versionLabel.SetLabel(str(self.currversion))

    def __set_properties(self):
        self.SetTitle(_("About"))
        self.SetSize((550, 380))
        self.titleLabel.SetFont(
            wx.Font(
                15,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                0,
                "",
            )
        )
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
        self.notebook.AddPage(self.contactsPane, _("Author contacts"))
        main_sizer.Add(self.notebook, 1, wx.ALL | wx.EXPAND, 2)
        main_sizer.Add(
            self.okButton, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL, 4
        )
        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre()

    def _create_about_tab(self):
        about_tab_sizer = wx.FlexGridSizer(cols=2)
        about_tab_sizer.AddGrowableCol(0)
        about_tab_sizer.AddGrowableCol(1)

        about_tab_right_column = wx.FlexGridSizer(cols=1)
        about_tab_right_column.AddGrowableCol(0)

        outwiker_pages_sizer = wx.FlexGridSizer(cols=2)
        outwiker_pages_sizer.AddGrowableCol(1)

        about_tab_sizer.Add(
            self.aboutLogo, flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, border=8
        )
        about_tab_right_column.Add(
            self.description,
            flag=wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL,
            border=4,
        )
        author = wx.StaticText(
            self.aboutPane, -1, _("Author: Eugeniy Ilin (aka Jenyay)")
        )
        about_tab_right_column.Add(
            author, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        about_tab_right_column.Add(
            self.license, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )

        outwiker_pages_sizer.Add(
            self.outwikerUrlLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        outwiker_pages_sizer.Add(
            self.outwikerUrl, flag=wx.ALL | wx.ALIGN_LEFT, border=2
        )

        outwiker_pages_sizer.Add(
            self.outwikerTelegramLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        outwiker_pages_sizer.Add(
            self.outwikerTelegram, flag=wx.ALL | wx.ALIGN_LEFT, border=2
        )

        outwiker_pages_sizer.Add(
            self.outwikerVKLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        outwiker_pages_sizer.Add(
            self.outwikerVK, flag=wx.ALL | wx.ALIGN_LEFT, border=2
        )

        outwiker_pages_sizer.Add(
            self.outwikerGithubLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        outwiker_pages_sizer.Add(
            self.outwikerGithub, flag=wx.ALL | wx.ALIGN_LEFT, border=2
        )

        outwiker_pages_sizer.Add(
            self.outwikerCrowdinLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2
        )
        outwiker_pages_sizer.Add(
            self.outwikerCrowdin, flag=wx.ALL | wx.ALIGN_LEFT, border=2
        )

        about_tab_right_column.Add(outwiker_pages_sizer, flag=wx.EXPAND, border=0)
        about_tab_sizer.Add(about_tab_right_column, flag=wx.EXPAND, border=0)
        self.aboutPane.SetSizer(about_tab_sizer)

    def _create_title(self, main_sizer):
        main_sizer.Add(
            self.titleLabel,
            flag=wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL,
            border=2,
        )
        title_sizer = wx.FlexGridSizer(cols=2)
        title_sizer.Add(self.versionTitleLabel, flag=wx.ALL | wx.ALIGN_RIGHT, border=2)
        title_sizer.Add(self.versionLabel, flag=wx.ALL, border=2)
        title_sizer.AddGrowableRow(0)
        title_sizer.AddGrowableCol(0)
        title_sizer.AddGrowableCol(1)
        main_sizer.Add(title_sizer, flag=wx.EXPAND, border=0)

    def _create_contacts_tab(self):
        border_sizer = wx.FlexGridSizer(cols=1)
        border_sizer.AddGrowableCol(0)
        border_sizer.AddGrowableRow(0)

        contacts_tab_sizer = wx.FlexGridSizer(cols=2)
        contacts_tab_sizer.AddGrowableCol(0)
        contacts_tab_sizer.AddGrowableCol(1)

        contacts_tab_sizer.Add(self.authorEmailLabel, flag=wx.ALL | wx.ALIGN_LEFT| wx.ALIGN_CENTER_VERTICAL, border=2)
        contacts_tab_sizer.Add(self.authorEmail, flag=wx.ALL | wx.ALIGN_LEFT, border=2)

        contacts_tab_sizer.Add(self.authorHomeSiteLabel, flag=wx.ALL | wx.ALIGN_LEFT| wx.ALIGN_CENTER_VERTICAL, border=2)
        contacts_tab_sizer.Add(self.authorHomeSite, flag=wx.ALL | wx.ALIGN_LEFT, border=2)

        contacts_tab_sizer.Add(self.authorTelegramLabel, flag=wx.ALL | wx.ALIGN_LEFT| wx.ALIGN_CENTER_VERTICAL, border=2)
        contacts_tab_sizer.Add(self.authorTelegram, flag=wx.ALL | wx.ALIGN_LEFT, border=2)

        contacts_tab_sizer.Add(self.authorGithubLabel, flag=wx.ALL | wx.ALIGN_LEFT| wx.ALIGN_CENTER_VERTICAL, border=2)
        contacts_tab_sizer.Add(self.authorGithub, flag=wx.ALL | wx.ALIGN_LEFT, border=2)

        border_sizer.Add(contacts_tab_sizer, flag=wx.ALL | wx.EXPAND, border=8)
        self.contactsPane.SetSizer(border_sizer)
