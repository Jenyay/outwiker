# -*- coding: UTF-8 -*-

import wx
import wx.combo

from outwiker.core.tagslist import TagsList
from outwiker.core.factoryselector import FactorySelector
from outwiker.core.commands import testPageTitle, MessageBox
from outwiker.core.tree import RootWikiPage
from outwiker.core.events import (PageDialogPageTypeChangedParams,
                                  PageDialogPageTitleChangedParams,
                                  PageDialogPageTagsChangedParams)
from outwiker.gui.tagsselector import TagsSelector, EVT_TAGS_LIST_CHANGED
from outwiker.gui.guiconfig import PageDialogConfig
from basepanel import BasePageDialogPanel
from basecontroller import BasePageDialogController


class GeneralPanel (BasePageDialogPanel):
    """
    Класс панели, расположенной на вкладке "Общее"
    """
    def __init__ (self, parent, application, dialog):
        super (GeneralPanel, self).__init__ (parent, application)
        self._dialog = dialog

        self.__createGeneralControls()
        self.__layout ()


    def __layout (self):
        titleSizer = wx.FlexGridSizer(1, 2, 0, 0)
        titleSizer.Add(self.titleLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        titleSizer.Add(self.titleTextCtrl, 0, wx.ALL | wx.EXPAND, 4)
        titleSizer.AddGrowableCol(1)

        typeSizer = wx.FlexGridSizer(1, 2, 0, 0)
        typeSizer.Add(self.typeLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        typeSizer.Add(self.typeCombo, 0, wx.ALL | wx.EXPAND, 4)
        typeSizer.AddGrowableCol(1)

        generalSizer = wx.FlexGridSizer(3, 1, 0, 0)
        generalSizer.AddGrowableRow(2)
        generalSizer.AddGrowableCol(0)
        generalSizer.Add(titleSizer, 0, wx.EXPAND, 0)
        generalSizer.Add(typeSizer, 0, wx.EXPAND, 0)
        generalSizer.Add(self.tagsSelector, 0, wx.EXPAND, 0)

        self.SetSizer (generalSizer)
        self.Layout()


    def __createGeneralControls (self):
        self.titleLabel = wx.StaticText(self, -1, _(u"Title"))

        self.titleTextCtrl = wx.TextCtrl(self, -1, "")
        self.titleTextCtrl.SetMinSize((350, -1))

        self.typeCombo = wx.ComboBox(self,
                                     -1,
                                     choices=[],
                                     style=wx.CB_DROPDOWN | wx.CB_READONLY)

        self.tagsSelector = TagsSelector (self)
        self.typeLabel = wx.StaticText(self, -1, _(u"Page type"))


    @property
    def pageTitle (self):
        return self.titleTextCtrl.GetValue().strip()


    @property
    def selectedFactory (self):
        index = self.typeCombo.GetSelection()
        return self.typeCombo.GetClientData (index)


    @property
    def tags (self):
        return self.tagsSelector.tags


    @tags.setter
    def tags (self, value):
        self.tagsSelector.tags = value


class GeneralController (BasePageDialogController):
    def __init__ (self, generalPanel, application, dialog):
        super (GeneralController, self).__init__ (application)
        self._dialog = dialog
        self._generalPanel = generalPanel

        self._fillComboType()
        self._setTagsList()

        self._generalPanel.typeCombo.Bind (
            wx.EVT_COMBOBOX,
            handler=self.__onPageTypeChanged
        )

        self._generalPanel.titleTextCtrl.Bind (
            wx.EVT_TEXT,
            handler=self.__onPageTitleChanged
        )

        self._generalPanel.tagsSelector.Bind (
            EVT_TAGS_LIST_CHANGED,
            handler=self.__onTagsListChanged
        )


    def setPageProperties (self, page):
        """
        Return True if success and False otherwise
        """
        page.tags = self._generalPanel.tags
        return True


    def saveParams (self):
        PageDialogConfig (self._application.config).recentCreatedPageType.value = self._generalPanel.selectedFactory.getTypeString()


    def initBeforeCreation (self, parentPage):
        """
        Initialize the panel before new page creation
        parentPage - the parent page for new page
        """
        if parentPage.parent is not None:
            self._generalPanel.tags = parentPage.tags

        # Опция для хранения типа страницы, которая была создана последней
        lastCreatedPageType = PageDialogConfig (self._application.config).recentCreatedPageType.value
        self._setComboPageType(lastCreatedPageType)
        self._generalPanel.titleTextCtrl.SetFocus()


    def initBeforeEditing (self, currentPage):
        """
        Initialize the panel before new page editing.
        page - page for editing
        """
        self._generalPanel.titleTextCtrl.SetFocus()
        self._generalPanel.titleTextCtrl.SetSelection (-1, -1)

        self._generalPanel.tags = currentPage.tags

        # Запретить изменять заголовок
        self._generalPanel.titleTextCtrl.SetValue (currentPage.title)

        # Установить тип страницы
        self._setComboPageType(currentPage.getTypeString())
        self._generalPanel.typeCombo.Disable ()


    def _validateCommon (self, parentPage):
        if not testPageTitle (self._generalPanel.pageTitle):
            self._generalPanel.titleTextCtrl.SetFocus()
            self._generalPanel.titleTextCtrl.SetSelection (-1, -1)
            return False

        return True


    def validateBeforeCreation (self, parentPage):
        if not self._validateCommon (parentPage):
            return False

        if (parentPage is not None and
                not RootWikiPage.testDublicate (parentPage, self._generalPanel.pageTitle)):
            MessageBox (_(u"A page with some title already exists"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return False

        return True


    def validateBeforeEditing (self, page):
        if not self._validateCommon (page.parent):
            return False

        if not page.canRename (self._generalPanel.pageTitle):
            MessageBox (_(u"Can't rename page when page with that title already exists"),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            return False

        return True


    def _fillComboType (self):
        self._generalPanel.typeCombo.Clear()
        for factory in FactorySelector.getFactories():
            self._generalPanel.typeCombo.Append (factory.title, factory)

        if not self._generalPanel.typeCombo.IsEmpty():
            self._generalPanel.typeCombo.SetSelection (0)


    def _setTagsList (self):
        assert self._application.wikiroot is not None

        tagslist = TagsList (self._application.wikiroot)
        self._generalPanel.tagsSelector.setTagsList (tagslist)


    def _setComboPageType (self, pageTypeString):
        """
        Установить тип страницы в диалоге по строке, описывающей тип страницы
        """
        n = 0
        for factory in FactorySelector.getFactories():
            if factory.getTypeString() == FactorySelector.getFactory(pageTypeString).getTypeString():
                self._generalPanel.typeCombo.SetSelection (n)
                break
            n += 1


    def __onPageTypeChanged (self, event):
        eventParams = PageDialogPageTypeChangedParams (
            self._dialog,
            self._generalPanel.selectedFactory.getPageType().getTypeString())

        self._application.onPageDialogPageTypeChanged (
            self._generalPanel._application.selectedPage,
            eventParams)


    def __onPageTitleChanged (self, event):
        eventParams = PageDialogPageTitleChangedParams (
            self._dialog,
            self._generalPanel.pageTitle)

        self._application.onPageDialogPageTitleChanged (
            self._application.selectedPage,
            eventParams)


    def __onTagsListChanged (self, event):
        eventParams = PageDialogPageTagsChangedParams (
            self._dialog,
            self._generalPanel.tags)

        self._application.onPageDialogPageTagsChanged (
            self._application.selectedPage,
            eventParams)
