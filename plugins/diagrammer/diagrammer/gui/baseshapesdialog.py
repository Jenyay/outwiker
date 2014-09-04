# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty

import wx

from .basedialog import BaseDialog

from ..i18n import get_


class BaseShapesDialog (BaseDialog):
    """
    Базовый класс для диалогов с параметрами
    """
    __metaclass__ = ABCMeta

    def __init__ (self, parent):
        global _
        _ = get_()

        super (BaseShapesDialog, self).__init__ (parent)


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
