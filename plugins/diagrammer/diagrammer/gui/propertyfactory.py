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
        _colorPicker = wx.ColourPickerCtrl (parent, colour=defaultColor)

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
        return self.createComboBox (parent,
                                    sizer,
                                    label,
                                    self._orientations,
                                    "orientation",
                                    "orientationIndex")


    def createOrientationChecked (self, parent, sizer, label):
        """
        Создать элементы управления, связанные с установкой ориентации диаграммы.
        При этом добавляется чекбокс, с помощью которого выбитается, нужно ли устанавливать этот параметр
        """
        return self.createComboBoxChecked (parent,
                                           sizer,
                                           label,
                                           self._orientations,
                                           "orientation",
                                           "orientationIndex",
                                           "isOrientationChanged")


    def createComboBoxChecked (self,
                               parent,
                               sizer,
                               label,
                               itemsList,
                               propName,
                               propIndexName,
                               changePropName):
        """
        Создать элементы управления в виде связки CheckBox - Combobox
        parent - родительский контрол
        sizer - родительский сайзер
        label - текст для комбобокса
        itemsList - список кортежей для комбобокса. Первый элемент каждого кортежа - то, что показывается пользователю, второй элемент - то, что будет являться значением параметра
        propName - имя свойства для доступа к значению результата (только для чтения)
        propIndexName - имя свойства для чтения и записи индекса выбранного элемента
        changePropName - имя свойства для чтения / установки того, нужно ли задавать параметр
        """
        _checkBox = wx.CheckBox (parent, label = label)
        _checkBox.SetValue (False)

        _comboBox = self._createComboBox (parent,
                                          sizer,
                                          _checkBox,
                                          itemsList,
                                          propName,
                                          propIndexName)

        _comboBox.Enabled = False

        def isChangedGetter (self):
            return _checkBox.GetValue()


        def isChangedSetter (self, value):
            _checkBox.SetValue (value)

        PropertyFactory.bindEnabled (self._obj, _checkBox, _comboBox)

        setattr (type (self._obj), changePropName, property (isChangedGetter, isChangedSetter))

        return (_checkBox, _comboBox)


    def createComboBox (self, parent, sizer, label, itemsList, propName, propIndexName):
        """
        Создать элементы управления в виде связки StaticText - Combobox
        """
        orientationLabel = wx.StaticText (parent, label = label)

        return self._createComboBox (parent,
                                     sizer,
                                     orientationLabel,
                                     itemsList,
                                     propName,
                                     propIndexName)


    def _createComboBox (self, parent, sizer, labelCtrl, itemsList, propName, propIndexName):
        """
        Создать элементы управления, связанные с установкой ориентации диаграммы
        itemsList - список кортежей для заполнения списка. Первый элемент - то, что видит пользователь, второй элемент - значение создаваемого параметра.
        """
        _comboBox = wx.ComboBox (parent, style = wx.CB_DROPDOWN | wx.CB_READONLY)

        def getter (self):
            index = _comboBox.GetSelection()
            assert index != wx.NOT_FOUND

            return itemsList[index][1]


        def getterIndex (self):
            return _comboBox.GetSelection()


        def setterIndex (self, index):
            _comboBox.SetSelection(index)


        _comboBox.SetMinSize ((250, -1))
        _comboBox.Clear()
        _comboBox.AppendItems ([item[0] for item in itemsList])
        _comboBox.SetSelection (0)

        sizer.Add (labelCtrl,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (_comboBox,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        setattr (type (self._obj), propName, property (getter))
        setattr (type (self._obj), propIndexName, property (getterIndex, setterIndex))

        return _comboBox


    def createBoolean (self, parent, sizer, label, propName):
        """
        Создать элементы для булевого параметра
        """
        _checkbox = wx.CheckBox (parent, label = label)

        def getter (self):
            return _checkbox.GetValue()


        def setter (self, value):
            _checkbox.SetValue (value)

        sizer.Add (_checkbox,
                   flag = wx.ALL | wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.AddSpacer (1)

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

        _style = wx.ComboBox (parent, style = wx.CB_DROPDOWN)


        def styleGetter (self):
            """
            Возвращает стиль рамки
            """
            index = _style.GetSelection()
            if index == wx.NOT_FOUND:
                return _style.GetValue()

            return stylesList[index][1]


        def styleSetter (self, value):
            _style.SetSelection (wx.NOT_FOUND)
            _style.SetValue (value)


        def setStyleIndex (self, value):
            _style.SetSelection (value)


        styleLabel = wx.StaticText (parent, label = label)
        styles = [style[0] for style in stylesList]

        _style.Clear()
        _style.AppendItems (styles)
        _style.SetSelection (0)

        sizer.Add (styleLabel,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2
                   )

        sizer.Add (_style,
                   flag = wx.ALL | wx.EXPAND,
                   border = 2
                   )

        type (self._obj).style = property (styleGetter, styleSetter)
        type (self._obj).setStyleIndex = setStyleIndex

        return _style


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
