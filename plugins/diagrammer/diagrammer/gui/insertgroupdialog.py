# -*- coding: utf-8 -*-

import wx
import wx.adv

from ..i18n import get_

from .propertyfactory import PropertyFactory
from .basedialog import BaseDialog


class InsertGroupDialog(BaseDialog):
    def __init__(self, parent):
        super(InsertGroupDialog, self).__init__(parent)
        global _
        _ = get_()

        self.SetTitle(_("Insert Group"))

        self._borderShapes = [
            (_("Box"), "box"),
            (_("Line"), "line"),
        ]

        self.__createGui()
        self.Fit()
        self.Center(wx.BOTH)

    def __createGui(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        propFactory = PropertyFactory(self)

        self._name = propFactory.createText(self, mainSizer, _("Node name"), "name")

        propFactory.createText(self, mainSizer, _("Label"), "label")

        propFactory.createOrientationChecked(self, mainSizer, _("Orientation"))

        propFactory.createColor(
            self,
            mainSizer,
            _("Set background color"),
            "#F39903",
            "backColor",
            "isBackColorChanged",
        )

        propFactory.createColor(
            self,
            mainSizer,
            _("Set text color"),
            "black",
            "textColor",
            "isTextColorChanged",
        )

        propFactory.createComboBoxChecked(
            self,
            mainSizer,
            _("Border shape"),
            self._borderShapes,
            "borderShape",
            "borderShapeIndex",
            "isBorderShapeChanged",
        )

        propFactory.createStyle(self, mainSizer, _("Border style"))

        helpLink = wx.adv.HyperlinkCtrl(
            self,
            -1,
            _("Open the documentation page"),
            "http://blockdiag.com/en/blockdiag/examples.html#grouping-nodes",
        )

        mainSizer.Add(helpLink, flag=wx.ALIGN_LEFT | wx.ALL, border=4)

        mainSizer.AddSpacer(1)

        propFactory.createOkCancelButtons(mainSizer)

        self.SetSizer(mainSizer)


class InsertGroupController(object):
    def __init__(self, dialog):
        """
        dialog - экземпляр класса InsertGroupDialog
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
        params = self._getParamString(self._dialog)
        name = self._dialog.name.strip()

        begin = "group"

        if len(name) != 0:
            begin += " " + name

        begin += " {\n"

        if len(params) != 0:
            begin += params + "\n\n"

        begin += "    "

        return (begin, "\n}")

    def _getParamString(self, dialog):
        params = []
        params.append(self._getLabelParam(dialog))
        params.append(self._getBackColorParam(dialog))
        params.append(self._getOrientationParam(dialog))
        params.append(self._getTextColorParam(dialog))
        params.append(self._getBorderShapeParam(dialog))
        params.append(self._getBorderStyleParam(dialog))

        result = "\n    ".join([param for param in params if len(param.strip()) != 0])

        if len(result) != 0:
            result = "    " + result

        return result

    def _getBackColorParam(self, dialog):
        return (
            'color = "{}";'.format(dialog.backColor)
            if dialog.isBackColorChanged
            else ""
        )

    def _getOrientationParam(self, dialog):
        return (
            "orientation = {};".format(dialog.orientation)
            if dialog.isOrientationChanged
            else ""
        )

    def _getLabelParam(self, dialog):
        return 'label = "{}";'.format(dialog.label) if len(dialog.label) != 0 else ""

    def _getTextColorParam(self, dialog):
        return (
            'textcolor = "{}";'.format(dialog.textColor)
            if dialog.isTextColorChanged
            else ""
        )

    def _getBorderShapeParam(self, dialog):
        return (
            "shape = {};".format(dialog.borderShape)
            if dialog.isBorderShapeChanged
            else ""
        )

    def _getBorderStyleParam(self, dialog):
        """
        Возвращает строку с параметром, задающим стиль рамки
        """
        style = dialog.style.lower().strip().replace(" ", "")

        if (
            not dialog.isBorderShapeChanged
            or dialog.borderShapeIndex != 1
            or len(style) == 0
        ):
            return ""

        if style[0].isdigit():
            return 'style = "{}";'.format(style)

        return "style = {};".format(style)
