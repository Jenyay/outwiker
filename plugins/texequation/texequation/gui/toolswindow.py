# -*- coding: utf-8 -*-

import logging
import os.path
import urllib
from pathlib import Path

import wx
import wx.html2

from outwiker.core.htmltemplate import MyTemplate
from outwiker.utilites.textfile import readTextFile

from ..defines import KATEX_DIR_NAME

logger = logging.getLogger('TeXEquation')


class ToolsWindow(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent,
                         style=wx.RESIZE_BORDER | wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT | wx.FRAME_TOOL_WINDOW | wx.CLOSE_BOX)

        self._oldEquation = ''
        self._template_fname = str(Path(__file__).parents[1].joinpath('data', 'equation.html'))
        self._katexdir = 'file://' + str(Path(__file__).parents[1].joinpath('tools', KATEX_DIR_NAME)).replace('\\', '/')

        self.createGUI()
        self.Bind(wx.EVT_CLOSE, handler=self._onClose)

    def createGUI(self):
        self._htmlRender = wx.html2.WebView.New(self)

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)

        mainSizer.Add(self._htmlRender, flag=wx.EXPAND)

        self.SetSizer(mainSizer)
        self.Layout()

    def _onClose(self, event):
        self.Hide()
        event.Veto()

    def setEquation(self, equation: str) -> None:
        '''
        Update equation in the preview window if equation was changed
        '''
        if equation != self._oldEquation:
            pass

        equation = equation.replace('\\', '\\\\')
        html = self._getHTML(equation)
        path = "file://" + urllib.parse.quote(os.path.abspath('.').replace('\\', '/')) + "/"
        self._htmlRender.SetPage(html, path)

    def _getHTML(self, equation):
        try:
            template_str = readTextFile(self._template_fname)
        except IOError as e:
            logger.error("Can't read template file: {}".format(self._template_fname))
            logger.error(str(e))
            return

        template = MyTemplate(template_str)
        katexdir = self._katexdir

        return template.safe_substitute(katexdir=katexdir, equation=equation)
