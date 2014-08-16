# -*- coding: UTF-8 -*-

import wx

from ..i18n import get_
from outwiker.gui.testeddialog import TestedDialog

from .baseshapesdialog import BaseShapesDialog
from .propertyfactory import PropertyFactory


class InsertGroupDialog (TestedDialog):
    def __init__ (self, parent):
        super (InsertGroupDialog, self).__init__ (parent)
        global _
        _ = get_()

        self.SetTitle (_(u"Insert Group"))

        self.__createGui()
        self.Fit()
        self.Center(wx.CENTRE_ON_SCREEN)


    def __createGui (self):
        mainSizer = wx.FlexGridSizer (cols = 2)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableCol (1)

        propFactory = PropertyFactory (self)

        self._name = propFactory.createText (self,
                                             mainSizer,
                                             _(u"Node name"),
                                             "name")

        propFactory.createOrientation (self,
                                       mainSizer,
                                       _(u"Orientation"))

        propFactory.createColor (self,
                                 mainSizer,
                                 _(u"Set background color"),
                                 "#F39903",
                                 "backColor",
                                 "isBackColorChanged")

        propFactory.createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)



class InsertGroupController (object):
    def __init__ (self, dialog):
        """
        dialog - экземпляр класса InsertGroupDialog
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
        name = self._dialog.name.strip()

        begin = u"group"

        if len (name) != 0:
            begin += u" " + name

        begin += u" {\n"

        if len (params) != 0:
            begin += params + u"\n\n\n"

        return (begin, u"\n}")


    def _getParamString (self, dialog):
        params = []
        params.append (self._getBackColorParam (dialog))
        params.append (self._getOrientationParam (dialog))

        return u"\n".join ([param for param in params if len (param.strip()) != 0])


    def _getBackColorParam (self, dialog):
        return u'color = "{}";'.format (dialog.backColor) if dialog.isBackColorChanged else u""


    def _getOrientationParam (self, dialog):
        return u'orientation = {};'.format (dialog.orientation) if dialog.orientation != dialog.orientations[0][1] else u""
