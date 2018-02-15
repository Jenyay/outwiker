# -*- coding: utf-8 -*-

from collections import namedtuple
import os

import wx
from wx.lib.newevent import NewEvent

from outwiker.core.event import Event
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.texteditorbase import TextEditorBase

from snippets.snippetparser import SnippetParser
from snippets.gui.snippeteditor import SnippetEditor
from snippets.i18n import get_
from snippets.utils import getSnippetsDir, getImagesPath
from snippets.config import SnippetsConfig


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

        self._shortTemplateName = None
        self._createGUI()
        self.SetTitle(u'Snippet variables')

    def _createGUI(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)

        # Panel with variables
        self._varPanel = VaraiblesPanel(self)
        self._varPanel.Hide()

        self._notebook = wx.Notebook(self)

        # Result panel
        self._resultEditor = TextEditorBase(self._notebook)
        self._notebook.AddPage(self._resultEditor, _(u'Preview'))

        # Snippet panel
        self._snippetEditor = SnippetEditor(self._notebook)
        self._notebook.AddPage(self._snippetEditor, _(u'Snippet'))

        # Checkbox for wiki command
        self._wikiCommandCheckBox = wx.CheckBox(
            self,
            label=_(u'Insert as wiki command'))

        # OK / Cancel buttons
        self.ok_button = wx.Button(self, wx.ID_OK)
        self.ok_button.SetDefault()

        btn_sizer = self.CreateStdDialogButtonSizer(wx.CANCEL)
        btn_sizer.Add(self.ok_button)

        # Fill mainSizer
        self.topPanel = wx.FlexGridSizer(cols=2)
        self.topPanel.AddGrowableCol(0)
        self.topPanel.AddGrowableCol(1)
        self.topPanel.AddGrowableRow(0)

        self.bottomPanel = wx.FlexGridSizer(cols=2)
        self.bottomPanel.AddGrowableCol(0)
        self.bottomPanel.AddGrowableCol(1)
        self.bottomPanel.AddGrowableRow(0)

        self.topPanel.Add(self._varPanel, 1, flag=wx.ALL | wx.EXPAND, border=2)
        self.topPanel.Add(self._notebook,
                          1,
                          flag=wx.ALL | wx.EXPAND,
                          border=2)
        self.bottomPanel.Add(self._wikiCommandCheckBox,
                             flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                             border=2)
        self.bottomPanel.Add(btn_sizer,
                             flag=wx.ALL | wx.ALIGN_RIGHT,
                             border=2)

        mainSizer.Add(self.topPanel, 1, flag=wx.ALL | wx.EXPAND, border=2)
        mainSizer.Add(self.bottomPanel, 1, flag=wx.ALL | wx.EXPAND, border=2)

        self.SetSizer(mainSizer)
        self.Layout()

    def hideVarPanel(self):
        self._varPanel.Hide()
        self.Layout()

    def setSnippetText(self, text):
        self._snippetEditor.SetReadOnly(False)
        self._snippetEditor.SetText(text)
        self._snippetEditor.SetReadOnly(True)
        self._varPanel.clear()

    def addStringVariable(self, varname):
        self._varPanel.Show()
        self._varPanel.addStringVariable(varname)
        self._notebook.MoveAfterInTabOrder(self._varPanel)
        self.Layout()

    def setStringVariable(self, varname, value):
        self._varPanel.setVarString(varname, value)

    def getVarDict(self):
        return self._varPanel.getVarDict()

    def setResult(self, text):
        self._resultEditor.SetText(text)

    def getResult(self):
        return self._resultEditor.GetText()

    def setWikiCommandSetVisible(self, visible):
        if not visible:
            self._wikiCommandCheckBox.SetValue(False)

        self._wikiCommandCheckBox.Show(visible)

    @property
    def wikiCommandChecked(self):
        return self._wikiCommandCheckBox.IsChecked()

    @wikiCommandChecked.setter
    def wikiCommandChecked(self, value):
        self._wikiCommandCheckBox.SetValue(value)

    @property
    def templateFileName(self):
        return self._shortTemplateName

    @templateFileName.setter
    def templateFileName(self, shortTemplateName):
        title = _(u'{} | Snippet variables').format(shortTemplateName)
        self._shortTemplateName = shortTemplateName
        self.SetTitle(title)

    def setFocusToFirstVariable(self):
        self._varPanel.setFocusToFirstVariable()


