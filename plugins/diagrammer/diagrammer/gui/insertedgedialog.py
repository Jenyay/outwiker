# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

import wx

from outwiker.gui.testeddialog import TestedDialog

from ..i18n import get_
from .propertyfactory import PropertyFactory


class InsertEdgeDialog (TestedDialog):
    """
    Диалог для выбора параметров ребра
    """
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertEdgeDialog, self).__init__ (parent,
                                                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME)

        self.SetTitle (_(u"Insert edge"))

        self.__createGui()
        self.Fit()
        self.Center(wx.CENTRE_ON_SCREEN)

        self.Bind (wx.EVT_COLLAPSIBLEPANE_CHANGED, self.__onPaneChanged)


    def __createGui (self):
        self._paramsPanel = wx.CollapsiblePane (self,
                                                label = _(u"Options"),
                                                style = wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE)

        mainSizer = wx.FlexGridSizer (cols = 1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)

        nameSizer = wx.FlexGridSizer (cols=2)
        nameSizer.AddGrowableCol (1)
        nameSizer.AddGrowableRow (0)

        propFactory = PropertyFactory (self)

        self._firstName = propFactory.createText (self,
                                                  nameSizer,
                                                  _(u"First node name"),
                                                  "firstName")

        self._secondName = propFactory.createText (self,
                                                   nameSizer,
                                                   _(u"Second node name"),
                                                   "secondName")
        mainSizer.Add (nameSizer,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)

        optionsSizer = wx.FlexGridSizer (cols=2)
        optionsSizer.AddGrowableCol (0)
        optionsSizer.AddGrowableCol (1)

        propFactory.createStyle (self._paramsPanel.GetPane(),
                                 optionsSizer,
                                 _(u"Line style"))

        propFactory.createBoolean (self._paramsPanel.GetPane(),
                                   optionsSizer,
                                   _(u"Thick line"),
                                   "thick")

        propFactory.createArrowStyle (self._paramsPanel.GetPane(),
                                      optionsSizer,
                                      _(u"Arrow style"))

        propFactory.createColor (self._paramsPanel.GetPane(),
                                 optionsSizer,
                                 _(u"Set line color"),
                                 "black",
                                 "lineColor",
                                 "isLineColorChanged")

        propFactory.createText (self._paramsPanel.GetPane(),
                                optionsSizer,
                                _(u"Label"),
                                "label")

        propFactory.createInteger (self._paramsPanel.GetPane(),
                                   optionsSizer,
                                   _(u"Set font size"),
                                   "fontSize",
                                   "isFontSizeChanged",
                                   1,
                                   100,
                                   11)

        propFactory.createColor (self._paramsPanel.GetPane(),
                                 optionsSizer,
                                 _(u"Set text color"),
                                 "black",
                                 "textColor",
                                 "isTextColorChanged")

        self._paramsPanel.GetPane().SetSizer (optionsSizer)

        mainSizer.Add (self._paramsPanel,
                       flag = wx.EXPAND | wx.ALL,
                       border = 2)

        propFactory.createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)
        self._firstName.SetFocus()


    def __onPaneChanged (self, event):
        self.Fit()



class InsertEdgeControllerBase (object):
    __metaclass__ = ABCMeta

    def __init__ (self, dialog):
        self._dialog = dialog


    @abstractmethod
    def getEdge (self):
        """
        Метод должен возвращать строку, описывающую связь узлов (ребро): "--", "->", "<-", "<->"
        """
        pass


    def showDialog (self):
        result = self._dialog.ShowModal()
        return result


    def getResult (self):
        """
        Возвращает строку для создания ребра в соответствии с параметрами, установленными в диалоге.
        Считается, что этот метод вызывают после того, как showDialog вернул значение wx.ID_OK
        """
        firstname = self._getFirstName (self._dialog).strip()
        if len (firstname) == 0:
            firstname = _(u"Node1")

        secondname = self._getSecondName (self._dialog).strip()
        if len (secondname) == 0:
            secondname = _(u"Node2")

        edge = self.getEdge()
        params = self._getParamString (self._dialog).strip()

        if len (params) == 0:
            return u"{firstname} {edge} {secondname}".format (firstname = firstname,
                                                              secondname = secondname,
                                                              edge = edge)
        else:
            return u"{firstname} {edge} {secondname} [{params}]".format (firstname = firstname,
                                                                         secondname = secondname,
                                                                         edge = edge,
                                                                         params = params)


    def _getParamString (self, dialog):
        params = []
        params.append (self._getLabelParam (dialog))
        params.append (self._getFontSizeParam (dialog))
        params.append (self._getLineStyleParam (dialog))
        params.append (self._getThickParam (dialog))
        params.append (self._getArrowStyleParam (dialog))
        params.append (self._getLineColorParam (dialog))
        params.append (self._getTextColorParam (dialog))

        return u", ".join ([param for param in params if len (param.strip()) != 0])


    def __getNameNotation (self, name):
        if u" " in name:
            return u'"{}"'.format (name)

        return name


    def _getFirstName (self, dialog):
        return self.__getNameNotation (dialog.firstName)


    def _getSecondName (self, dialog):
        return self.__getNameNotation (dialog.secondName)


    def _getLabelParam (self, dialog):
        return u'label = "{}"'.format (dialog.label) if len (dialog.label) != 0 else u""


    def _getFontSizeParam (self, dialog):
        return u'fontsize = {}'.format (dialog.fontSize) if dialog.isFontSizeChanged else u""


    def _getLineStyleParam (self, dialog):
        """
        Возвращает строку с параметром, задающим стиль линии
        """
        style = dialog.style.lower().strip().replace (u" ", u"")

        if len (style) == 0:
            return u""

        if style[0].isdigit():
            return u'style = "{}"'.format (style)

        return u"style = {}".format (style)


    def _getArrowStyleParam (self, dialog):
        """
        Возвращает строку с параметром, задающим стиль линии
        """
        style = dialog.arrowStyle.lower().strip().replace (u" ", u"")

        if len (style) == 0:
            return u""

        if style[0].isdigit():
            return u'hstyle = "{}"'.format (style)

        return u"hstyle = {}".format (style)


    def _getLineColorParam (self, dialog):
        return u'color = "{}"'.format (dialog.lineColor) if dialog.isLineColorChanged else u""


    def _getTextColorParam (self, dialog):
        return u'textcolor = "{}"'.format (dialog.textColor) if dialog.isTextColorChanged else u""


    def _getThickParam (self, dialog):
        return u"thick" if dialog.thick else u""



class InsertEdgeControllerNone (InsertEdgeControllerBase):
    def getEdge (self):
        return u"--"



class InsertEdgeControllerLeft (InsertEdgeControllerBase):
    def getEdge (self):
        return u"<-"



class InsertEdgeControllerRight (InsertEdgeControllerBase):
    def getEdge (self):
        return u"->"



class InsertEdgeControllerBoth (InsertEdgeControllerBase):
    def getEdge (self):
        return u"<->"
