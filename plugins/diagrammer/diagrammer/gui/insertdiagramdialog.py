# -*- coding: utf-8 -*-

import wx
import wx.adv

from ..i18n import get_
from ..diagramrender import DiagramRender

from .baseshapesdialog import BaseShapesDialog
from .propertyfactory import PropertyFactory


class InsertDiagramDialog(BaseShapesDialog):
    defaultShape = "box"

    def __init__(self, parent):
        super(InsertDiagramDialog, self).__init__(parent)
        global _
        _ = get_()

        self.SetTitle(_("Insert Diagram"))

        self.__createGui()
        self.Fit()
        self.Center(wx.BOTH)

    def _getShapesList(self):
        return DiagramRender.shapes

    @property
    def isShapeDefault(self):
        """
        Свойство должно вернуть True, если выбрана фигура по умолчанию, и False в противном случае
        """
        return self._shape.GetStringSelection() == self.defaultShape

    def __createGui(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        propFactory = PropertyFactory(self)

        propFactory.createOrientation(self, mainSizer, _("Orientation"))

        self._createShapeRow(self, mainSizer, _("Default nodes shape"))

        propFactory.createColor(
            self,
            mainSizer,
            _("Set default nodes background color"),
            "white",
            "backColor",
            "isBackColorChanged",
        )

        propFactory.createColor(
            self,
            mainSizer,
            _("Set default text color"),
            "black",
            "textColor",
            "isTextColorChanged",
        )

        propFactory.createInteger(
            self,
            mainSizer,
            _("Set default font size"),
            "fontSize",
            "isFontSizeChanged",
            1,
            100,
            11,
        )

        propFactory.createInteger(
            self,
            mainSizer,
            _("Set default nodes width"),
            "width",
            "isWidthChanged",
            1,
            1000,
            128,
        )

        propFactory.createInteger(
            self,
            mainSizer,
            _("Set default nodes height"),
            "height",
            "isHeightChanged",
            1,
            1000,
            40,
        )

        propFactory.createInteger(
            self,
            mainSizer,
            _("Set default horizontal span between nodes"),
            "spanWidth",
            "isSpanWidthChanged",
            0,
            1000,
            64,
        )

        propFactory.createInteger(
            self,
            mainSizer,
            _("Set default vertical span between nodes"),
            "spanHeight",
            "isSpanHeightChanged",
            0,
            1000,
            40,
        )

        helpLink = wx.adv.HyperlinkCtrl(
            self,
            -1,
            _("Open the documentation page"),
            "http://blockdiag.com/en/blockdiag/attributes/diagram.attributes.html",
        )

        mainSizer.Add(helpLink, flag=wx.ALIGN_LEFT | wx.ALL, border=4)

        mainSizer.AddSpacer(1)

        propFactory.createOkCancelButtons(mainSizer)

        # Выберем по умолчанию в качестве фигуры box
        boxIndex = self._shape.FindString(self.defaultShape)
        if boxIndex != wx.NOT_FOUND:
            self._shape.SetSelection(boxIndex)

        self.SetSizer(mainSizer)


class InsertDiagramController(object):
    def __init__(self, dialog):
        """
        dialog - экземпляр класса InsertNodeDialog
        """
        self._dialog = dialog

    def showDialog(self):
        result = self._dialog.ShowModal()
        return result

    def getResult(self):
        """
        Возвращает кортеж из строк: (начало викикоманды с параметрами, конец викикоманды)
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        params = self._getParamString(self._dialog).strip()

        if len(params) == 0:
            return ("(:diagram:)\n", "\n(:diagramend:)")
        else:
            return ("(:diagram:)\n{}\n".format(params), "\n(:diagramend:)")

    def _getParamString(self, dialog):
        params = []
        params.append(self._getOrientationParam(dialog))
        params.append(self._getShapeParam(dialog))
        params.append(self._getBackColorParam(dialog))
        params.append(self._getTextColorParam(dialog))
        params.append(self._getFontSizeParam(dialog))
        params.append(self._getWidthParam(dialog))
        params.append(self._getHeightParam(dialog))
        params.append(self._getSpanWidthParam(dialog))
        params.append(self._getSpanHeightParam(dialog))

        return "\n".join([param for param in params if len(param.strip()) != 0])

    def _getShapeParam(self, dialog):
        """
        Возвращает строку с параметром, задающим фигуру
        """
        shape = dialog.shape

        return "default_shape = {};".format(shape) if not dialog.isShapeDefault else ""

    def _getBackColorParam(self, dialog):
        return (
            'default_node_color = "{}";'.format(dialog.backColor)
            if dialog.isBackColorChanged
            else ""
        )

    def _getTextColorParam(self, dialog):
        return (
            'default_textcolor = "{}";'.format(dialog.textColor)
            if dialog.isTextColorChanged
            else ""
        )

    def _getFontSizeParam(self, dialog):
        return (
            "default_fontsize = {};".format(dialog.fontSize)
            if dialog.isFontSizeChanged
            else ""
        )

    def _getWidthParam(self, dialog):
        return "node_width = {};".format(dialog.width) if dialog.isWidthChanged else ""

    def _getHeightParam(self, dialog):
        return (
            "node_height = {};".format(dialog.height) if dialog.isHeightChanged else ""
        )

    def _getSpanWidthParam(self, dialog):
        return (
            "span_width = {};".format(dialog.spanWidth)
            if dialog.isSpanWidthChanged
            else ""
        )

    def _getSpanHeightParam(self, dialog):
        return (
            "span_height = {};".format(dialog.spanHeight)
            if dialog.isSpanHeightChanged
            else ""
        )

    def _getOrientationParam(self, dialog):
        return (
            "orientation = {};".format(dialog.orientation)
            if dialog.orientationIndex != 0
            else ""
        )
