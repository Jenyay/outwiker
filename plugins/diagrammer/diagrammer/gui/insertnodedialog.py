# -*- coding: UTF-8 -*-

import wx
import wx.adv

from outwiker.core.commands import MessageBox

from ..i18n import get_
from ..diagramrender import DiagramRender

from .baseshapesdialog import BaseShapesDialog
from .propertyfactory import PropertyFactory


class InsertNodeDialog (BaseShapesDialog):
    def __init__ (self, parent):
        super (InsertNodeDialog, self).__init__ (parent)
        global _
        _ = get_()

        self.SetTitle (_(u"Insert Node"))

        self.__createGui()
        self._paramsPanel.Collapse()
        self.Fit()

        self.Bind (wx.EVT_BUTTON, self.__onOk, id = wx.ID_OK)
        self.Bind (wx.EVT_COLLAPSIBLEPANE_CHANGED, self.__onPaneChanged)
        self.Bind (wx.EVT_TEXT, self.__onNameChanged, self._name)

        self.Center(wx.BOTH)


    def _getShapesList (self):
        return [_(u"Default")] + DiagramRender.shapes


    @property
    def isShapeDefault (self):
        """
        Свойство должно вернуть True, если выбрана фигура по умолчанию, и False в противном случае
        """
        return self._shape.GetSelection() == 0


    def __createGui (self):
        self._paramsPanel = wx.CollapsiblePane (self,
                                                label = _(u"Options"),
                                                style = wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)

        mainSizer = wx.FlexGridSizer (cols = 1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)

        optionsSizer = wx.FlexGridSizer (cols=2)
        optionsSizer.AddGrowableCol (0)
        optionsSizer.AddGrowableCol (1)

        nameSizer = wx.FlexGridSizer (cols=2)
        nameSizer.AddGrowableCol (1)
        nameSizer.AddGrowableRow (0)

        propFactory = PropertyFactory (self)

        self._name = propFactory.createText (self,
                                             nameSizer,
                                             _(u"Node name"),
                                             "name")

        mainSizer.Add (nameSizer,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)

        self._label = propFactory.createText (self._paramsPanel.GetPane(),
                                              optionsSizer,
                                              _(u"Label"),
                                              "label")

        self._createShapeRow (self._paramsPanel.GetPane(),
                              optionsSizer,
                              _(u"Shape"))

        propFactory.createBoolean (self._paramsPanel.GetPane(),
                                   optionsSizer,
                                   _(u"Stacked"),
                                   "stacked")

        propFactory.createStyle (self._paramsPanel.GetPane(),
                                 optionsSizer,
                                 _(u"Border style"))

        propFactory.createColor (self._paramsPanel.GetPane(),
                                 optionsSizer,
                                 _(u"Set background color"),
                                 "white",
                                 "backColor",
                                 "isBackColorChanged")

        propFactory.createColor (self._paramsPanel.GetPane(),
                                 optionsSizer,
                                 _(u"Set text color"),
                                 "black",
                                 "textColor",
                                 "isTextColorChanged")

        propFactory.createInteger (self._paramsPanel.GetPane(),
                                   optionsSizer,
                                   _(u"Set font size"),
                                   "fontSize",
                                   "isFontSizeChanged",
                                   1,
                                   100,
                                   11)

        propFactory.createInteger (self._paramsPanel.GetPane(),
                                   optionsSizer,
                                   _(u"Set width"),
                                   "width",
                                   "isWidthChanged",
                                   1,
                                   1000,
                                   128)

        propFactory.createInteger (self._paramsPanel.GetPane(),
                                   optionsSizer,
                                   _(u"Set height"),
                                   "height",
                                   "isHeightChanged",
                                   1,
                                   1000,
                                   40)

        helpLink = wx.adv.HyperlinkCtrl (self,
                                     -1,
                                     _(u"Open the documentation page"),
                                     u"http://blockdiag.com/en/blockdiag/attributes/node.attributes.html")

        self._paramsPanel.GetPane().SetSizer (optionsSizer)

        mainSizer.Add (self._paramsPanel,
                       flag = wx.EXPAND | wx.ALL,
                       border = 2)

        mainSizer.Add (helpLink,
                       flag = wx.ALIGN_LEFT | wx.ALL,
                       border = 4)

        propFactory.createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)
        self._name.SetFocus()


    @property
    def name (self):
        return self._name.GetValue()


    @name.setter
    def name (self, value):
        return self._name.SetValue (value)


    def __onPaneChanged (self, event):
        self.Fit()


    def __onNameChanged (self, event):
        self._label.SetValue (self._name.GetValue())


    def __onOk (self, event):
        if len (self.name.strip()) == 0:
            MessageBox (_(u"Name of a node can't be empty"),
                        u"Name of a node is empty",
                        wx.ICON_ERROR | wx.OK)
            return

        event.Skip()



class InsertNodeController (object):
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
        Возвращает строку для создания нового узла в соответствии с параметрами, установленными в диалоге.
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        name = self._getName (self._dialog)
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return name
        else:
            return u"{} [{}];".format (name, params)


    def _getParamString (self, dialog):
        params = []
        params.append (self._getShapeParam (dialog))
        params.append (self._getBorderStyleParam (dialog))
        params.append (self._getStackedParam (dialog))
        params.append (self._getLabelParam (dialog))
        params.append (self._getBackColorParam (dialog))
        params.append (self._getTextColorParam (dialog))
        params.append (self._getFontSizeParam (dialog))
        params.append (self._getWidthParam (dialog))
        params.append (self._getHeightParam (dialog))

        return u", ".join ([param for param in params if len (param.strip()) != 0])


    def _getName (self, dialog):
        if u" " in dialog.name:
            return u'"{}"'.format (dialog.name)

        return dialog.name


    def _getShapeParam (self, dialog):
        """
        Возвращает строку с параметром, задающим фигуру
        """
        shape = dialog.shape

        return u"shape = {}".format (shape) if len (shape) != 0 else u""


    def _getBorderStyleParam (self, dialog):
        """
        Возвращает строку с параметром, задающим стиль рамки
        """
        style = dialog.style.lower().strip().replace (u" ", u"")

        if len (style) == 0:
            return u""

        if style[0].isdigit():
            return u'style = "{}"'.format (style)

        return u"style = {}".format (style)


    def _getStackedParam (self, dialog):
        return u"stacked" if dialog.stacked else u""


    def _getLabelParam (self, dialog):
        return u'label = "{}"'.format (dialog.label) if dialog.label != dialog.name else u""


    def _getBackColorParam (self, dialog):
        return u'color = "{}"'.format (dialog.backColor) if dialog.isBackColorChanged else u""


    def _getTextColorParam (self, dialog):
        return u'textcolor = "{}"'.format (dialog.textColor) if dialog.isTextColorChanged else u""


    def _getFontSizeParam (self, dialog):
        return u'fontsize = {}'.format (dialog.fontSize) if dialog.isFontSizeChanged else u""


    def _getWidthParam (self, dialog):
        return u'width = {}'.format (dialog.width) if dialog.isWidthChanged else u""


    def _getHeightParam (self, dialog):
        return u'height = {}'.format (dialog.height) if dialog.isHeightChanged else u""
