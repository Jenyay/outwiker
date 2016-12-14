# -*- coding: UTF-8 -*-

from collections import namedtuple

import wx
from wx.lib.newevent import NewEvent

from outwiker.core.event import Event
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.texteditorbase import TextEditorBase

from snippets.snippetparser import SnippetParser
from snippets.gui.snippeteditor import SnippetEditor
from snippets.i18n import get_


FinishDialogParams = namedtuple('FinishDialogParams', ['text'])

VarChangeEvent, EVT_VAR_CHANGE = NewEvent()


class VariablesDialog(TestedDialog):
    '''
    Dialog to enter variables and preview result
    '''
    def __init__(self, parent):
        super(VariablesDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        global _
        _ = get_()

        self._width = 700
        self._height = 400
        self._createGUI()
        self.SetTitle(u'Snippet variables')

    def _createGUI(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(0)

        self._notebook = wx.Notebook(self)

        # Result panel
        self._resultEditor = TextEditorBase(self._notebook)
        self._notebook.AddPage(self._resultEditor, _(u'Preview'))

        # Snippet panel
        self._snippetEditor = SnippetEditor(self._notebook)
        self._notebook.AddPage(self._snippetEditor, _(u'Snippet'))

        # Panel with variables
        self._varPanel = VaraiblesPanel(self)

        # OK / Cancel buttons
        self.ok_button = wx.Button(self, wx.ID_OK)
        self.ok_button.SetDefault()

        btn_sizer = self.CreateStdDialogButtonSizer(wx.CANCEL)
        btn_sizer.Add(self.ok_button)

        mainSizer.Add(self._varPanel, 1, flag=wx.ALL | wx.EXPAND, border=2)
        mainSizer.Add(self._notebook,
                      1,
                      flag=wx.ALL | wx.EXPAND,
                      border=2)
        mainSizer.AddStretchSpacer()
        mainSizer.Add(btn_sizer,
                      flag=wx.ALL | wx.ALIGN_RIGHT,
                      border=2)

        self.SetSizer(mainSizer)
        self.SetClientSize((self._width, self._height))
        self.Layout()

    def setSnippetText(self, text):
        self._snippetEditor.SetReadOnly(False)
        self._snippetEditor.SetText(text)
        self._snippetEditor.SetReadOnly(True)
        self._varPanel.clear()

    def addStringVariable(self, varname):
        self._varPanel.addStringVariable(varname)
        self.Layout()

    def setStringVariable(self, varname, value):
        self._varPanel.setVarString(varname, value)

    def getVarDict(self):
        return self._varPanel.getVarDict()

    def setResult(self, text):
        self._resultEditor.SetText(text)

    def getResult(self):
        return self._resultEditor.GetText()


class VariablesDialogController(object):
    '''
    Controller to manage VariablesDialog.
    '''
    def __init__(self, application):
        self._application = application

        self.onFinishDialogEvent = Event()
        self._parser = None
        self._selectedText = u''

        self._dialog = VariablesDialog(self._application.mainWindow)
        self._dialog.ok_button.Bind(wx.EVT_BUTTON, handler=self._onOk)
        self._dialog.Bind(EVT_VAR_CHANGE, handler=self._onVarChange)

    def ShowDialog(self, selectedText, template, dirname):
        self._selectedText = selectedText
        self._parser = SnippetParser(template, dirname, self._application)
        variables_list = self._parser.getVariables()

        # Get non builtin variables
        variables = sorted([var for var
                            in variables_list
                            if not var.startswith('__')])

        self._dialog.setSnippetText(template)
        map(lambda var: self._dialog.addStringVariable(var), variables)

        # Show dialog if user must enter variable's values
        self._updateResult()
        if variables:
            self._dialog.Show()
        else:
            self.FinishDialog()

    def destroy(self):
        self.onFinishDialogEvent.clear()
        self._dialog.ok_button.Unbind(wx.EVT_BUTTON, handler=self._onOk)
        self._dialog.Unbind(EVT_VAR_CHANGE, handler=self._onVarChange)
        self._dialog.Close()
        self._dialog.Destroy()

    def FinishDialog(self):
        text = self.GetResult()
        self.onFinishDialogEvent(FinishDialogParams(text))
        self._dialog.Close()

    def CloseDialog(self):
        self._dialog.Close()

    def GetResult(self):
        return self._dialog.getResult()

    def _onOk(self, event):
        self.FinishDialog()

    def _onVarChange(self, event):
        self._updateResult()

    def _updateResult(self):
        variables = self._dialog.getVarDict()
        text = self._parser.process(self._selectedText,
                                    self._application.selectedPage,
                                    **variables)
        self._dialog.setResult(text)


class VaraiblesPanel(wx.ScrolledWindow):
    '''
    Panel with controls to enter variables from snippet.
    '''
    def __init__(self, parent):
        super(VaraiblesPanel, self).__init__(parent)

        # List of the tuples. First element - variable's name,
        # second element - Control to enter variable's value
        self._varControls = []

        self._mainSizer = wx.FlexGridSizer(cols=1)
        self._mainSizer.AddGrowableCol(0)
        self.SetSizer(self._mainSizer)

    def addStringVariable(self, varname):
        newCtrl = StringVariableCtrl(self, varname)
        self._varControls.append((varname, newCtrl))
        self._mainSizer.Add(newCtrl, 1, flag=wx.EXPAND | wx.ALL, border=2)
        self.Layout()

        selfSize = self.GetClientSize()
        lastItemRect = self._varControls[-1][1].GetRect()
        self.SetVirtualSize((selfSize[0], lastItemRect.GetBottom()))
        self.SetScrollRate(0, 20)

    def getVarDict(self):
        return {item[0]: item[1].GetValue() for item in self._varControls}

    def setVarString(self, varname, value):
        ctrl = self._findControl(varname)
        ctrl.SetValue(value)

    def _findControl(self, varname):
        for item in self._varControls:
            if varname == item[0]:
                return item[1]

        raise KeyError

    def clear(self):
        self._mainSizer.Clear()
        map(lambda item: item[1].Destroy(), self._varControls)
        self._varControls = []


class StringVariableCtrl(wx.Panel):
    '''
    Control to edit string variable
    '''
    def __init__(self, parent, varname):
        super(StringVariableCtrl, self).__init__(parent)
        self._varname = varname

        self._createGUI()

    def _createGUI(self):
        self._label = wx.StaticText(self, label=self._varname)
        self._textCtrl = wx.TextCtrl(self)
        self._textCtrl.Bind(wx.EVT_TEXT, handler=self._onTextEdit)

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)

        mainSizer.Add(self._label, flag=wx.ALL, border=2)
        mainSizer.Add(self._textCtrl, flag=wx.EXPAND | wx.ALL, border=2)

        self.SetSizer(mainSizer)
        self.Layout()

    def GetValue(self):
        return self._textCtrl.GetValue()

    def SetValue(self, value):
        self._textCtrl.SetValue(value)

    def _onTextEdit(self, event):
        propagationLevel = 10
        newevent = VarChangeEvent()
        newevent.ResumePropagation(propagationLevel)
        wx.PostEvent(self, newevent)
