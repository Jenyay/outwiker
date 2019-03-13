# -*- coding: utf-8 -*-

import logging
import os.path
import urllib
from pathlib import Path

import wx
import wx.html2

from outwiker.core.htmltemplate import MyTemplate
from outwiker.core.system import getOS
from outwiker.utilites.textfile import readTextFile
from outwiker.gui.mainpanes.mainpane import MainPane

from ..defines import KATEX_DIR_NAME, TOOLS_PANE_NAME
from ..texconfig import TeXConfig

logger = logging.getLogger('TeXEquation')


class ToolsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self._oldEquationHash = ''
        self._template_fname = str(Path(__file__).parents[1].joinpath('data', 'equation.html'))
        self._katexdir = 'file://' + str(Path(__file__).parents[1].joinpath('tools', KATEX_DIR_NAME)).replace('\\', '/')
        self._firstLoad = True

        self.createGUI()

    def createGUI(self):
        self._htmlRender = wx.html2.WebView.New(self)
        self._htmlRender.Disable()

        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(0)

        mainSizer.Add(self._htmlRender, flag=wx.EXPAND)

        self.SetSizer(mainSizer)
        self.Layout()

    def _getEquationHash(self, equation: str, blockMode: bool) -> str:
        return '{}{}'.format(equation, blockMode)

    def setEquation(self, equation: str, blockMode: bool) -> None:
        '''
        Update equation in the preview window if equation was changed
        '''
        equationHash = self._getEquationHash(equation, blockMode)

        if equationHash == self._oldEquationHash:
            return

        self._oldEquationHash = equationHash
        equation = equation.replace('\\', '\\\\')
        equation = equation.replace('"', '\\"')
        html = self._getHTML(equation, blockMode)
        path = "file://" + urllib.parse.quote(os.path.abspath('.').replace('\\', '/')) + "/"
        self._htmlRender.SetPage(html, path)
        if self._firstLoad and getOS().name == 'windows':
            self._htmlRender.Reload()
            self._firstLoad = False

    def _getHTML(self, equation: str, blockMode: bool):
        try:
            template_str = readTextFile(self._template_fname)
        except IOError as e:
            logger.error("Can't read template file: {}".format(self._template_fname))
            logger.error(str(e))
            return

        template = MyTemplate(template_str)
        katexdir = self._katexdir
        blockModeStr = str(blockMode).lower()

        return template.safe_substitute(katexdir=katexdir,
                                        equation=equation,
                                        blockMode=blockModeStr)


class ToolsPane(MainPane):
    def beginRename(self, page=None):
        self.panel.beginRename(page)

    def _createPanel(self):
        return ToolsPanel(self.parent)

    def _createConfig(self):
        return TeXConfig(self.application.config)

    @property
    def caption(self):
        return 'TeXEquation'

    def _createPane(self):
        pane = self._loadPaneInfo(self.config.pane)

        if pane is None:
            pane = wx.aui.AuiPaneInfo().Name(TOOLS_PANE_NAME).Caption(self.caption).Gripper(False).CaptionVisible(True).CloseButton(True).MaximizeButton(False).Float()

        pane.CloseButton()
        pane.Caption(self.caption)

        pane.BestSize((self.config.width.value,
                       self.config.height.value))

        return pane

    def setEquation(self, equation: str, blockMode: bool) -> None:
        self.panel.setEquation(equation, blockMode)
