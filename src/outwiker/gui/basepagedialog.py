# -*- coding: UTF-8 -*-

import os
import os.path

import wx
import wx.combo

from outwiker.core.factoryselector import FactorySelector
from outwiker.core.application import Application
from outwiker.core.tagslist import TagsList
from outwiker.core.styleslist import StylesList
from outwiker.core.system import getStylesDirList, getIconsDirList
from outwiker.core.iconscollection import IconsCollection
from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT
from .guiconfig import PageDialogConfig
from .iconlistctrl import IconListCtrl
from .tagsselector import TagsSelector


class BasePageDialog(wx.Dialog):
    def __init__(self, parentPage = None, *args, **kwds):
        """
        parentPage - родительская страница (используется, если страницу нужно создавать, а не изменять)
        """
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)

        # Используется для редактирования существующей страницы
        self.currentPage = None

        self.config = PageDialogConfig (Application.config)

        self.notebook = wx.Notebook (self, -1)

        self.generalPanel = GeneralPanel (self.notebook)
        self.iconPanel = IconPanel (self.notebook)
        self.appearancePanel = AppearancePanel (self.notebook)

        self.notebook.AddPage (self.generalPanel, _("General"))
        self.notebook.AddPage (self.iconPanel, _("Icon"))
        self.notebook.AddPage (self.appearancePanel, _("Appearance"))

        self.__set_properties()
        self.__do_layout()

        self.parentPage = parentPage
        self._fillComboType()
        self._setTagsList()

        self.generalPanel.titleTextCtrl.SetFocus()
        self._stylesList = StylesList (getStylesDirList ())
        self.Center(wx.CENTRE_ON_SCREEN)


    def __set_properties(self):
        self.SetTitle(_(u"Create Page"))
        self.SetSize((self.config.width.value, self.config.height.value))


    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)
        mainSizer.Add (self.notebook, 0, wx.EXPAND, 0)
        self._createOkCancelButtons (mainSizer)
        self.SetSizer(mainSizer)

        self.Layout()


    def saveParams (self):
        width, height = self.GetSizeTuple()
        self.config.width.value = width
        self.config.height.value = height

        styleName = self.appearancePanel.styleCombo.GetStringSelection()

        # Не будем изменять стиль по умолчанию в случае,
        # если изменяется существующая страница
        if (self.currentPage is None):
            self.config.recentStyle.value = styleName


    def _fillStyleCombo (self, styleslist, page=None):
        """
        Заполняет self.appearancePanel.styleCombo списком стилей
        styleslist - список путей до загруженных стилей
        page - страница, для которой вызывается диалог. Если page is not None, то первый стиль в списке - это стиль данной страницы
        """
        names = []
        if page is not None:
            names.append (_(u"Do not change"))

        names.append (_(u"Default"))
        style_names = [os.path.basename (style) for style in styleslist]
        style_names.sort()

        names += style_names

        self.appearancePanel.styleCombo.Clear()
        self.appearancePanel.styleCombo.AppendItems (names)

        # Определение последнего используемого стиля
        recentStyle = self.config.recentStyle.value
        names_lower = [name.lower() for name in names]
        try:
            currentStyleIndex = names_lower.index (recentStyle.lower())
        except ValueError:
            currentStyleIndex = 0

        if page is not None:
            # Для уже существующих страниц по умолчанию использовать уже установленный стиль
            currentStyleIndex = 0

        self.appearancePanel.styleCombo.SetSelection (currentStyleIndex)



    def _setTagsList (self):
        assert Application.wikiroot is not None

        tagslist = TagsList (Application.wikiroot)
        self.generalPanel.tagsSelector.setTagsList (tagslist)


    def _createOkCancelButtons (self, sizer):
        # Создание кнопок Ok/Cancel
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 2)
        self.Bind (wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)


    def _fillComboType (self):
        self.generalPanel.typeCombo.Clear()
        for factory in FactorySelector.getFactories():
            self.generalPanel.typeCombo.Append (factory.title, factory)

        if not self.generalPanel.typeCombo.IsEmpty():
            self.generalPanel.typeCombo.SetSelection (0)


    def _setComboPageType (self, pageTypeString):
        """
        Установить тип страницы в диалоге по строке, описывающей тип страницы
        """
        n = 0
        for factory in FactorySelector.getFactories():
            if factory.getTypeString() == FactorySelector.getFactory(pageTypeString).getTypeString():
                self.generalPanel.typeCombo.SetSelection (n)
                break
            n += 1


    @property
    def selectedFactory (self):
        index = self.generalPanel.typeCombo.GetSelection()
        return self.generalPanel.typeCombo.GetClientData (index)


    @property
    def pageTitle (self):
        return self.generalPanel.titleTextCtrl.GetValue().strip()


    @property
    def tags (self):
        return self.generalPanel.tagsSelector.tags


    @property
    def icon (self):
        selection = self.iconPanel.iconsList.getSelection()
        assert len (selection) != 0

        return selection[0]



