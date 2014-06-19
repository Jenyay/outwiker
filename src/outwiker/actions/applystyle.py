# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.core.commands import testreadonly
from outwiker.core.style import Style
from outwiker.core.styleslist import StylesList
from outwiker.core.system import getStylesDirList


class SetStyleToBranchAction (BaseAction):
    """
    Применить стиль ко всем страницам ветки
    """
    stringId = u"SetStyleToBranch"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Set Style to Branch…")


    @property
    def description (self):
        return _(u"Set Style to Branch")


    def run (self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return

        if self._application.selectedPage is None:
            self.addStyleToBranchGui (self._application.wikiroot,
                                      self._application.mainWindow)
        else:
            self.addStyleToBranchGui (self._application.selectedPage,
                                      self._application.mainWindow)


    @testreadonly
    def addStyleToBranchGui (self, page, parent):
        """
        Установить стиль для всей ветки, в том числе и для текущей страницы
        """
        with AddStyleDialog (self._application.mainWindow) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                wiki = self._application.wikiroot

                # Чтобы не вызывались никакие события при обновлении стиля
                self._application.wikiroot = None

                runner = LongProcessRunner (self.__applyStyle,
                                            self._application.mainWindow,
                                            _(u"Set Style to Branch"),
                                            _(u"Please wait..."))

                runner.run (page, dlg.style)
                # Вернем открытую вики
                self._application.wikiroot = wiki


    def __applyStyle (self, page, style):
        if page.parent is not None:
            # Если это не корень вики
            Style().setPageStyle (page, style)

        map (lambda child: self.__applyStyle (child, style), page.children)



class AddStyleDialog (TestedDialog):
    def __init__ (self, parent):
        super (AddStyleDialog, self).__init__ (parent,
                                               style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.__stylesList = StylesList (getStylesDirList ())

        self.SetMinSize ((300, 80))
        self.__createGui()
        self.Center(wx.CENTRE_ON_SCREEN)


    def __createGui (self):
        self.SetTitle (_(u"Set style to branch"))

        styleLabel = wx.StaticText (parent = self,
                                    label = _(u"Style"))

        self.__stylesCombo = wx.ComboBox (parent = self,
                                          style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.__stylesCombo.SetMinSize ((200, -1))

        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (1)
        mainSizer.AddGrowableRow (1)

        mainSizer.Add (styleLabel,
                       flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border = 4)

        mainSizer.Add (self.__stylesCombo,
                       flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                       border = 4)

        self.__createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)
        self.Fit()

        self.__fillStyles (self.__stylesCombo)


    def __fillStyles (self, combobox):
        names_list = [_(u"Default")] + [os.path.basename (style)
                                        for style
                                        in self.__stylesList]

        combobox.Clear()
        combobox.AppendItems (names_list)
        combobox.SetSelection (0)


    def __createOkCancelButtons (self, mainSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add (
            okCancel,
            flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
            border=4
        )


    @property
    def style (self):
        selItem = self.__stylesCombo.GetSelection()
        if selItem == 0:
            return Style().getDefaultStyle()

        return self.__stylesList[selItem - 1]
