# -*- coding: utf-8 -*-

import wx.aui

from outwiker.utilites.text import positionInside

from .gui.toolswindow import ToolsPane
from .i18n import get_
from .tokentex import InlineTexToken
from .defines import TOOLS_PANE_NAME


class ToolsWindowController(object):
    def __init__(self, application):
        self._application = application
        self._toolsPane = None
        self._prevPositionInsideEquation = False
        self._auiManager = self._application.mainWindow.auiManager

    def initialize(self):
        global _
        _ = get_()

        self._application.onTextEditorCaretMove += self.__onTextEditorCaretMove
        self._auiManager.Bind(wx.aui.EVT_AUI_PANE_CLOSE,
                              handler=self._onPaneClose)

    def destroy(self):
        self._auiManager.Unbind(wx.aui.EVT_AUI_PANE_CLOSE,
                                handler=self._onPaneClose)
        self._application.onTextEditorCaretMove -= self.__onTextEditorCaretMove
        self._destroyToolsWindow()

    def _destroyToolsWindow(self):
        self._hideToolsWindow()
        if self._toolsPane is not None:
            self._toolsPane.close()
            self._toolsPane = None

    def __onTextEditorCaretMove(self,
                                page: 'outwiker.core.tree.WikiPage',
                                params: 'outwiker.core.events.TextEditorCaretMoveParams') -> None:
        if params.startSelection != params.endSelection:
            return

        editor = params.editor
        position = params.startSelection
        text = editor.GetText()
        insideEquation = positionInside(text, position, '{$', '$}')

        if insideEquation:
            # May be the window was closed by user
            if not self._prevPositionInsideEquation:
                self._showToolsWindow()

            self._updateEquation(text, position)
        else:
            self._hideToolsWindow()

        self._prevPositionInsideEquation = insideEquation

    def _showToolsWindow(self):
        '''
        Show tools window (with equation preview). The window will be created
        if _toolsPane is None.
        '''
        if self._toolsPane is None:
            self._toolsPane = ToolsPane(
                self._application.mainWindow,
                self._application.mainWindow.auiManager,
                self._application)
            self._application.mainWindow.UpdateAuiManager()

        if not self._toolsPane.isShown():
            self._toolsPane.show()
            self._application.mainWindow.UpdateAuiManager()

    def _hideToolsWindow(self):
        if self._toolsPane is not None:
            self._toolsPane.hide()
            self._application.mainWindow.UpdateAuiManager()

    def _updateEquation(self, text, position):
        equation = self.extractEquation(text, position)
        assert self._toolsPane is not None

        self._toolsPane.setEquation(equation)
        self._application.mainWindow.Raise()

    @staticmethod
    def extractEquation(text: str, position: int):
        left_token = InlineTexToken.texStart
        right_token = InlineTexToken.texEnd
        left_pos = text.rfind(left_token, 0, position)
        right_pos = text.find(right_token, position)

        if left_pos == -1 or right_pos == -1:
            return ''

        equation = text[left_pos + len(left_token): right_pos]
        if equation.startswith('$') and equation.endswith('$'):
            equation = equation[1:-1]

        return equation

    def _onPaneClose(self, event):
        paneName = event.GetPane().name
        if paneName == TOOLS_PANE_NAME:
            self._toolsPane.saveParams()

        event.Skip()
