# -*- coding: UTF-8 -*-

import wx


class PropertyFactory (object):
    """
    Класс для создания элементов управления для свойств, общих для разных диалогов
    """
    @staticmethod
    def bindEnabled (parent, checkbox, control):
        def handler (event):
            control.Enabled = checkbox.GetValue()

        parent.Bind (wx.EVT_CHECKBOX,
                     handler = handler,
                     source = checkbox)

    @staticmethod
    def createLabel (obj, parent, optionsSizer, label):
        """
        Создать элементы для ввода имени узла
        """
        def getter (self):
            return self._label.GetValue()


        def setter (self, value):
            self._label.SetValue (value)

        labelLabel = wx.StaticText (parent, label = label)
        obj._label = wx.TextCtrl (parent)

        optionsSizer.Add (labelLabel,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (obj._label,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )

        type (obj).label = property (getter, setter)


    @staticmethod
    def createBackColor (obj, parent, optionsSizer, label):
        """
        Создать элементы для выбора цвета фона узла
        """
        def isBackColorChangedGetter (self):
            return self._backColorCheckBox.GetValue()


        def isBackColorChangedSetter (self, value):
            self._backColorCheckBox.SetValue (value)


        def backColorGetter (self):
            return self._backColor.GetColour().GetAsString (wx.C2S_NAME | wx.C2S_HTML_SYNTAX)


        def backColorSetter (self, value):
            self._backColor.SetColour (value)


        obj._backColorCheckBox = wx.CheckBox (parent, label = label)

        obj._backColor = wx.ColourPickerCtrl (parent,
                                              col=u"white")

        obj._backColorCheckBox.SetValue (False)
        obj._backColor.Enabled = False

        optionsSizer.Add (obj._backColorCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (obj._backColor,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )

        PropertyFactory.bindEnabled (obj, obj._backColorCheckBox, obj._backColor)

        type(obj).isBackColorChanged = property (isBackColorChangedGetter, isBackColorChangedSetter)
        type(obj).backColor = property (backColorGetter, backColorSetter)


    @staticmethod
    def createFontSize (obj, parent, optionsSizer, label):
        """
        Создать элементы для выбора размера шрифта
        """
        def fontSizeGetter (self):
            return self._fontSize.GetValue()


        def fontSizeSetter (self, value):
            self._fontSize.SetValue (value)


        def isFontSizeChangedGetter (self):
            return self._fontSizeCheckBox.GetValue()


        def isFontSizeChangedSetter (self, value):
            self._fontSizeCheckBox.SetValue (value)


        obj._fontSizeCheckBox = wx.CheckBox (parent, label = label)

        obj._fontSize = wx.SpinCtrl (parent,
                                     min = 1,
                                     max = 100,
                                     initial = 11)

        obj._fontSizeCheckBox.SetValue (False)
        obj._fontSize.Enabled = False

        optionsSizer.Add (obj._fontSizeCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (obj._fontSize,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )

        PropertyFactory.bindEnabled (obj, obj._fontSizeCheckBox, obj._fontSize)

        type (obj).fontSize = property (fontSizeGetter, fontSizeSetter)
        type (obj).isFontSizeChanged = property (isFontSizeChangedGetter, isFontSizeChangedSetter)


    @staticmethod
    def createWidth (obj, parent, optionsSizer, label):
        """
        Создать элементы для выбора ширины узла
        """
        def widthGetter (self):
            return self._width.GetValue()


        def widthSetter (self, value):
            self._width.SetValue (value)


        def isWidthChangedGetter (self):
            return self._widthCheckBox.GetValue()


        def isWidthChangedSetter (self, value):
            self._widthCheckBox.SetValue (value)


        obj._widthCheckBox = wx.CheckBox (parent, label = label)

        obj._width = wx.SpinCtrl (parent,
                                  min = 1,
                                  max = 1000,
                                  initial = 128)

        obj._widthCheckBox.SetValue (False)
        obj._width.Enabled = False

        optionsSizer.Add (obj._widthCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (obj._width,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )

        PropertyFactory.bindEnabled (obj, obj._widthCheckBox, obj._width)

        type (obj).width = property (widthGetter, widthSetter)
        type (obj).isWidthChanged = property (isWidthChangedGetter, isWidthChangedSetter)


    @staticmethod
    def createHeight (obj, parent, optionsSizer, label):
        """
        Создать элементы для выбора высоты узла
        """
        def isHeightChangedGetter (self):
            return self._heightCheckBox.GetValue()


        def isHeightChangedSetter (self, value):
            self._heightCheckBox.SetValue (value)


        def heightGetter (self):
            return self._height.GetValue()


        def heightSetter (self, value):
            self._height.SetValue (value)


        obj._heightCheckBox = wx.CheckBox (parent, label = label)

        obj._height = wx.SpinCtrl (parent,
                                   min = 1,
                                   max = 1000,
                                   initial = 40)

        obj._heightCheckBox.SetValue (False)
        obj._height.Enabled = False

        optionsSizer.Add (obj._heightCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (obj._height,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )

        PropertyFactory.bindEnabled (obj, obj._heightCheckBox, obj._height)

        type (obj).height = property (heightGetter, heightSetter)
        type (obj).isHeightChanged = property (isHeightChangedGetter, isHeightChangedSetter)


    @staticmethod
    def createTextColor (obj, parent, optionsSizer, label):
        """
        Создать элементы для выбора цвета текста узла
        """
        def isTextColorChangedGetter (self):
            return self._textColorCheckBox.GetValue()


        def isTextColorChangedSetter (self, value):
            self._textColorCheckBox.SetValue (value)


        def textColorGetter (self):
            return self._textColor.GetColour().GetAsString (wx.C2S_NAME | wx.C2S_HTML_SYNTAX)


        def textColorSetter (self, value):
            self._textColor.SetColour (value)


        obj._textColorCheckBox = wx.CheckBox (parent, label = label)

        obj._textColor = wx.ColourPickerCtrl (parent,
                                              col=u"black")

        obj._textColorCheckBox.SetValue (False)
        obj._textColor.Enabled = False

        optionsSizer.Add (obj._textColorCheckBox,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (obj._textColor,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )

        PropertyFactory.bindEnabled (obj, obj._textColorCheckBox, obj._textColor)
        type (obj).isTextColorChanged = property (isTextColorChangedGetter, isTextColorChangedSetter)
        type (obj).textColor = property (textColorGetter, textColorSetter)


    @staticmethod
    def createOrientation (obj, parent, mainSizer, label):
        """
        Создать элементы управления, связанные с установкой ориентации диаграммы
        """
        obj.orientations = [
            (_(u"Landscape"), u"landscape"),
            (_(u"Portrait"), u"portrait"),
        ]

        def setOrientationSelection (self, index):
            self._orientation.SetSelection(index)


        def orientationGetter (self):
            index = self._orientation.GetSelection()
            assert index != wx.NOT_FOUND

            return self.orientations[index][1]


        orientationLabel = wx.StaticText (parent, label = label)
        obj._orientation = wx.ComboBox (parent, style = wx.CB_DROPDOWN | wx.CB_READONLY)

        obj._orientation.SetMinSize ((250, -1))
        obj._orientation.Clear()
        obj._orientation.AppendItems ([orientation[0] for orientation in obj.orientations])
        obj._orientation.SetSelection (0)

        mainSizer.Add (orientationLabel,
                       flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                       border = 2
                       )

        mainSizer.Add (obj._orientation,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2
                       )

        type (obj).setOrientationSelection = setOrientationSelection
        type (obj).orientation = property (orientationGetter)


    @staticmethod
    def createStacked (obj, parent, optionsSizer, label):
        """
        Создать элементы для параметра stacked
        """
        def stackedGetter (self):
            return self._stacked.GetValue()


        def stackedSetter (self, value):
            self._stacked.SetValue (value)

        optionsSizer.AddSpacer (1)
        obj._stacked = wx.CheckBox (parent, label = label)

        optionsSizer.Add (obj._stacked,
                          flag = wx.ALL | wx.ALIGN_RIGHT,
                          border = 2
                          )

        type (obj).stacked = property (stackedGetter, stackedSetter)


    @staticmethod
    def createStyle (obj, parent, optionsSizer, label):
        """
        Создать элементы для выбора стиля рамки
        """
        stylesList = [
            (_(u"Default"), u""),
            (_(u"Solid"), u"solid"),
            (_(u"Dotted"), u"dotted"),
            (_(u"Dashed"), u"dashed"),
        ]


        def styleGetter (self):
            """
            Возвращает стиль рамки
            """
            index = self._style.GetSelection()
            if index == wx.NOT_FOUND:
                return self._style.GetValue()

            return stylesList[index][1]


        def styleSetter (self, value):
            self._style.SetValue (value)


        def setBorderStyleIndex (self, value):
            self._style.SetSelection (value)


        styleLabel = wx.StaticText (parent, label = label)
        obj._style = wx.ComboBox (parent, style = wx.CB_DROPDOWN)
        styles = [style[0] for style in stylesList]

        obj._style.Clear()
        obj._style.AppendItems (styles)
        obj._style.SetSelection (0)

        optionsSizer.Add (styleLabel,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (obj._style,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )

        type (obj).style = property (styleGetter, styleSetter)
        type (obj).setBorderStyleIndex = setBorderStyleIndex


    @staticmethod
    def createOkCancelButtons (obj, optionsSizer):
        okCancel = obj.CreateButtonSizer (wx.OK | wx.CANCEL)
        optionsSizer.AddStretchSpacer()
        optionsSizer.Add (okCancel,
                          flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                          border=4
                          )
