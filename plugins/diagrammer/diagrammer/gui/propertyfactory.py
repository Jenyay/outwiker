# -*- coding: UTF-8 -*-

import wx

from ..i18n import get_


class PropertyFactory (object):
    """
    Класс для создания элементов управления для свойств, общих для разных диалогов
    """
    def __init__ (self, obj):
        """
        obj - диалог, в который добавляются свойства
        """
        global _
        _ = get_()

        self._obj = obj

        self._orientations = [
            (_(u"Landscape"), u"landscape"),
            (_(u"Portrait"), u"portrait"),
        ]


    @staticmethod
    def bindEnabled (parent, checkbox, control):
        def handler (event):
            control.Enabled = checkbox.GetValue()

        parent.Bind (wx.EVT_CHECKBOX,
                     handler = handler,
                     source = checkbox)


    def createText (self, parent, sizer, label, propName):
        """
        Создать элементы для ввода текста
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

        setattr (type (self._obj), propName, property (getter, setter))

        return _label


    def createColor (self,
                     parent,
                     sizer,
                     label,
                     defaultColor,
                     prop,
                     changeProp):
        """
        Создать элементы для выбора цвета фона узла
        self._obj - объект диалога, для которого добавляются контролы и члены
        sizer - сайзер, куда нужно поместить контролы
        label - имя метки перед свойством
        defaultColor - цвет по умолчанию
        prop - имя свойства, которое будет добавлено в класс объекта self._obj для получения и изменения цвета
        changeProp - имя свойства, котороу будет добавлено в класс объекта self._obj для определения того, что цвет изменился
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

        PropertyFactory.bindEnabled (self._obj, _colorCheckBox, _colorPicker)

        # Добавим свойства с заданными именами
        setattr (type(self._obj),
                 prop,
                 property (colorGetter, colorSetter)
                 )

        setattr (type(self._obj),
                 changeProp,
                 property (isColorChangedGetter, isColorChangedSetter)
                 )

        return (_colorCheckBox, _colorPicker)


    def createInteger (self,
                       parent,
                       sizer,
                       label,
                       propName,
                       changePropName,
                       minVal,
                       maxVal,
                       initialVal):
        """
        Создать элементы для выбора целочисленного параметра
        """
        _checkBox = wx.CheckBox (parent, label = label)
        _checkBox.SetValue (False)

        _spin = wx.SpinCtrl (parent,
                             min = minVal,
                             max = maxVal,
                             initial = initialVal)
        _spin.Enabled = False


        def getter (self):
            return _spin.GetValue()


        def setter (self, value):
            _spin.SetValue (value)


        def isChangedGetter (self):
            return _checkBox.GetValue()


        def isChangedSetter (self, value):
            _checkBox.SetValue (value)


        sizer.Add (_checkBox,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (_spin,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        PropertyFactory.bindEnabled (self._obj, _checkBox, _spin)

        setattr (type (self._obj), propName, property (getter, setter))
        setattr (type (self._obj), changePropName, property (isChangedGetter, isChangedSetter))

        return (_checkBox, _spin)


    def createOrientation (self, parent, sizer, label):
        """
        Создать элементы управления, связанные с установкой ориентации диаграммы
        """
        orientationLabel = wx.StaticText (parent, label = label)
        return self._createOrientation (parent, sizer, orientationLabel)


    def createOrientationChecked (self, parent, sizer, label):
        """
        Создать элементы управления, связанные с установкой ориентации диаграммы.
        При этом добавляется чекбокс, с помощью которого выбитается, нужно ли устанавливать этот параметр
        """
        _checkBox = wx.CheckBox (parent, label = label)
        _checkBox.SetValue (False)

        _comboBox = self._createOrientation (parent, sizer, _checkBox)
        _comboBox.Enabled = False

        def isChangedGetter (self):
            return _checkBox.GetValue()


        def isChangedSetter (self, value):
            _checkBox.SetValue (value)

        PropertyFactory.bindEnabled (self._obj, _checkBox, _comboBox)

        setattr (type (self._obj), "isOrientationChanged", property (isChangedGetter, isChangedSetter))

        return (_checkBox, _comboBox)


    def _createOrientation (self, parent, sizer, labelCtrl):
        """
        Создать элементы управления, связанные с установкой ориентации диаграммы
        """
        self._obj.orientations = self._orientations

        def setOrientationSelection (self, index):
            self._orientation.SetSelection(index)


        def orientationGetter (self):
            index = self._orientation.GetSelection()
            assert index != wx.NOT_FOUND

            return self.orientations[index][1]


        self._obj._orientation = wx.ComboBox (parent, style = wx.CB_DROPDOWN | wx.CB_READONLY)

        self._obj._orientation.SetMinSize ((250, -1))
        self._obj._orientation.Clear()
        self._obj._orientation.AppendItems ([orientation[0] for orientation in self._obj.orientations])
        self._obj._orientation.SetSelection (0)

        sizer.Add (labelCtrl,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (self._obj._orientation,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        type (self._obj).setOrientationSelection = setOrientationSelection
        type (self._obj).orientation = property (orientationGetter)

        return self._obj._orientation


    def createBoolean (self, parent, sizer, label, propName):
        """
        Создать элементы для булевого параметра
        """
        _checkbox = wx.CheckBox (parent, label = label)

        def getter (self):
            return _checkbox.GetValue()


        def setter (self, value):
            _checkbox.SetValue (value)

        sizer.AddSpacer (1)

        sizer.Add (_checkbox,
                   flag = wx.ALL | wx.ALIGN_RIGHT,
                   border = 2
                   )

        setattr (type (self._obj), propName, property (getter, setter))

        return _checkbox


    def createStyle (self, parent, sizer, label):
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
        self._obj._style = wx.ComboBox (parent, style = wx.CB_DROPDOWN)
        styles = [style[0] for style in stylesList]

        self._obj._style.Clear()
        self._obj._style.AppendItems (styles)
        self._obj._style.SetSelection (0)

        sizer.Add (styleLabel,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (self._obj._style,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        type (self._obj).style = property (styleGetter, styleSetter)
        type (self._obj).setStyleIndex = setStyleIndex


    def createArrowStyle (self, parent, sizer, label):
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
        self._obj._arrowStyle = wx.ComboBox (parent, style = wx.CB_DROPDOWN | wx.CB_READONLY)
        styles = [style[0] for style in stylesList]

        self._obj._arrowStyle.Clear()
        self._obj._arrowStyle.AppendItems (styles)
        self._obj._arrowStyle.SetSelection (0)

        sizer.Add (styleLabel,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (self._obj._arrowStyle,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        type (self._obj).arrowStyle = property (styleGetter, styleSetter)
        type (self._obj).setArrowStyleIndex = setArrowStyleIndex


    def createOkCancelButtons (self, sizer):
        okCancel = self._obj.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.AddStretchSpacer()
        sizer.Add (okCancel,
                   flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                   border=4
                   )
