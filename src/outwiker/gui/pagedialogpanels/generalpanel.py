# -*- coding: utf-8 -*-

from datetime import datetime
from typing import List, Callable

import wx

import outwiker.core.factory as ocf
from outwiker.core.tagslist import TagsList
from outwiker.core.tree import RootWikiPage
from outwiker.core.events import (PageDialogPageTypeChangedParams,
                                  PageDialogPageTitleChangedParams,
                                  PageDialogPageTagsChangedParams,
                                  PageDialogPageFactoriesNeededParams,
                                  PageDialogNewPageOrderChangedParams)
from outwiker.gui.tagsselector import TagsSelector, EVT_TAGS_LIST_CHANGED
from outwiker.gui.guiconfig import PageDialogConfig, GeneralGuiConfig
from .basecontroller import BasePageDialogController


class GeneralPanel(wx.Panel):
    """
    Класс панели, расположенной на вкладке "Общее"
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.__createGeneralControls()
        self.__layout()

    def __layout(self):
        # Page alias
        titleSizer = wx.FlexGridSizer(cols=2)
        titleSizer.AddGrowableCol(1)
        titleSizer.Add(self.titleLabel,
                       flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        titleSizer.Add(self.titleTextCtrl, flag=wx.ALL | wx.EXPAND, border=4)

        # Page type
        typeSizer = wx.FlexGridSizer(cols=2)
        typeSizer.AddGrowableCol(1)
        typeSizer.Add(self.typeLabel, flag=wx.ALL |
                      wx.ALIGN_CENTER_VERTICAL, border=4)
        typeSizer.Add(self.typeCombo, flag=wx.ALL | wx.EXPAND, border=4)

        # Page order
        self.orderSizer = wx.FlexGridSizer(cols=2)
        self.orderSizer.AddGrowableCol(1)
        self.orderSizer.Add(
            self.orderLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        self.orderSizer.Add(
            self.orderCombo, flag=wx.ALL | wx.EXPAND, border=4)

        generalSizer = wx.FlexGridSizer(cols=1)
        generalSizer.AddGrowableRow(3)
        generalSizer.AddGrowableCol(0)
        generalSizer.Add(titleSizer, flag=wx.EXPAND)
        generalSizer.Add(typeSizer, flag=wx.EXPAND)
        generalSizer.Add(self.orderSizer, flag=wx.EXPAND)
        generalSizer.Add(self.tagsSelector, flag=wx.EXPAND)

        self.SetSizer(generalSizer)
        self.Layout()

    def __createGeneralControls(self):
        # Page alias
        self.titleLabel = wx.StaticText(self, label=_(u"Title"))
        self.titleTextCtrl = wx.TextCtrl(self, value="")
        self.titleTextCtrl.SetMinSize((350, -1))

        # Page type
        self.typeLabel = wx.StaticText(self, label=_(u"Page type"))
        self.typeCombo = wx.ComboBox(self,
                                     choices=[],
                                     style=wx.CB_DROPDOWN | wx.CB_READONLY)

        # Page order
        self.orderLabel = wx.StaticText(self, label=_('New page position'))
        self.orderCombo = wx.ComboBox(self,
                                      choices=[],
                                      style=wx.CB_DROPDOWN | wx.CB_READONLY)

        # Tags
        self.tagsSelector = TagsSelector(self)

    @property
    def pageTitle(self):
        return self.titleTextCtrl.GetValue()

    @pageTitle.setter
    def pageTitle(self, value):
        self.titleTextCtrl.SetValue(value)


class GeneralController(BasePageDialogController):
    def __init__(self, generalPanel, application, dialog):
        super().__init__(application)
        self._dialog = dialog
        self._generalPanel = generalPanel
        self._config = PageDialogConfig(self._application.config)

        self._orderCalculators = [
            (ocf.orderCalculatorTop, _('Top of the list')),
            (ocf.orderCalculatorBottom, _('End of the list')),
            (ocf.orderCalculatorAlphabetically, _('Alphabetically')),
        ]

        self._setTagsList()

        self._generalPanel.typeCombo.Bind(
            wx.EVT_COMBOBOX,
            handler=self.__onPageTypeChanged
        )

        self._generalPanel.titleTextCtrl.Bind(
            wx.EVT_TEXT,
            handler=self.__onPageTitleChanged
        )

        self._generalPanel.orderCombo.Bind(
            wx.EVT_COMBOBOX,
            handler=self.__onPageOrderChanged
        )

        self._generalPanel.tagsSelector.Bind(
            EVT_TAGS_LIST_CHANGED,
            handler=self.__onTagsListChanged
        )

    @property
    def pageTitle(self) -> str:
        return self._generalPanel.titleTextCtrl.GetValue().strip()

    @pageTitle.setter
    def pageTitle(self, value: str):
        self._generalPanel.titleTextCtrl.SetValue(value)

    @property
    def selectedFactory(self):
        index = self._generalPanel.typeCombo.GetSelection()
        return self._generalPanel.typeCombo.GetClientData(index)

    @property
    def tags(self) -> List[str]:
        return self._generalPanel.tagsSelector.tags

    @tags.setter
    def tags(self, value: List[str]):
        self._generalPanel.tagsSelector.tags = value

    @property
    def orderCalculator(self) -> Callable[[RootWikiPage, str, List[str]], int]:
        index = self._generalPanel.orderCombo.GetSelection()
        return self._orderCalculators[index][0]

    def setPageProperties(self, page):
        """
        Return True if success and False otherwise
        """
        page.tags = self.tags
        return True

    def saveParams(self):
        self._config.recentCreatedPageType.value = self.selectedFactory.getTypeString()
        self._config.newPageOrderCalculator.value = self._generalPanel.orderCombo.GetSelection()

    def initBeforeCreation(self, parentPage):
        """
        Initialize the panel before new page creation
        parentPage - the parent page for new page
        """
        self._fillComboType(None)
        self._fillComboOrderCalculators()

        if parentPage.parent is not None:
            self.tags = parentPage.tags

        # Опция для хранения типа страницы, которая была создана последней
        lastCreatedPageType = self._config.recentCreatedPageType.value
        self._setComboPageType(lastCreatedPageType)

        title = self._getDefaultTitle()
        self._generalPanel.titleTextCtrl.SetValue(title)
        self._generalPanel.titleTextCtrl.SelectAll()
        self._generalPanel.orderSizer.ShowItems(True)
        self._generalPanel.Layout()

        self.__onPageTypeChanged(None)

    def _getDefaultTitle(self):
        config = GeneralGuiConfig(self._application.config)
        template = config.pageTitleTemplate.value
        title = datetime.now().strftime(template)
        return title

    def initBeforeEditing(self, currentPage):
        """
        Initialize the panel before new page editing.
        page - page for editing
        """
        self._fillComboType(currentPage)
        self._generalPanel.titleTextCtrl.SetSelection(-1, -1)

        self.tags = currentPage.tags

        self._generalPanel.titleTextCtrl.SetValue(currentPage.display_title)

        # Установить тип страницы
        self._setComboPageType(currentPage.getTypeString())
        self._generalPanel.typeCombo.Disable()
        self._generalPanel.orderSizer.ShowItems(False)
        self._generalPanel.Layout()
        self.__onPageTypeChanged(None)

    def validateBeforeCreation(self, _parentPage):
        return True

    def validateBeforeEditing(self, _page):
        return True

    def clear(self):
        self._generalPanel.typeCombo.Unbind(
            wx.EVT_COMBOBOX,
            handler=self.__onPageTypeChanged
        )

        self._generalPanel.titleTextCtrl.Unbind(
            wx.EVT_TEXT,
            handler=self.__onPageTitleChanged
        )

        self._generalPanel.orderCombo.Unbind(
            wx.EVT_COMBOBOX,
            handler=self.__onPageOrderChanged
        )

        self._generalPanel.tagsSelector.Unbind(
            EVT_TAGS_LIST_CHANGED,
            handler=self.__onTagsListChanged
        )
        self._dialog = None

    def _fillComboType(self, currentPage):
        """
        currentPage - page for edit or None if dialog opened
            for creation a page
        """
        eventParams = PageDialogPageFactoriesNeededParams(self._dialog,
                                                          currentPage)
        self._application.onPageDialogPageFactoriesNeeded(
            self._application.selectedPage,
            eventParams
        )

        self._generalPanel.typeCombo.Clear()
        for factory in eventParams.pageFactories:
            self._generalPanel.typeCombo.Append(factory.title, factory)

        if not self._generalPanel.typeCombo.IsEmpty():
            self._generalPanel.typeCombo.SetSelection(0)

    def _fillComboOrderCalculators(self):
        orderTitles = [item[1] for item in self._orderCalculators]
        self._generalPanel.orderCombo.SetItems(orderTitles)
        order = self._config.newPageOrderCalculator.value

        if order >= 0 and order < len(self._orderCalculators):
            self._generalPanel.orderCombo.SetSelection(order)
        else:
            self._generalPanel.orderCombo.SetSelection(1)

    def _setTagsList(self):
        assert self._application.wikiroot is not None

        tagslist = TagsList(self._application.wikiroot)
        self._generalPanel.tagsSelector.setTagsList(tagslist)

    def _setComboPageType(self, pageTypeString):
        """
        Установить тип страницы в диалоге по строке, описывающей тип страницы
        """
        typeCombo = self._generalPanel.typeCombo
        for n in range(typeCombo.GetCount()):
            if typeCombo.GetClientData(n).getTypeString() == pageTypeString:
                typeCombo.SetSelection(n)

    def __onPageTypeChanged(self, event):
        eventParams = PageDialogPageTypeChangedParams(
            self._dialog,
            self.selectedFactory.getPageType().getTypeString())

        self._application.onPageDialogPageTypeChanged(
            self._application.selectedPage,
            eventParams)

    def __onPageTitleChanged(self, event):
        eventParams = PageDialogPageTitleChangedParams(
            self._dialog,
            self.pageTitle)

        self._application.onPageDialogPageTitleChanged(
            self._application.selectedPage,
            eventParams)

    def __onPageOrderChanged(self, event):
        eventParams = PageDialogNewPageOrderChangedParams(
            self._dialog,
            self.orderCalculator)

        self._application.onPageDialogNewPageOrderChanged(
            self._application.selectedPage,
            eventParams)

    def __onTagsListChanged(self, event):
        eventParams = PageDialogPageTagsChangedParams(
            self._dialog,
            self.tags)

        self._application.onPageDialogPageTagsChanged(
            self._application.selectedPage,
            eventParams)
