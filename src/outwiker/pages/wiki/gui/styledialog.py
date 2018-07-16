# -*- coding: utf-8 -*-

from typing import Mapping, Optional

import wx

from outwiker.core.system import getOS
from outwiker.gui.testeddialog import TestedDialog
from .csseditor import CSSEditor


class StyleDialog(TestedDialog):
    def __init__(self,
                 parent: wx.Window,
                 title: str,
                 styles: Mapping[str, str],
                 example_html: str,
                 tag: str):
        '''
        styles - dictionary. Key - style name, value - CSS content.
        '''
        super().__init__(parent,
                         title=title,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.NONE_STYLE = _('None')
        self.CSS_STYLE_NAME = '__outwiker_preview'
        self._styles = styles
        self._example_html = example_html
        self._tag = tag
        self._template = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv='X-UA-Compatible' content='IE=edge' />
    <meta http-equiv='content-type' content='text/html; charset=utf-8'/>
    <style>
    {css}
    </style>
</head>
<body>
{example}
</body>
'''

        self.SetSize((500, 600))
        self.Center()
        self._create_gui()

        self._style_name_combo.Bind(wx.EVT_COMBOBOX,
                                    handler=self._onUpdate)
        self._text_color_check.Bind(wx.EVT_CHECKBOX,
                                    handler=self._onUpdate)
        self._text_color_picker.Bind(wx.EVT_COLOURPICKER_CHANGED,
                                     handler=self._onTextColorPicker)
        self._text_background_check.Bind(wx.EVT_CHECKBOX,
                                         handler=self._onUpdate)
        self._text_background_picker.Bind(wx.EVT_COLOURPICKER_CHANGED,
                                          handler=self._onTextBackgroundPicker)
        self._custom_CSS_check.Bind(wx.EVT_CHECKBOX,
                                    handler=self._onUpdate)
        self._custom_CSS_editor.Bind(wx.stc.EVT_STC_CHANGE,
                                     handler=self._onEditCSS)
        self.updateExample()

    def updateExample(self):
        html = self.getHTML()
        self._browser.SetPage(html, '.')

    def _onUpdate(self, event):
        self.updateExample()

    def _onTextColorPicker(self, event):
        self.enableTextColor(True)
        self._onUpdate(event)

    def _onTextBackgroundPicker(self, event):
        self.enableBackgroundColor(True)
        self._onUpdate(event)

    def _onEditCSS(self, event):
        self.enableCustomCSS(True)
        self._onUpdate(event)

    def getHTML(self):
        result = ''

        # Classes for styles
        css_class = self.CSS_STYLE_NAME

        custom_style_name = self.getCustomStyleName()
        if custom_style_name:
            result += self._styles[custom_style_name] + '\n'
            css_class = custom_style_name + ' ' + css_class

        result += '{tag}.{class_name} {{\n'.format(
            tag=self._tag,
            class_name=self.CSS_STYLE_NAME
        )

        # Text color
        text_color = self.getTextColor()
        if text_color:
            result += 'color: {};\n'.format(text_color.GetAsString(wx.C2S_HTML_SYNTAX))

        # Background color
        background_color = self.getBackgroundColor()
        if background_color:
            result += 'background-color: {};\n'.format(background_color.GetAsString(wx.C2S_HTML_SYNTAX))

        # Custom CSS
        custom_css = self.getCustomCSS()
        if custom_css:
            result += custom_css.strip() + '\n'

        result += '}'

        example = self._example_html.format(css_class=css_class)
        html = self._template.format(css=result, example=example)

        return html

    def _create_gui(self):
        paramsPreviewSizer = wx.FlexGridSizer(cols=1)
        paramsPreviewSizer.AddGrowableRow(0, 1)
        paramsPreviewSizer.AddGrowableRow(1, 2)
        paramsPreviewSizer.AddGrowableCol(0)

        paramsSizer = wx.FlexGridSizer(cols=1)
        paramsSizer.AddGrowableCol(0)
        paramsSizer.AddGrowableRow(4)

        # Style name
        style_names = sorted(self._styles.keys())
        style_names.insert(0, self.NONE_STYLE)

        style_name_label = wx.StaticText(self, label='Style name')

        self._style_name_combo = wx.ComboBox(self, choices=style_names)
        self._style_name_combo.SetSelection(0)

        style_name_sizer = wx.FlexGridSizer(cols=2)
        style_name_sizer.AddGrowableCol(1)
        style_name_sizer.Add(style_name_label,
                             flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL,
                             border=4)

        style_name_sizer.Add(self._style_name_combo,
                             flag=wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL,
                             border=4)

        paramsSizer.Add(style_name_sizer, flag=wx.EXPAND)

        # Text color
        self._text_color_check = wx.CheckBox(self, label=_('Text color'))
        self._text_color_picker = wx.ColourPickerCtrl(self)

        text_color_sizer = wx.FlexGridSizer(cols=2)
        text_color_sizer.AddGrowableCol(1)
        text_color_sizer.Add(self._text_color_check,
                             flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
                             border=4)

        text_color_sizer.Add(self._text_color_picker,
                             flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL,
                             border=4)

        paramsSizer.Add(text_color_sizer, flag=wx.EXPAND)

        # Text background
        self._text_background_check = wx.CheckBox(self, label=_('Text background'))
        self._text_background_picker = wx.ColourPickerCtrl(self,
                                                           colour=wx.WHITE)

        text_background_sizer = wx.FlexGridSizer(cols=2)
        text_background_sizer.AddGrowableCol(1)
        text_background_sizer.Add(self._text_background_check,
                                  flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT,
                                  border=4)

        text_background_sizer.Add(self._text_background_picker,
                                  flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL,
                                  border=4)

        paramsSizer.Add(text_background_sizer, flag=wx.EXPAND)

        # Custom CSS
        self._custom_CSS_check = wx.CheckBox(self, label=_('Custom CSS'))
        self._custom_CSS_editor = CSSEditor(self)
        self._custom_CSS_editor.SetMinSize((-1, 100))

        paramsSizer.Add(self._custom_CSS_check, flag=wx.ALIGN_CENTER_VERTICAL)
        paramsSizer.Add(self._custom_CSS_editor,
                        flag=wx.EXPAND | wx.LEFT,
                        border=16)

        paramsPreviewSizer.Add(paramsSizer,
                               flag=wx.EXPAND | wx.ALL,
                               border=4)

        # HTML browser
        self._browser = getOS().getHtmlRender(self)
        paramsPreviewSizer.Add(self._browser,
                               flag=wx.EXPAND | wx.ALL,
                               border=4)

        # Ok / Cancel buttons
        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        paramsPreviewSizer.Add(okCancel,
                               flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
                               border=4)

        self.SetSizer(paramsPreviewSizer)

    def getTextColor(self) -> Optional[wx.Colour]:
        '''
        Return selected text color if set appropriate check box
            or None otherwise.
        '''
        return (self._text_color_picker.GetColour()
                if self._text_color_check.IsChecked()
                else None)

    def setTextColor(self, color: wx.Colour) -> None:
        self.enableTextColor(True)
        self._text_color_picker.SetColour(color)

    def enableTextColor(self, enabled: bool) -> None:
        self._text_color_check.SetValue(enabled)

    def getBackgroundColor(self) -> Optional[wx.Colour]:
        '''
        Return selected text background color if set appropriate check box
            or None otherwise.
        '''
        return (self._text_background_picker.GetColour()
                if self._text_background_check.IsChecked()
                else None)

    def setBackgroundColor(self, color: wx.Colour) -> None:
        self.enableBackgroundColor(True)
        self._text_background_picker.SetColour(color)

    def enableBackgroundColor(self, enabled: bool) -> None:
        self._text_background_check.SetValue(enabled)

    def getCustomStyleName(self) -> Optional[str]:
        '''
        Return selected custom style name or None.
        '''
        return (self._style_name_combo.GetStringSelection()
                if self._style_name_combo.GetSelection() > 0
                else None)

    def setCustomStyleName(self, style_name: str) -> None:
        if style_name in self._styles:
            for n, string in enumerate(self._style_name_combo.GetItems()):
                if string == style_name:
                    self._style_name_combo.SetSelection(n)

    def disableCustomStyleName(self) -> None:
        self._style_name_combo.SetSelection(0)

    def getCustomCSS(self) -> Optional[str]:
        '''
        Return custom CSS if set appropriate check box or None otherwise.
        '''
        return (self._custom_CSS_editor.GetText().strip()
                if self._custom_CSS_check.IsChecked()
                else None)

    def setCustomCSS(self, css: str) -> None:
        self.enableCustomCSS(True)
        self._custom_CSS_editor.SetText(css)

    def enableCustomCSS(self, enabled: bool) -> None:
        self._custom_CSS_check.SetValue(enabled)
