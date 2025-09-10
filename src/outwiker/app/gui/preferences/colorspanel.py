# -*- coding: utf-8 -*-

from typing import Dict, Optional, List
import wx

from outwiker.core.application import Application
from outwiker.core.config import StringOption
from outwiker.gui.controls.colorcombobox import ColorComboBox
from outwiker.gui.guiconfig import EditorConfig, MainWindowConfig, GeneralGuiConfig, TabsConfig
from outwiker.gui.preferences.prefpanel import BasePrefPanel


class ColorElement:
    def __init__(self, title: str, config_param: StringOption) -> None:
        self._title = title
        self._config_param = config_param
        self._ctrl: Optional[ColorComboBox] = None

    @property
    def title(self) -> str:
        return self._title

    @property
    def config_param(self) -> StringOption:
        return self._config_param

    @property
    def ctrl(self) -> Optional[ColorComboBox]:
        return self._ctrl

    @ctrl.setter
    def ctrl(self, value: Optional[ColorComboBox]) -> None:
        self._ctrl = value


class ColorsPanel(BasePrefPanel):
    def __init__(self, parent, application: Application):
        super().__init__(parent)
        self._mainWindowConfig = MainWindowConfig(application.config)
        self._editorGuiConfig = EditorConfig(application.config)
        self._generalGuiConfig = GeneralGuiConfig(application.config)
        self._tabsConfig = TabsConfig(application.config)

        self._color_sections: Dict[str, List[ColorElement]] = {
            _("Main window"): [
                ColorElement(
                    _("Main panels background color"),
                    self._mainWindowConfig.mainPanesBackgroundColor,
                ),
                ColorElement(
                    _("Main panels text color"),
                    self._mainWindowConfig.mainPanesTextColor,
                ),
            ],

            _("Editor"): [
                ColorElement(_("Font color"), self._editorGuiConfig.fontColor),
                ColorElement(_("Background color"), self._editorGuiConfig.backColor),
                ColorElement(_("Background color of the selected text"), self._editorGuiConfig.selBackColor),
                ColorElement(_("Page margin background color"), self._editorGuiConfig.marginBackColor),
                ],

            _("Tabs"): [
                ColorElement(_("Tab color"), self._tabsConfig.backColorNormal),
                ColorElement(_("Сolor of the selected tab"), self._tabsConfig.backColorSelected),
                ColorElement(_("Сolor of the tab under cursor"), self._tabsConfig.backColorHover),
                ColorElement(_("Color of the pressed tab"), self._tabsConfig.backColorDowned),
                ColorElement(_("Color of the dragged tab"), self._tabsConfig.backColorDragged),
                ColorElement(_("Tab border color"), self._tabsConfig.borderColor),
                ]
        }

        self._recentGuiColors = [
            wx.Colour(color_txt)
            for color_txt in self._generalGuiConfig.recentGuiColors.value
            if wx.Colour(color_txt).IsOk()
        ]

        self._createGUI()

        self.LoadState()
        self.SetupScrolling()

    def _createGUI(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)

        self._createSections(main_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def _createSections(self, main_sizer):
        for section_title, items in self._color_sections.items():
            sizer = self._createSection(main_sizer, section_title)[1]
            for color_element in items:
                ctrl = self._createLabelAndColorComboBox(color_element.title, sizer)[1]
                ctrl.AddColors(self._recentGuiColors)
                color_element.ctrl = ctrl

    def LoadState(self):
        for items in self._color_sections.values():
            for color_element in items:
                color_element.ctrl.SetSelectedColor(
                    wx.Colour(color_element.config_param.value)
                )

    def Save(self):
        for items in self._color_sections.values():
            for color_element in items:
                color = color_element.ctrl.GetSelectedColor()
                if color is not None:
                    color_element.config_param.value = color.GetAsString(
                        wx.C2S_HTML_SYNTAX
                    )
                else:
                    color_element.config_param.value = None