class VariablesDialogController(object):
    '''
    Controller to manage VariablesDialog.
    '''
    def __init__(self, application):
        self._application = application

        self.onFinishDialogEvent = Event()
        self._parser = None
        self._selectedText = u''
        self._config = SnippetsConfig(self._application.config)
        self._recentSnippetPath = None

        self._dialog = VariablesDialog(self._application.mainWindow)
        self._dialog.ok_button.Bind(wx.EVT_BUTTON, handler=self._onOk)
        self._dialog.Bind(EVT_VAR_CHANGE, handler=self._onVarChange)
        self._dialog.SetClientSize((self._config.variablesDialogWidth,
                                    self._config.variablesDialogHeight))

    @property
    def dialog(self):
        return self._dialog

    def ShowDialog(self, selectedText, template, template_path):
        self._recentSnippetPath = template_path
        dirname = os.path.dirname(template_path)
        self._selectedText = selectedText
        self._parser = SnippetParser(template, dirname, self._application)
        variables_list = self._parser.getVariables()

        # Get non builtin variables
        variables = sorted([var for var
                            in variables_list
                            if not var.startswith('__')])

        self.dialog.hideVarPanel()
        self.dialog.setSnippetText(template)
        [*map(lambda var: self.dialog.addStringVariable(var), variables)]

        shortTemplateName = self._getShortTemplateName(template_path)
        self.dialog.templateFileName = shortTemplateName
        self.dialog.wikiCommandChecked = False

        # Show dialog if user must enter variable's values
        self._updateResult()
        if (self._application.selectedPage is not None and
                self._application.selectedPage.getTypeString() == u'wiki'):
            self.dialog.setWikiCommandSetVisible(True)
        else:
            self.dialog.setWikiCommandSetVisible(False)

        self.dialog.setFocusToFirstVariable()
        self.dialog.Show()

    def _getShortTemplateName(self, template_fname):
        '''
        Convert full template path to short path
        '''
        snippets_dir = getSnippetsDir()
        shortTemplateName = template_fname

        if shortTemplateName.startswith(snippets_dir):
            shortTemplateName = shortTemplateName[len(snippets_dir) + 1:]

        shortTemplateName = shortTemplateName.replace(u'\\', u'/')
        return shortTemplateName

    def destroy(self):
        self.onFinishDialogEvent.clear()
        self.dialog.ok_button.Unbind(wx.EVT_BUTTON, handler=self._onOk)
        self.dialog.Unbind(EVT_VAR_CHANGE, handler=self._onVarChange)
        self.dialog.Close()
        self.dialog.Destroy()

    def FinishDialog(self):
        try:
            w, h = self._dialog.GetClientSize()
            self._config.variablesDialogWidth = w
            self._config.variablesDialogHeight = h
            self._config.recentSnippet = self._recentSnippetPath
        except EnvironmentError:
            pass

        text = self.GetResult()
        self.onFinishDialogEvent(FinishDialogParams(text))
        self.dialog.Close()

    def CloseDialog(self):
        self.dialog.Close()

    def GetResult(self):
        if not self.dialog.wikiCommandChecked:
            return self.dialog.getResult()
        else:
            return self._makeWikiCommand(self.dialog.getVarDict(),
                                         self.dialog.templateFileName)

    def _makeWikiCommand(self, vardict, template_name):
        vars_str = u''

        for varname in sorted(vardict.keys()):
            value = vardict[varname]
            if u'"' not in value:
                vars_str += u' {name}="{value}"'.format(name=varname,
                                                        value=vardict[varname])
            else:
                vars_str += u" {name}='{value}'".format(name=varname,
                                                        value=vardict[varname])

        result = u'(:snip file="{template}"{vars}:)(:snipend:)'.format(
            template=template_name,
            vars=vars_str)
        return result

    def _onOk(self, event):
        self.FinishDialog()

    def _onVarChange(self, event):
        self._updateResult()

    def _updateResult(self):
        variables = self.dialog.getVarDict()
        text = self._parser.process(self._selectedText,
                                    self._application.selectedPage,
                                    **variables)
        self.dialog.setResult(text)


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

    @property
    def count(self):
        return len(self._varControls)

    def setFocusToFirstVariable(self):
        if self._varControls:
            self._varControls[0][1].SetFocus()

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
        [*map(lambda item: item[1].Destroy(), self._varControls)]
        self._varControls = []


