# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

import wx

from outwiker.gui.testeddialog import TestedDialog

from ..i18n import get_


class BaseParamsDialog (TestedDialog):
    """
    Базовый класс для диалогов с параметрами
    """
    __metaclass__ = ABCMeta

    def __init__ (self, parent):
        global _
        _ = get_()

        super (BaseParamsDialog, self).__init__ (parent,
                                                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)


    @abstractmethod
    def _getShapesList (self):
        """
        Метод должен вернуть список фигур, который нужно добавить в комбобокс _shape
        """
        pass


    @abstractproperty
    def isShapeDefault (self):
        """
        Свойство должно вернуть True, если выбрана фигура по умолчанию, и False в противном случае
        """
        pass


    def _bindEnabled (self, checkbox, control):
        def handler (event):
            control.Enabled = checkbox.GetValue()

        self.Bind (wx.EVT_CHECKBOX,
                   handler = handler,
                   source = checkbox)

    @property
    def shape (self):
        """
        Возвращает пустую строку, если выбрано значение по умолчанию или строку с именем фигуры
        """
        return self._shape.GetStringSelection() if not self.isShapeDefault else u""


    def setShapeSelection (self, index):
        """
        Выбирает фигуру из списка с заданным номером. 0 - значение по умолчанию.
        Метод используется для тестирования
        """
        self._shape.SetSelection (index)


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


    def _createShapeRow (self, parent, optionsSizer, label):
        """
        Создать элементы для выбора формы узла
        """
        shapeLabel = wx.StaticText (parent, label = label)
        self._shape = wx.ComboBox (parent, style = wx.CB_DROPDOWN | wx.CB_READONLY)

        self._shape.Clear()
        self._shape.AppendItems (self._getShapesList())
        self._shape.SetSelection (0)

        optionsSizer.Add (shapeLabel,
                          flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                          border = 2
                          )

        optionsSizer.Add (self._shape,
                          flag = wx.ALL | wx.EXPAND,
                          border = 2
                          )


    def _createBackColorRow (self, parent, optionsSizer, label):
        """
        Создать элементы для выбора цвета фона узла
        """
        self._backColorCheckBox = wx.CheckBox (parent, label = label)

        self._backColor = wx.ColourPickerCtrl (parent,
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

        self._bindEnabled (self._backColorCheckBox, self._backColor)


    def _createTextColorRow (self, parent, optionsSizer, label):
        """
        Создать элементы для выбора цвета текста узла
        """
        self._textColorCheckBox = wx.CheckBox (parent, label = label)

        self._textColor = wx.ColourPickerCtrl (parent,
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

        self._bindEnabled (self._textColorCheckBox, self._textColor)


    def _createFontSizeRow (self, parent, optionsSizer, label):
        """
        Создать элементы для выбора размера шрифта
        """
        self._fontSizeCheckBox = wx.CheckBox (parent, label = label)

        self._fontSize = wx.SpinCtrl (parent,
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
        self._bindEnabled (self._fontSizeCheckBox, self._fontSize)


    def _createWidthRow (self, parent, optionsSizer, label):
        """
        Создать элементы для выбора ширины узла
        """
        self._widthCheckBox = wx.CheckBox (parent, label = label)

        self._width = wx.SpinCtrl (parent,
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
        self._bindEnabled (self._widthCheckBox, self._width)


    def _createHeightRow (self, parent, optionsSizer, label):
        """
        Создать элементы для выбора высоты узла
        """
        self._heightCheckBox = wx.CheckBox (parent, label = label)

        self._height = wx.SpinCtrl (parent,
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

        self._bindEnabled (self._heightCheckBox, self._height)


    def _createOkCancelButtons (self, optionsSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        optionsSizer.AddStretchSpacer()
        optionsSizer.Add (okCancel,
                          flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                          border=4
                          )
