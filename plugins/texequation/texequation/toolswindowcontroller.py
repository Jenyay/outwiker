# -*- coding: utf-8 -*-


from outwiker.utilites.text import positionInside

from .gui.toolswindow import ToolsWindow
from .i18n import get_
from .tokentex import InlineTexToken


class ToolsWindowController(object):
    def __init__(self, application):
        self._application = application
        self._toolsWindow = None
        self._prevPositionInsideEquation = False

    def initialize(self):
        global _
        _ = get_()

        self._application.onTextEditorCaretMove += self.__onTextEditorCaretMove

    def destroy(self):
        self._application.onTextEditorCaretMove -= self.__onTextEditorCaretMove
        self._destroyToolsWindow()

    def _destroyToolsWindow(self):
        self._hideToolsWindow()
        if self._toolsWindow is not None:
            self._toolsWindow.Destroy()
            self._toolsWindow = None

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
        if _toolsWindow is None.
        '''
        if self._toolsWindow is None:
            self._toolsWindow = ToolsWindow(self._application.mainWindow)

        if not self._toolsWindow.IsShown():
            self._toolsWindow.Show()

    def _hideToolsWindow(self):
        if self._toolsWindow is not None:
            self._toolsWindow.Hide()

    def _updateEquation(self, text, position):
        equation = self.extractEquation(text, position)
        assert self._toolsWindow is not None

        self._toolsWindow.setEquation(equation)

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
