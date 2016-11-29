# -*- coding: UTF-8 -*-

from collections import namedtuple

import wx
from wx.lib.newevent import NewEvent

from outwiker.core.event import Event
from outwiker.gui.testeddialog import TestedDialog

from snippets.snippetparser import SnippetParser
from snippets.gui.snippeteditor import SnippetEditor


FinishDialogParams = namedtuple('FinishDialogParams', ['text'])

VarChangeEvent, EVT_VAR_CHANGE = NewEvent()


class VariablesDialog(TestedDialog):
    def __init__(self, parent, application):
        super(TestedDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        self._application = application
        self._width = 700
        self._height = 400
        self._createGUI()

    def _createGUI(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(0)

        self._notebook = wx.Notebook(self)

        self._snippetPanel = TextPanel(self._notebook, self._application)
        self._snippetPanel.editor.SetReadOnly(True)
        self._notebook.AddPage(self._snippetPanel, _(u'Snippet'))

        self._resultPanel = TextPanel(self._notebook, self._application)
        self._notebook.AddPage(self._resultPanel, _(u'Result'))

        self._varPanel = VaraiblesPanel(self)

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

    def setTemplate(self, text):
        self._snippetPanel.editor.SetReadOnly(False)
        self._snippetPanel.editor.SetText(text)
        self._snippetPanel.editor.SetReadOnly(True)
        self._varPanel.clear()

    def addStringVariable(self, varname):
        self._varPanel.addStringVariable(varname)
        self.Layout()

    def getVarDict(self):
        return self._varPanel.getVarDict()

    def setResult(self, text):
        self._resultPanel.editor.SetText(text)

    def getResult(self):
        return self._resultPanel.editor.GetText()


class VariablesDialogController(object):
    '''
    Controller to manage VariablesDialog.
    '''
    def __init__(self, application):
        self._application = application

        self.onFinishDialog = Event()
        self._dialog = None
        self._parser = None
        self._selectedText = u''

    def _setDialogTemplate(self, template):
        self._dialog.setTemplate(template)

    def ShowDialog(self, selectedText, template):
        if self._application.selectedPage is None:
            return

        if self._dialog is None:
            self._dialog = VariablesDialog(self._application.mainWindow,
                                           self._application)
            self._dialog.ok_button.Bind(wx.EVT_BUTTON, handler=self._onOk)
            self._dialog.Bind(EVT_VAR_CHANGE, handler=self._onVarChange)

        self._selectedText = selectedText
        self._parser = SnippetParser(template, self._application)
        variables = sorted([var for var
                            in self._parser.getVariables()
                            if not var.startswith('__')])

        self._setDialogTemplate(template)
        map(lambda var: self._dialog.addStringVariable(var), variables)

        if variables:
            self._updateResult()
            self._dialog.Show()
        else:
            self._finishDialog()

    def destroy(self):
        self.onFinishDialog.clear()
        if self._dialog is not None:
            self._dialog.ok_button.Unbind(wx.EVT_BUTTON, handler=self._onOk)
            self._dialog.Unbind(EVT_VAR_CHANGE, handle=self._onVarChange)
            self._dialog.Close()
            self._dialog = None

    def _finishDialog(self):
        if self._application.selectedPage is not None:
            text = self._dialog.getResult()
            self.onFinishDialog(FinishDialogParams(text))
        self._dialog.Close()
        self._dialog = None

    def _onOk(self, event):
        self._finishDialog()

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

    def clear(self):
        self._mainSizer.Clear()
        map(lambda item: item[1].Destroy(), self._varControls)
        self._varControls = []


class StringVariableCtrl(wx.Panel):
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

    def _onTextEdit(self, event):
        propagationLevel = 10
        newevent = VarChangeEvent()
        newevent.ResumePropagation(propagationLevel)
        wx.PostEvent(self, newevent)


class TextPanel(wx.Panel):
    '''
    Panel to show snippet source.
    '''
    def __init__(self, parent, application):
        super(TextPanel, self).__init__(parent)

        self._application = application
        self.editor = None

        self._createGUI()

    def _createGUI(self):
        self.editor = SnippetEditor(self, self._application)
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        mainSizer.Add(self.editor,
                      1,
                      flag=wx.ALL | wx.EXPAND,
                      border=2)

        self.SetSizer(mainSizer)
        self.Layout()
