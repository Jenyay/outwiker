# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

import wx

from outwiker.gui.testeddialog import TestedDialog

from ..i18n import get_


class InsertEdgeDialog (TestedDialog):
    """
    Диалог для выбора параметров ребра
    """
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertEdgeDialog, self).__init__ (parent,
                                                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self.SetTitle (_(u"Insert edge"))

        self.__createGui()
        self.Fit()
        self.Center(wx.CENTRE_ON_SCREEN)

        self.Bind (wx.EVT_COLLAPSIBLEPANE_CHANGED, self.__onPaneChanged)


    def __createGui (self):
        self._paramsPanel = wx.CollapsiblePane (self,
                                                label = _(u"Options"),
                                                style = wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)

        mainSizer = wx.FlexGridSizer (cols = 1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)

        optionsSizer = wx.FlexGridSizer (cols=2)
        optionsSizer.AddGrowableCol (0)
        optionsSizer.AddGrowableCol (1)

        self._createNodesRows (self, mainSizer)
        # self._createLabelRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Label"))
        # self._createShapeRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Shape"))
        # self._createStackedRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Stacked"))
        # self._createBorderStyleRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Border style"))
        # self._createBackColorRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Set background color"))
        # self._createTextColorRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Set text color"))
        # self._createFontSizeRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Set font size"))
        # self._createWidthRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Set width"))
        # self._createHeightRow (self._paramsPanel.GetPane(), optionsSizer, _(u"Set height"))

        self._paramsPanel.GetPane().SetSizer (optionsSizer)

        mainSizer.Add (self._paramsPanel,
                       flag = wx.EXPAND | wx.ALL,
                       border = 2)
        self._createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)
        self._firstName.SetFocus()


    def _createNodesRows (self, parent, sizer):
        """
        Создать элементы для ввода имен узлов
        """
        firstTitleLabel = wx.StaticText (parent, label = _(u"First node name"))
        self._firstName = wx.TextCtrl (parent)
        self._firstName.SetMinSize ((250, -1))

        secondTitleLabel = wx.StaticText (parent, label = _(u"Second node name"))
        self._secondName = wx.TextCtrl (parent)
        self._secondName.SetMinSize ((250, -1))

        nameSizer = wx.FlexGridSizer (cols=2)
        nameSizer.AddGrowableCol (1)
        nameSizer.AddGrowableRow (0)

        nameSizer.Add (firstTitleLabel,
                       flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border = 2
                       )

        nameSizer.Add (self._firstName,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2
                       )

        nameSizer.Add (secondTitleLabel,
                       flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border = 2
                       )

        nameSizer.Add (self._secondName,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2
                       )

        sizer.Add (nameSizer,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2)


    def _createOkCancelButtons (self, optionsSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        optionsSizer.AddStretchSpacer()
        optionsSizer.Add (okCancel,
                          flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                          border=4
                          )


    def __onPaneChanged (self, event):
        self.Fit()


    @property
    def firstName (self):
        return self._firstName.GetValue()


    @firstName.setter
    def firstName (self, value):
        return self._firstName.SetValue (value)


    @property
    def secondName (self):
        return self._secondName.GetValue()


    @secondName.setter
    def secondName (self, value):
        return self._secondName.SetValue (value)



class InsertEdgeControllerBase (object):
    __metaclass__ = ABCMeta

    def __init__ (self, dialog):
        self._dialog = dialog


    @abstractmethod
    def getEdge (self):
        """
        Метод должен возвращать строку, описывающую связь узлов (ребро): "--", "->", "<-", "<->"
        """
        pass


    def showDialog (self):
        result = self._dialog.ShowModal()
        return result


    def getResult (self):
        """
        Возвращает строку для создания ребра в соответствии с параметрами, установленными в диалоге.
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        firstname = self._getFirstName (self._dialog).strip()
        if len (firstname) == 0:
            firstname = _(u"Node1")

        secondname = self._getSecondName (self._dialog).strip()
        if len (secondname) == 0:
            secondname = _(u"Node2")

        edge = self.getEdge()
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return u"{firstname} {edge} {secondname}".format (firstname = firstname,
                                                              secondname = secondname,
                                                              edge = edge)
        else:
            return u"{firstname} {edge} {secondname} [{params}]".format (firstname = firstname,
                                                                         secondname = secondname,
                                                                         edge = edge,
                                                                         params = params)


    def _getParamString (self, dialog):
        params = []
        # params.append (self._getShapeParam (dialog))

        return u", ".join ([param for param in params if len (param.strip()) != 0])


    def __getNameNotation (self, name):
        if u" " in name:
            return u'"{}"'.format (name)

        return name


    def _getFirstName (self, dialog):
        return self.__getNameNotation (dialog.firstName)


    def _getSecondName (self, dialog):
        return self.__getNameNotation (dialog.secondName)



class InsertEdgeControllerNone (InsertEdgeControllerBase):
    def getEdge (self):
        return u"--"



class InsertEdgeControllerLeft (InsertEdgeControllerBase):
    def getEdge (self):
        return u"<-"



class InsertEdgeControllerRight (InsertEdgeControllerBase):
    def getEdge (self):
        return u"->"



class InsertEdgeControllerBoth (InsertEdgeControllerBase):
    def getEdge (self):
        return u"<->"
