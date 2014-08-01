# -*- coding: UTF-8 -*-

import wx

from ..i18n import get_
from ..diagramrender import DiagramRender

from .baseparamsdialog import BaseParamsDialog


class InsertDiagramDialog (BaseParamsDialog):
    defaultShape = u"box"

    def __init__ (self, parent):
        super (InsertDiagramDialog, self).__init__ (parent)
        global _
        _ = get_()

        self.SetTitle (_(u"Insert Diagram"))

        self.__createGui()
        self.Fit()
        self.Center(wx.CENTRE_ON_SCREEN)


    def _getShapesList (self):
        return DiagramRender.shapes


    @property
    def isShapeDefault (self):
        """
        Свойство должно вернуть True, если выбрана фигура по умолчанию, и False в противном случае
        """
        return self._shape.GetStringSelection() == self.defaultShape


    def __createGui (self):
        mainSizer = wx.FlexGridSizer (cols = 2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        self._createShapeRow (self, mainSizer)
        self._createBackColorRow (self, mainSizer)
        self._createTextColorRow (self, mainSizer)
        self._createFontSizeRow (self, mainSizer)
        self._createWidthRow (self, mainSizer)
        self._createHeightRow (self, mainSizer)
        self._createOkCancelButtons (mainSizer)

        # Выберем по умолчанию в качестве фигуры box
        boxIndex = self._shape.FindString (self.defaultShape)
        if boxIndex != wx.NOT_FOUND:
            self._shape.SetSelection (boxIndex)

        self.SetSizer (mainSizer)


    def _createNameRow (self, mainSizer):
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



class InsertDiagramController (object):
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
        Возвращает кортеж из строк: (начало викикоманды с параметрами, конец викикоманды)
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return (u"(:diagram:)\n",
                    u"\n(:diagramend:)")
        else:
            return (u"(:diagram:)\n{}\n".format (params),
                    u"\n(:diagramend:)")


    def _getParamString (self, dialog):
        params = []
        params.append (self._getShapeParam (dialog))
        params.append (self._getBackColorParam (dialog))
        params.append (self._getTextColorParam (dialog))
        params.append (self._getFontSizeParam (dialog))
        params.append (self._getWidthParam (dialog))
        params.append (self._getHeightParam (dialog))

        return u"\n".join ([param for param in params if len (param.strip()) != 0])


    def _getShapeParam (self, dialog):
        """
        Возвращает строку с параметром, задающим фигуру
        """
        shape = dialog.shape

        return u"default_shape = {};".format (shape) if not dialog.isShapeDefault else u""


    def _getBackColorParam (self, dialog):
        return u'default_node_color = "{}";'.format (dialog.backColor) if dialog.isBackColorChanged else u""


    def _getTextColorParam (self, dialog):
        return u'default_textcolor = "{}";'.format (dialog.textColor) if dialog.isTextColorChanged else u""


    def _getFontSizeParam (self, dialog):
        return u'default_fontsize = {};'.format (dialog.fontSize) if dialog.isFontSizeChanged else u""


    def _getWidthParam (self, dialog):
        return u'node_width = {};'.format (dialog.width) if dialog.isWidthChanged else u""


    def _getHeightParam (self, dialog):
        return u'node_height = {};'.format (dialog.height) if dialog.isHeightChanged else u""
