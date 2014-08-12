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
    def createText (obj, parent, sizer, label, propName):
        """
        Создать элементы для ввода текста
        obj - диалог, в который добавляются свойства
        parent - родительский контрол
        sizer - родительский сайзер
        label - метка перед полем ввода
        propName - свойство, которое будет добавлено к классу объекта obj для доступа к значению введенного текста
        """
        _label = wx.TextCtrl (parent)
        _label.SetMinSize ((250, -1))

        def getter (self):
            return _label.GetValue()


        def setter (self, value):
            _label.SetValue (value)

        labelLabel = wx.StaticText (parent, label = label)

        sizer.Add (labelLabel,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (_label,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        setattr (type (obj), propName, property (getter, setter))

        return _label


    @staticmethod
    def createColor (obj,
                     parent,
                     sizer,
                     label,
                     defaultColor,
                     prop,
                     changeProp):
        """
        Создать элементы для выбора цвета фона узла
        obj - объект диалога, для которого добавляются контролы и члены
        sizer - сайзер, куда нужно поместить контролы
        label - имя метки перед свойством
        defaultColor - цвет по умолчанию
        prop - имя свойства, которое будет добавлено в класс объекта obj для получения и изменения цвета
        changeProp - имя свойства, котороу будет добавлено в класс объекта obj для определения того, что цвет изменился
        """
        _colorCheckBox = wx.CheckBox (parent, label = label)
        _colorPicker = wx.ColourPickerCtrl (parent, col = defaultColor)

        _colorCheckBox.SetValue (False)
        _colorPicker.Enabled = False

        def isColorChangedGetter (self):
            return _colorCheckBox.GetValue()


        def isColorChangedSetter (self, value):
            _colorCheckBox.SetValue (value)


        def colorGetter (self):
            return _colorPicker.GetColour().GetAsString (wx.C2S_NAME | wx.C2S_HTML_SYNTAX)


        def colorSetter (self, value):
            _colorPicker.SetColour (value)


        sizer.Add (_colorCheckBox,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (_colorPicker,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        PropertyFactory.bindEnabled (obj, _colorCheckBox, _colorPicker)

        # Добавим свойства с заданными именами
        setattr (type(obj),
                 prop,
                 property (colorGetter, colorSetter)
                 )

        setattr (type(obj),
                 changeProp,
                 property (isColorChangedGetter, isColorChangedSetter)
                 )

        return (_colorCheckBox, _colorPicker)


    @staticmethod
    def createFontSize (obj, parent, sizer, label):
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

        sizer.Add (obj._fontSizeCheckBox,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (obj._fontSize,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        PropertyFactory.bindEnabled (obj, obj._fontSizeCheckBox, obj._fontSize)

        type (obj).fontSize = property (fontSizeGetter, fontSizeSetter)
        type (obj).isFontSizeChanged = property (isFontSizeChangedGetter, isFontSizeChangedSetter)


    @staticmethod
    def createWidth (obj, parent, sizer, label):
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

        sizer.Add (obj._widthCheckBox,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (obj._width,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        PropertyFactory.bindEnabled (obj, obj._widthCheckBox, obj._width)

        type (obj).width = property (widthGetter, widthSetter)
        type (obj).isWidthChanged = property (isWidthChangedGetter, isWidthChangedSetter)


    @staticmethod
    def createHeight (obj, parent, sizer, label):
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

        sizer.Add (obj._heightCheckBox,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (obj._height,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        PropertyFactory.bindEnabled (obj, obj._heightCheckBox, obj._height)

        type (obj).height = property (heightGetter, heightSetter)
        type (obj).isHeightChanged = property (isHeightChangedGetter, isHeightChangedSetter)



    @staticmethod
    def createOrientation (obj, parent, sizer, label):
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

        sizer.Add (orientationLabel,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (obj._orientation,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        type (obj).setOrientationSelection = setOrientationSelection
        type (obj).orientation = property (orientationGetter)


    @staticmethod
    def createStacked (obj, parent, sizer, label):
        """
        Создать элементы для параметра stacked
        """
        def stackedGetter (self):
            return self._stacked.GetValue()


        def stackedSetter (self, value):
            self._stacked.SetValue (value)

        sizer.AddSpacer (1)
        obj._stacked = wx.CheckBox (parent, label = label)

        sizer.Add (obj._stacked,
                   flag = wx.ALL | wx.ALIGN_RIGHT,
                   border = 2
                   )

        type (obj).stacked = property (stackedGetter, stackedSetter)


    @staticmethod
    def createStyle (obj, parent, sizer, label):
        """
        Создать элементы для выбора стиля рамки или линии
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


        def setStyleIndex (self, value):
            self._style.SetSelection (value)


        styleLabel = wx.StaticText (parent, label = label)
        obj._style = wx.ComboBox (parent, style = wx.CB_DROPDOWN)
        styles = [style[0] for style in stylesList]

        obj._style.Clear()
        obj._style.AppendItems (styles)
        obj._style.SetSelection (0)

        sizer.Add (styleLabel,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (obj._style,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        type (obj).style = property (styleGetter, styleSetter)
        type (obj).setStyleIndex = setStyleIndex


    @staticmethod
    def createArrowStyle (obj, parent, sizer, label):
        """
        Создать элементы для выбора стиля стрелки
        """
        stylesList = [
            (_(u"Default"), u""),
            (_(u"Generalization"), u"generalization"),
            (_(u"Composition"), u"composition"),
            (_(u"Aggregation"), u"aggregation"),
        ]


        def styleGetter (self):
            """
            Возвращает стиль рамки
            """
            index = self._arrowStyle.GetSelection()
            if index == wx.NOT_FOUND:
                return self._arrowStyle.GetValue()

            return stylesList[index][1]


        def styleSetter (self, value):
            self._arrowStyle.SetValue (value)


        def setArrowStyleIndex (self, value):
            self._arrowStyle.SetSelection (value)


        styleLabel = wx.StaticText (parent, label = label)
        obj._arrowStyle = wx.ComboBox (parent, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        styles = [style[0] for style in stylesList]

        obj._arrowStyle.Clear()
        obj._arrowStyle.AppendItems (styles)
        obj._arrowStyle.SetSelection (0)

        sizer.Add (styleLabel,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (obj._arrowStyle,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        type (obj).arrowStyle = property (styleGetter, styleSetter)
        type (obj).setArrowStyleIndex = setArrowStyleIndex


    @staticmethod
    def createOkCancelButtons (obj, sizer):
        okCancel = obj.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.AddStretchSpacer()
        sizer.Add (okCancel,
                   flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                   border=4
                   )