class GeneralPanel (wx.Panel):
    """
    Класс панели, расположенной на вкладке "Общее"
    """
    def __init__ (self, parent):
        super (GeneralPanel, self).__init__ (parent)

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


class IconPanel (wx.Panel):
    """
    Class of the panel in the "Icon" tab.
    """
    def __init__ (self, parent):
        super (IconPanel, self).__init__ (parent)

        self._iconsCollections = [IconsCollection (path) for path in getIconsDirList()]
        self.__createGui()

        self.__appendGroups ()
        self.groupCtrl.SetSelection (0)
        self.__switchToCurrentGroup()


    def __createGui (self):
        self.iconsList = IconListCtrl (self)
        self.iconsList.SetMinSize((200, 150))

        # Control for selection icons group
        self.groupCtrl = wx.combo.BitmapComboBox (self, style=wx.CB_READONLY)
        self.groupCtrl.Bind (wx.EVT_COMBOBOX, handler=self.__onGroupSelect)

        self.__layout()


    def __layout (self):
        iconSizer = wx.FlexGridSizer(rows=2)
        iconSizer.AddGrowableRow(1)
        iconSizer.AddGrowableCol(0)
        iconSizer.Add(self.groupCtrl, 1, wx.ALL | wx.EXPAND, 2)
        iconSizer.Add(self.iconsList, 1, wx.ALL | wx.EXPAND, 2)

        self.SetSizer (iconSizer)
        self.Layout()


    def __appendGroups (self):
        for n, collection in enumerate (self._iconsCollections):
            # First None is root directory
            for group in [None] + sorted (collection.getGroups(), key=self._localize):
                # Get group name
                if group is None:
                    title = _(u'Not in groups')
                else:
                    title = self._localize(group)

                if n != 0:
                    title += u' *'
                # Every item has tuple (collection index, group name)
                self.groupCtrl.Append (title,
                                       self._getCover (collection, group),
                                       (n, group))



    def _getImageForGroup (self, fname):
        neww = ICON_WIDTH
        newh = ICON_HEIGHT + 2

        wx.Log_EnableLogging(False)
        image = wx.Image (fname)
        wx.Log_EnableLogging(True)

        if not image.IsOk():
            print _(u'Invalid icon file: {}').format (fname)
            return wx.NullBitmap

        posx = (neww - image.Width) / 2
        posy = (newh - image.Height) / 2
        image.Resize ((neww, newh), (posx, posy), 255, 255, 255)

        return wx.BitmapFromImage (image)


    def _getCover (self, collection, groupname):
        """
        Return bitmap for combobox item
        """
        fname = collection.getCover (groupname)
        if fname is not None:
            return self._getImageForGroup (fname)

        return wx.NullBitmap


    def _getRootCover (self):
        """
        Return bitmap for combobox item
        """
        # fname = self._iconsCollections[0].getCover (None)
        fname = None
        for collection in self._iconsCollections:
            cover = collection.getCover (None)
            if cover is not None:
                fname = cover

        if fname is not None:
            return self._getImageForGroup (fname)

        return wx.NullBitmap


    def __onGroupSelect (self, event):
        self.__switchToCurrentGroup()


    def __getCurrentIcons (self):
        index, groupname = self.groupCtrl.GetClientData (self.groupCtrl.GetSelection())

        icons = self._iconsCollections[index].getIcons (groupname)
        icons.sort()

        return icons


    def __switchToCurrentGroup (self):
        icons = self.__getCurrentIcons()
        icons.sort (key=os.path.basename)
        self.iconsList.setIconsList (icons)


    def _localize (self, groupname):
        name = _(groupname)
        return name.capitalize()


class AppearancePanel (wx.Panel):
    def __init__ (self, parent):
        super (AppearancePanel, self).__init__ (parent)

        self.styleText = wx.StaticText (self, -1, _("Page style"))
        self.styleCombo = wx.ComboBox (self,
                                       -1,
                                       choices=[],
                                       style=wx.CB_DROPDOWN | wx.CB_DROPDOWN | wx.CB_READONLY)

        self.__layout ()


    def __layout (self):
        styleSizer = wx.FlexGridSizer (1, 2, 0, 0)
        styleSizer.AddGrowableCol (1)
        styleSizer.Add (self.styleText, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 4)
        styleSizer.Add (self.styleCombo, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 4)

        self.SetSizer (styleSizer)
        self.Layout()
