# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog

from .i18n import get_


class InsertDialog (TestedDialog):
    """
    Диалог для вставки команды (:counter:)
    """
    def __init__ (self, parent):
        global _
        _ = get_()

        super (InsertDialog, self).__init__ (parent, 
                style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
                title=u"Counter")

        # Размер отступа
        self._fieldsWidth = 200

        self._createGui()

        self.Bind (wx.EVT_CHECKBOX, handler=self._onSetReset, source=self._startCheckBox)

        self._startCheckBox.SetValue (False)
        self._startValue.Enable (False)

        self._counterName.SetFocus()
        self.Center(wx.CENTRE_ON_SCREEN)


    def _onSetReset (self, event):
        self._startValue.Enable (self._startCheckBox.IsChecked())


    @property
    def countersList (self):
        """
        Список имен счетчиков, взятый из _counterName. Считаем, что _counterName и _parentCounterName содержат один и тот же список имен.
        """
        return self._counterName.GetStrings()


    @countersList.setter
    def countersList (self, value):
        """
        Установить список счетчиков в диалоге. В списке обязательно превым должно присутствовать "пустое" имя. Этот список формируется в InsertDialogController
        """
        assert value[0] == u""

        self._counterName.Clear()
        self._counterName.AppendItems (value)
        self._counterName.SetSelection (0)

        self._parentCounterName.Clear()
        self._parentCounterName.AppendItems (value)
        self._parentCounterName.SetSelection (0)


    @property
    def counterName (self):
        return self._counterName.GetValue()


    @counterName.setter
    def counterName (self, value):
        self._counterName.SetValue (value)


    @property
    def parentName (self):
        return self._parentCounterName.GetValue()


    @parentName.setter
    def parentName (self, value):
        self._parentCounterName.SetValue (value)


    @property
    def separator (self):
        return self._separator.GetValue()


    @separator.setter
    def separator (self, value):
        return self._separator.SetValue (value)


    @property
    def reset (self):
        """
        Нужно ли устанавливать параметр start
        """
        return self._startCheckBox.IsChecked()


    @reset.setter
    def reset (self, value):
        self._startCheckBox.SetValue (value)


    @property
    def start (self):
        return self._startValue.GetValue()


    @start.setter
    def start (self, value):
        self._startValue.SetValue (value)


    @property
    def step (self):
        return self._stepValue.GetValue()


    @step.setter
    def step (self, value):
        self._stepValue.SetValue (value)


    @property
    def hide (self):
        return self._hideCheckBox.IsChecked()


    @hide.setter
    def hide (self, value):
        self._hideCheckBox.SetValue (value)


    def _createGui(self):
        """
        Создать элементы управления
        """
        self._createCounterNameGui ()
        self._createNestedGui ()
        self._createAdvancedGui ()

        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (3)

        mainSizer.Add (self._counterNameSizer,
                flag = wx.ALL | wx.EXPAND,
                border = 4)

        mainSizer.Add (self.nestedBoxSizer,
                flag = wx.ALL | wx.EXPAND,
                border = 4)

        mainSizer.Add (self.advancedBoxSizer,
                flag = wx.ALL | wx.EXPAND,
                border = 4)

        self._createOkCancelButtons (mainSizer)

        self.SetSizer (mainSizer)
        self.Fit()


    def _createAdvancedGui (self):
        """
        Создание остальных элементов управления (сброс счетчика к заданному значению, установка шага счетчика, скрытие счетчика)
        """
        advancedPanel = wx.StaticBox (self, label=_(u"Advanced"))
        
        self._startCheckBox = wx.CheckBox (self, label = _(u"Start count from"))
        self._startValue = wx.SpinCtrl (self, min=-10000, max=10000, initial=1)

        stepLabel = wx.StaticText (self, label = _(u"Step"))
        self._stepValue = wx.SpinCtrl (self, min=-10000, max=10000, initial=1)

        self._hideCheckBox = wx.CheckBox (self, label=_(u"Hide counter"))

        advancedSizer = wx.FlexGridSizer (cols=2)
        advancedSizer.AddGrowableCol (0)
        advancedSizer.AddGrowableCol (1)

        advancedSizer.Add (self._startCheckBox, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)
        
        advancedSizer.Add (self._startValue, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2)

        advancedSizer.Add (stepLabel, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)
        
        advancedSizer.Add (self._stepValue, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2)

        advancedSizer.Add (self._hideCheckBox, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)

        self.advancedBoxSizer = wx.StaticBoxSizer(advancedPanel, wx.VERTICAL)

        self.advancedBoxSizer.Add (advancedSizer,
                flag = wx.ALL | wx.EXPAND,
                border=2)


    def _createNestedGui (self):
        """
        Создание элементов управления, связанных с вложенным счетчиком
        """
        nestedPanel = wx.StaticBox (self, label=_(u"Nested counter"))
        
        parentNameLabel = wx.StaticText (self, label = _(u"Parent counter name"))
        self._parentCounterName = wx.ComboBox (self, style=wx.CB_DROPDOWN)
        self._parentCounterName.SetMinSize ((self._fieldsWidth, -1))

        separatorLabel = wx.StaticText (self, label = _(u"Separator"))
        self._separator = wx.TextCtrl (self, value=u".")

        nestedSizer = wx.FlexGridSizer (cols=2)
        nestedSizer.AddGrowableCol (0)
        nestedSizer.AddGrowableCol (1)

        nestedSizer.Add (parentNameLabel, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)
        
        nestedSizer.Add (self._parentCounterName, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2)

        nestedSizer.Add (separatorLabel, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)
        
        nestedSizer.Add (self._separator, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2)

        self.nestedBoxSizer = wx.StaticBoxSizer(nestedPanel, wx.VERTICAL)
        self.nestedBoxSizer.Add (nestedSizer,
                flag = wx.ALL | wx.EXPAND,
                border=2)



    def _createCounterNameGui (self):
        """
        Создание элементов управления, связанных с вводом имени счетчика
        """
        counterNameLabel = wx.StaticText (self, label = _(u"Counter name"))
        self._counterName = wx.ComboBox (self, style=wx.CB_DROPDOWN)
        self._counterName.SetMinSize ((self._fieldsWidth, -1))

        self._counterNameSizer = wx.FlexGridSizer (cols=2)
        self._counterNameSizer.AddGrowableCol (0)
        self._counterNameSizer.AddGrowableCol (1)

        self._counterNameSizer.Add (counterNameLabel, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                border=2)
        
        self._counterNameSizer.Add (self._counterName, 
                flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                border=2)


    def _createOkCancelButtons (self, mainSizer):
        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer()
        mainSizer.Add (
                okCancel,
                flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                border=4
                )