class StringVariableCtrl(wx.Panel):
    '''
    Control to edit string variable
    '''
    _expandBitmap = wx.Bitmap(os.path.join(getImagesPath(), u'expand.png'))
    _collapseBitmap = wx.Bitmap(os.path.join(getImagesPath(), u'collapse.png'))

    def __init__(self, parent, varname):
        super(StringVariableCtrl, self).__init__(parent)

        self._TEXT_CTRL_SIZER_POSITION = 2

        self._varname = varname
        self._createGUI()

    def SetFocus(self):
        if self._textCtrlExpanded.IsShown():
            self._textCtrlExpanded.SetFocus()
        else:
            self._textCtrlCollapsed.SetFocus()

    def _createGUI(self):
        # Label
        self._label = wx.StaticText(self, label=self._varname)

        # Expanded TextCtrl
        self._textCtrlExpanded = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self._textCtrlExpanded.SetMinSize((-1, 75))
        self._textCtrlExpanded.Bind(wx.EVT_TEXT, handler=self._onTextEdit)
        self._textCtrlExpanded.Hide()

        # Collapsed TextCtrl
        self._textCtrlCollapsed = wx.TextCtrl(self)
        self._textCtrlCollapsed.Bind(wx.EVT_TEXT, handler=self._onTextEdit)
        self._textCtrlCollapsed.Bind(wx.EVT_CHAR_HOOK, handler=self._onChar)

        # Expand / Collapse button
        self._expandButton = wx.BitmapButton(self, bitmap=self._expandBitmap)
        self._expandButton.SetToolTip(_(u'Expand (Shift+Enter)'))
        self._expandButton.Bind(wx.EVT_BUTTON, handler=self._onExpand)

        self._mainSizer = wx.FlexGridSizer(cols=2)
        self._mainSizer.AddGrowableCol(0)

        self._mainSizer.Add(self._label, flag=wx.ALL, border=2)
        self._mainSizer.AddStretchSpacer()

        self._mainSizer.Add(self._textCtrlCollapsed,
                            flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT,
                            border=2)
        self._mainSizer.Add(self._expandButton)

        self.SetSizer(self._mainSizer)
        self.Layout()

    def GetValue(self):
        if self._textCtrlCollapsed.IsShown():
            return self._textCtrlCollapsed.GetValue()
        else:
            return self._textCtrlExpanded.GetValue()

    def SetValue(self, value):
        self._textCtrlCollapsed.SetValue(value)
        self._textCtrlExpanded.SetValue(value)

    def _onChar(self, event):
        if event.GetKeyCode() == wx.WXK_RETURN and event.ShiftDown():
            self._onExpand(None)
            self._textCtrlExpanded.Value = self._textCtrlExpanded.Value + u'\n'
            self._textCtrlExpanded.SetInsertionPointEnd()
        else:
            event.Skip()

    def _onExpand(self, event):
        self._expandButton.Unbind(wx.EVT_BUTTON, handler=self._onExpand)
        self._expandButton.Bind(wx.EVT_BUTTON, handler=self._onCollapse)
        self._expandButton.SetBitmapLabel(self._collapseBitmap)
        self._expandButton.SetToolTip(_(u'Collapse'))

        self._textCtrlCollapsed.Hide()
        self._textCtrlExpanded.Show()

        self._mainSizer.Remove(self._TEXT_CTRL_SIZER_POSITION)
        self._mainSizer.Insert(self._TEXT_CTRL_SIZER_POSITION,
                               self._textCtrlExpanded,
                               flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT,
                               border=2)

        self._textCtrlExpanded.Value = self._textCtrlCollapsed.Value
        self.GetParent().Layout()

        self._textCtrlExpanded.SetFocus()
        self._textCtrlExpanded.SetInsertionPointEnd()

    def _onCollapse(self, event):
        self._expandButton.Bind(wx.EVT_BUTTON, handler=self._onExpand)
        self._expandButton.Unbind(wx.EVT_BUTTON, handler=self._onCollapse)
        self._expandButton.SetBitmapLabel(self._expandBitmap)
        self._expandButton.SetToolTip(_(u'Expand (Shift+Enter)'))

        self._textCtrlExpanded.Hide()
        self._textCtrlCollapsed.Show()

        self._mainSizer.Remove(self._TEXT_CTRL_SIZER_POSITION)
        self._mainSizer.Insert(self._TEXT_CTRL_SIZER_POSITION,
                               self._textCtrlCollapsed,
                               flag=wx.EXPAND | wx.TOP | wx.BOTTOM | wx.LEFT,
                               border=2)

        old_text = self._textCtrlExpanded.GetValue()
        if old_text:
            new_text = old_text.split(u'\n')[0]
            self._textCtrlCollapsed.SetValue(new_text)

        self.GetParent().Layout()
        self._textCtrlCollapsed.SetFocus()
        self._textCtrlCollapsed.SetInsertionPointEnd()

    def _onTextEdit(self, event):
        propagationLevel = 10
        newevent = VarChangeEvent()
        newevent.ResumePropagation(propagationLevel)
        wx.PostEvent(self, newevent)
