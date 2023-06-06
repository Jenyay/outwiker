# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import wx
import wx.adv

from ..i18n import get_
from .propertyfactory import PropertyFactory
from .basedialog import BaseDialog


class InsertEdgeDialog(BaseDialog):
    """
    Диалог для выбора параметров ребра
    """

    def __init__(self, parent):
        super(InsertEdgeDialog, self).__init__(parent)

        global _
        _ = get_()

        self.SetTitle(_("Insert edge"))

        self.__createGui()
        self.Fit()
        self.Center(wx.BOTH)

        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.__onPaneChanged)

    def __createGui(self):
        self._paramsPanel = wx.CollapsiblePane(
            self, label=_("Options"), style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE
        )

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(1)

        nameSizer = wx.FlexGridSizer(cols=2)
        nameSizer.AddGrowableCol(1)
        nameSizer.AddGrowableRow(0)

        propFactory = PropertyFactory(self)

        self._firstName = propFactory.createText(
            self, nameSizer, _("First node name"), "firstName"
        )

        self._secondName = propFactory.createText(
            self, nameSizer, _("Second node name"), "secondName"
        )
        mainSizer.Add(nameSizer, flag=wx.ALL | wx.EXPAND, border=2)

        optionsSizer = wx.FlexGridSizer(cols=2)
        optionsSizer.AddGrowableCol(0)
        optionsSizer.AddGrowableCol(1)

        propFactory.createStyle(
            self._paramsPanel.GetPane(), optionsSizer, _("Line style")
        )

        propFactory.createBoolean(
            self._paramsPanel.GetPane(), optionsSizer, _("Thick line"), "thick"
        )

        propFactory.createArrowStyle(
            self._paramsPanel.GetPane(), optionsSizer, _("Arrow style")
        )

        propFactory.createColor(
            self._paramsPanel.GetPane(),
            optionsSizer,
            _("Set line color"),
            "black",
            "lineColor",
            "isLineColorChanged",
        )

        propFactory.createText(
            self._paramsPanel.GetPane(), optionsSizer, _("Label"), "label"
        )

        propFactory.createInteger(
            self._paramsPanel.GetPane(),
            optionsSizer,
            _("Set font size"),
            "fontSize",
            "isFontSizeChanged",
            1,
            100,
            11,
        )

        propFactory.createColor(
            self._paramsPanel.GetPane(),
            optionsSizer,
            _("Set text color"),
            "black",
            "textColor",
            "isTextColorChanged",
        )

        propFactory.createBoolean(
            self._paramsPanel.GetPane(), optionsSizer, _("Folded"), "folded"
        )

        helpLink = wx.adv.HyperlinkCtrl(
            self,
            -1,
            _("Open the documentation page"),
            "http://blockdiag.com/en/blockdiag/attributes/edge.attributes.html",
        )

        self._paramsPanel.GetPane().SetSizer(optionsSizer)

        mainSizer.Add(self._paramsPanel, flag=wx.EXPAND | wx.ALL, border=2)

        mainSizer.Add(helpLink, flag=wx.ALIGN_LEFT | wx.ALL, border=4)

        propFactory.createOkCancelButtons(mainSizer)

        self.SetSizer(mainSizer)
        self._firstName.SetFocus()

    def __onPaneChanged(self, event):
        self.Fit()


class InsertEdgeControllerBase(object, metaclass=ABCMeta):
    def __init__(self, dialog):
        self._dialog = dialog

    @abstractmethod
    def getEdge(self):
        """
        Метод должен возвращать строку, описывающую связь узлов(ребро): "--", "->", "<-", "<->"
        """
        pass

    def showDialog(self):
        result = self._dialog.ShowModal()
        return result

    def getResult(self):
        """
        Возвращает строку для создания ребра в соответствии с параметрами, установленными в диалоге.
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        firstname = self._getFirstName(self._dialog).strip()
        if len(firstname) == 0:
            firstname = _("Node1")

        secondname = self._getSecondName(self._dialog).strip()
        if len(secondname) == 0:
            secondname = _("Node2")

        edge = self.getEdge()
        params = self._getParamString(self._dialog).strip()

        if len(params) == 0:
            return "{firstname} {edge} {secondname}".format(
                firstname=firstname, secondname=secondname, edge=edge
            )
        else:
            return "{firstname} {edge} {secondname} [{params}]".format(
                firstname=firstname, secondname=secondname, edge=edge, params=params
            )

    def _getParamString(self, dialog):
        params = []
        params.append(self._getLabelParam(dialog))
        params.append(self._getFontSizeParam(dialog))
        params.append(self._getLineStyleParam(dialog))
        params.append(self._getThickParam(dialog))
        params.append(self._getArrowStyleParam(dialog))
        params.append(self._getLineColorParam(dialog))
        params.append(self._getTextColorParam(dialog))
        params.append(self._getFoldedParam(dialog))

        return ", ".join([param for param in params if len(param.strip()) != 0])

    def __getNameNotation(self, name):
        if " " in name:
            return '"{}"'.format(name)

        return name

    def _getFirstName(self, dialog):
        return self.__getNameNotation(dialog.firstName)

    def _getSecondName(self, dialog):
        return self.__getNameNotation(dialog.secondName)

    def _getLabelParam(self, dialog):
        return 'label = "{}"'.format(dialog.label) if len(dialog.label) != 0 else ""

    def _getFontSizeParam(self, dialog):
        return (
            "fontsize = {}".format(dialog.fontSize) if dialog.isFontSizeChanged else ""
        )

    def _getLineStyleParam(self, dialog):
        """
        Возвращает строку с параметром, задающим стиль линии
        """
        style = dialog.style.lower().strip().replace(" ", "")

        if len(style) == 0:
            return ""

        if style[0].isdigit():
            return 'style = "{}"'.format(style)

        return "style = {}".format(style)

    def _getArrowStyleParam(self, dialog):
        """
        Возвращает строку с параметром, задающим стиль линии
        """
        style = dialog.arrowStyle.lower().strip().replace(" ", "")

        if len(style) == 0:
            return ""

        if style[0].isdigit():
            return 'hstyle = "{}"'.format(style)

        return "hstyle = {}".format(style)

    def _getLineColorParam(self, dialog):
        return (
            'color = "{}"'.format(dialog.lineColor) if dialog.isLineColorChanged else ""
        )

    def _getTextColorParam(self, dialog):
        return (
            'textcolor = "{}"'.format(dialog.textColor)
            if dialog.isTextColorChanged
            else ""
        )

    def _getThickParam(self, dialog):
        return "thick" if dialog.thick else ""

    def _getFoldedParam(self, dialog):
        return "folded" if dialog.folded else ""


class InsertEdgeControllerNone(InsertEdgeControllerBase):
    def getEdge(self):
        return "--"


class InsertEdgeControllerLeft(InsertEdgeControllerBase):
    def getEdge(self):
        return "<-"


class InsertEdgeControllerRight(InsertEdgeControllerBase):
    def getEdge(self):
        return "->"


class InsertEdgeControllerBoth(InsertEdgeControllerBase):
    def getEdge(self):
        return "<->"
