# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.pages.wiki.fontsizeselector import FontSizeSelector


class WikiFontSizeBaseAction (BaseAction):
    """
    Базовый класс для actions для выбора размера шрифта
    (крупный, мелкий и т.п.)
    """

    def __init__(self, application):
        self._application = application

    def selectFontSize(self, selIndex):
        fontSizeSelector = FontSizeSelector(self._application.mainWindow)
        notation = fontSizeSelector.selectFontSize(selIndex)

        if notation is not None:
            codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
            codeEditor.turnText(notation[0], notation[1])
