# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox

from ..i18n import get_
from ..diagramrender import DiagramRender


class InsertNodeDialog (TestedDialog):
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertNodeDialog, self).__init__ (parent,
                                                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
                                                 title=_(u"Insert Node"))

        self._borderStyles = [
            (_(u"Default"), u""),
            (_(u"Solid"), u"solid"),
            (_(u"Dotted"), u"dotted"),
            (_(u"Dashed"), u"dashed"),
        ]

        self.__createGui()
        self._paramsPanel.Collapse()
        self.Fit()

        self.Bind (wx.EVT_BUTTON, self.__onOk, id = wx.ID_OK)
        self.Bind (wx.EVT_COLLAPSIBLEPANE_CHANGED, self.__onPaneChanged)
        self.Bind (wx.EVT_TEXT, self.__onNameChanged, self._name)

        self.__bindEnabled (self._backColorCheckBox, self._backColor)
        self.__bindEnabled (self._textColorCheckBox, self._textColor)
        self.__bindEnabled (self._fontSizeCheckBox, self._fontSize)
        self.__bindEnabled (self._widthCheckBox, self._width)
        self.__bindEnabled (self._heightCheckBox, self._height)

        self.Center(wx.CENTRE_ON_SCREEN)


    def __bindEnabled (self, checkbox, control):
        def handler (event):
            control.Enabled = checkbox.GetValue()

        self.Bind (wx.EVT_CHECKBOX,
                   handler = handler,
                   source = checkbox)


    @property
    def name (self):
        return self._name.GetValue()


    @name.setter
    def name (self, value):
        return self._name.SetValue (value)


    @property
    def shape (self):
        """
        Возвращает пустую строку, если выбрано значение по умолчанию или строку с именем фигуры
        """
        return self._shape.GetStringSelection() if self._shape.GetSelection() != 0 else u""


    def setShapeSelection (self, index):
        """
        Выбирает фигуру из списка с заданным номером. 0 - значение по умолчанию.
        Метод используется для тестирования
        """
        self._shape.SetSelection (index)


    @property
    def borderStyle (self):
        """
        Возвращает стиль рамки
        """
        index = self._borderStyle.GetSelection()
        if index == wx.NOT_FOUND:
            return self._borderStyle.GetValue()

        return self._borderStyles[index][1]


    @borderStyle.setter
    def borderStyle (self, value):
        self._borderStyle.SetValue (value)


    def setBorderStyleIndex (self, value):
        self._borderStyle.SetSelection (value)


    @property
    def stacked (self):
        return self._stacked.GetValue()


    @stacked.setter
    def stacked (self, value):
        self._stacked.SetValue (value)


    @property
    def label (self):
        return self._label.GetValue()


    @label.setter
    def label (self, value):
        self._label.SetValue (value)


    @property
    def isBackColorChanged (self):
        return self._backColorCheckBox.GetValue()


    @isBackColorChanged.setter
    def isBackColorChanged (self, value):
        self._backColorCheckBox.SetValue (value)


    @property
    def backColor (self):
        return self._backColor.GetColour().GetAsString (wx.C2S_NAME | wx.C2S_HTML_SYNTAX)


    @backColor.setter
    def backColor (self, value):
        self._backColor.SetColour (value)


    @property
    def isTextColorChanged (self):
        return self._textColorCheckBox.GetValue()


    @isTextColorChanged.setter
    def isTextColorChanged (self, value):
        self._textColorCheckBox.SetValue (value)


    @property
    def textColor (self):
        return self._textColor.GetColour().GetAsString (wx.C2S_NAME | wx.C2S_HTML_SYNTAX)


    @textColor.setter
    def textColor (self, value):
        self._textColor.SetColour (value)


    @property
    def isFontSizeChanged (self):
        return self._fontSizeCheckBox.GetValue()


    @isFontSizeChanged.setter
    def isFontSizeChanged (self, value):
        self._fontSizeCheckBox.SetValue (value)


    @property
    def fontSize (self):
        return self._fontSize.GetValue()


    @fontSize.setter
    def fontSize (self, value):
        self._fontSize.SetValue (value)


    @property
    def isWidthChanged (self):
        return self._widthCheckBox.GetValue()


    @isWidthChanged.setter
    def isWidthChanged (self, value):
        self._widthCheckBox.SetValue (value)


    @property
    def width (self):
        return self._width.GetValue()


    @width.setter
    def width (self, value):
        self._width.SetValue (value)


    @property
    def isHeightChanged (self):
        return self._heightCheckBox.GetValue()


    @isHeightChanged.setter
    def isHeightChanged (self, value):
        self._heightCheckBox.SetValue (value)


    @property
    def height (self):
        return self._height.GetValue()


    @height.setter
    def height (self, value):
        self._height.SetValue (value)


    def __onPaneChanged (self, event):
        self.Fit()


    def __onNameChanged (self, event):
        self._label.SetValue (self._name.GetValue())


    def __onOk (self, event):
        if len (self.name.strip()) == 0:
            MessageBox (_(u"Node name can't be empty"),
                        u"Node name is empty",
                        wx.ICON_ERROR | wx.OK)
            return

        event.Skip()


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

        self.__createNameRow (mainSizer)
        self.__createShapeRow (optionsSizer)
        self.__createStackedRow (optionsSizer)
        self.__createLabelRow (optionsSizer)
        self.__createBorderStyleRow (optionsSizer)
        self.__createBackColorRow (optionsSizer)
        self.__createTextColorRow (optionsSizer)
        self.__createFontSizeRow (optionsSizer)
        self.__createWidthRow (optionsSizer)
        self.__createHeightRow (optionsSizer)

        self._paramsPanel.GetPane().SetSizer (optionsSizer)

        mainSizer.Add (self._paramsPanel,
                       flag = wx.EXPAND | wx.ALL,
                       border = 2)
        self.__createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)
        self._name.SetFocus()


    def __addSpaceRow (self, optionsSizer):
        size = 20
        optionsSizer.AddSpacer (size)
        optionsSizer.AddSpacer (size)


    def __createNameRow (self, mainSizer):
        """
        Создать элементы для ввода имени узла
        """
        titleLabel = wx.StaticText (self, label = _(u"Node name"))
        self._name = wx.TextCtrl (self)
        self._name.SetMinSize ((250, -1))

        nameSizer = wx.FlexGridSizer (cols=2)
        nameSizer.AddGrowableCol (1)
        nameSizer.AddGrowableRow (0)

        nameSizer.Add (titleLabel,
                       flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border = 2
                       )

        nameSizer.Add (self._name,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2
                       )

        mainSizer.Add (nameSizer,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)


    def __createLabelRow (self, optionsSizer):
        """
        Создать элементы для ввода имени узла
        """
        labelLabel = wx.StaticText (self._paramsPanel.GetPane(), label = _(u"Label"))
        self._label = wx.TextCtrl (self._paramsPanel.GetPane())

        optionsSizer.Add (labelLabel,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._label,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createShapeRow (self, optionsSizer):
        """
        Создать элементы для выбора формы узла
        """
        shapeLabel = wx.StaticText (self._paramsPanel.GetPane(), label = _(u"Shape"))
        self._shape = wx.ComboBox (self._paramsPanel.GetPane(), style = wx.CB_DROPDOWN | wx.CB_READONLY)
        shapes = [_(u"Default")] + DiagramRender.shapes

        self._shape.Clear()
        self._shape.AppendItems (shapes)
        self._shape.SetSelection (0)

        optionsSizer.Add (shapeLabel,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._shape,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createStackedRow (self, optionsSizer):
        """
        Создать элементы для параметра stacked
        """
        optionsSizer.AddSpacer (1)
        self._stacked = wx.CheckBox (self._paramsPanel.GetPane(), label = _(u"Stacked"))

        optionsSizer.Add (self._stacked,
                          flag = wx.ALL | wx.ALIGN_RIGHT,
                          border = 2
                          )


    def __createBorderStyleRow (self, optionsSizer):
        """
        Создать элементы для выбора стиля рамки
        """
        styleLabel = wx.StaticText (self._paramsPanel.GetPane(), label = _(u"Border style"))
        self._borderStyle = wx.ComboBox (self._paramsPanel.GetPane(), style = wx.CB_DROPDOWN)
        styles = [style[0] for style in self._borderStyles]

        self._borderStyle.Clear()
        self._borderStyle.AppendItems (styles)
        self._borderStyle.SetSelection (0)

        optionsSizer.Add (styleLabel,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._borderStyle,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createBackColorRow (self, optionsSizer):
        """
        Создать элементы для выбора цвета фона узла
        """
        self._backColorCheckBox = wx.CheckBox (self._paramsPanel.GetPane(),
                                               label = _(u"Set background color"))

        self._backColor = wx.ColourPickerCtrl (self._paramsPanel.GetPane(),
                                               col=u"white")

        self._backColorCheckBox.SetValue (False)
        self._backColor.Enabled = False

        optionsSizer.Add (self._backColorCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._backColor,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createTextColorRow (self, optionsSizer):
        """
        Создать элементы для выбора цвета текста узла
        """
        self._textColorCheckBox = wx.CheckBox (self._paramsPanel.GetPane(),
                                               label = _(u"Set text color"))

        self._textColor = wx.ColourPickerCtrl (self._paramsPanel.GetPane(),
                                               col=u"black")

        self._textColorCheckBox.SetValue (False)
        self._textColor.Enabled = False

        optionsSizer.Add (self._textColorCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._textColor,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createFontSizeRow (self, optionsSizer):
        """
        Создать элементы для выбора размера шрифта
        """
        self._fontSizeCheckBox = wx.CheckBox (self._paramsPanel.GetPane(),
                                              label = _(u"Set font size"))

        self._fontSize = wx.SpinCtrl (self._paramsPanel.GetPane(),
                                      min = 1,
                                      max = 100,
                                      initial = 11)

        self._fontSizeCheckBox.SetValue (False)
        self._fontSize.Enabled = False

        optionsSizer.Add (self._fontSizeCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._fontSize,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createWidthRow (self, optionsSizer):
        """
        Создать элементы для выбора ширины узла
        """
        self._widthCheckBox = wx.CheckBox (self._paramsPanel.GetPane(),
                                           label = _(u"Set width"))

        self._width = wx.SpinCtrl (self._paramsPanel.GetPane(),
                                   min = 1,
                                   max = 1000,
                                   initial = 128)

        self._widthCheckBox.SetValue (False)
        self._width.Enabled = False

        optionsSizer.Add (self._widthCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._width,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createHeightRow (self, optionsSizer):
        """
        Создать элементы для выбора высоты узла
        """
        self._heightCheckBox = wx.CheckBox (self._paramsPanel.GetPane(),
                                            label = _(u"Set height"))

        self._height = wx.SpinCtrl (self._paramsPanel.GetPane(),
                                    min = 1,
                                    max = 1000,
                                    initial = 40)

        self._heightCheckBox.SetValue (False)
        self._height.Enabled = False

        optionsSizer.Add (self._heightCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._height,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def __createOkCancelButtons (self, optionsSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        optionsSizer.AddStretchSpacer()
        optionsSizer.Add (okCancel,
                          flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                          border=4
                          )



class InsertNodeController (object):
    def __init__ (self, dialog):
        """
        dialog - экземпляр класса InsertNodeDialog
        """
        self._dialog = dialog


    def showDialog (self):
        result = self._dialog.ShowModal()
        return result


    def getResult (self):
        """
        Возвращает строку для создания нового узла в соответствии с параметрами, установленными в диалоге.
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        name = self._getName (self._dialog)
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return name
        else:
            return u"{} [{}];".format (name, params)


    def _getParamString (self, dialog):
        params = []
        params.append (self._getShapeParam (dialog))
        params.append (self._getBorderStyleParam (dialog))
        params.append (self._getStackedParam (dialog))
        params.append (self._getLabelParam (dialog))
        params.append (self._getBackColorParam (dialog))
        params.append (self._getTextColorParam (dialog))
        params.append (self._getFontSizeParam (dialog))
        params.append (self._getWidthParam (dialog))
        params.append (self._getHeightParam (dialog))

        return u", ".join ([param for param in params if len (param.strip()) != 0])


    def _getName (self, dialog):
        if u" " in dialog.name:
            return u'"{}"'.format (dialog.name)

        return dialog.name


    def _getShapeParam (self, dialog):
        """
        Возвращает строку с параметром, задающим фигуру
        """
        shape = dialog.shape

        return u"shape = {}".format (shape) if len (shape) != 0 else u""


    def _getBorderStyleParam (self, dialog):
        """
        Возвращает строку с параметром, задающим стиль рамки
        """
        style = dialog.borderStyle.lower().strip().replace (u" ", u"")

        if len (style) == 0:
            return u""

        if style[0].isdigit():
            return u'style = "{}"'.format (style)

        return u"style = {}".format (style)


    def _getStackedParam (self, dialog):
        return u"stacked" if dialog.stacked else u""


    def _getLabelParam (self, dialog):
        return u'label = "{}"'.format (dialog.label) if dialog.label != dialog.name else u""


    def _getBackColorParam (self, dialog):
        return u'color = "{}"'.format (dialog.backColor) if dialog.isBackColorChanged else u""


    def _getTextColorParam (self, dialog):
        return u'textcolor = "{}"'.format (dialog.textColor) if dialog.isTextColorChanged else u""


    def _getFontSizeParam (self, dialog):
        return u'fontsize = {}'.format (dialog.fontSize) if dialog.isFontSizeChanged else u""


    def _getWidthParam (self, dialog):
        return u'width = {}'.format (dialog.width) if dialog.isWidthChanged else u""


    def _getHeightParam (self, dialog):
        return u'height = {}'.format (dialog.height) if dialog.isHeightChanged else u""
