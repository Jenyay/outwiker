# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.defines import RECENT_COLORS_COUNT
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.testeddialog import TestedSingleChoiceDialog
from outwiker.core.defines import (STYLES_BLOCK_FOLDER_NAME,
                                   STYLES_INLINE_FOLDER_NAME,
                                   )
from outwiker.core.standardcolors import StandardColors
from outwiker.core.system import getSpecialDirList
from outwiker.utilites.collections import update_recent

from ..wikistyleutils import (turnBlockOrInline,
                              isSelectedBlock,
                              getCustomStylesNames,
                              loadCustomStyles,
                              )
from ..gui.styledialog import StyleDialog


class WikiStyleOnlyAction (BaseAction):
    """
    Mark text with style name
    """
    stringId = u"WikiStyleOnly"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Text style...")

    @property
    def description(self):
        return _(u"Apply style to text")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        editor = self._application.mainWindow.pagePanel.pageView.codeEditor

        styles_folder = (STYLES_BLOCK_FOLDER_NAME if isSelectedBlock(editor)
                         else STYLES_INLINE_FOLDER_NAME)
        dir_list = getSpecialDirList(styles_folder)
        styles = sorted(getCustomStylesNames(dir_list))

        title = _('Select style')
        message = _('Styles')
        mainWindow = self._application.mainWindow

        with TestedSingleChoiceDialog(mainWindow, message, title, styles) as dlg:
            dlg.SetSize((300, 400))

            if dlg.ShowModal() == wx.ID_OK:
                style = dlg.GetStringSelection()
                text_begin = '%{style}%'.format(style=style)
                text_end = '%%'
                turnBlockOrInline(editor, text_begin, text_end)


class WikiStyleAdvancedAction (BaseAction):
    """
    Show dialog for advanced text style settings.
    """
    stringId = u"WikiStyleAdvanced"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Advanced style...")

    @property
    def description(self):
        return _(u"Show dialog for advanced text style settings")

    def _color2str(self, color: wx.Colour) -> str:
        assert color is not None

        color_str = color.GetAsString(wx.C2S_HTML_SYNTAX).lower()
        if color_str in StandardColors:
            color_str = StandardColors[color_str]

        return color_str

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        config = GeneralGuiConfig(self._application.config)
        recent_text_colors = config.recentTextColors.value
        recent_background_colors = config.recentBackgroundColors.value

        editor = self._application.mainWindow.pagePanel.pageView.codeEditor

        if isSelectedBlock(editor):
            styles_folder = STYLES_BLOCK_FOLDER_NAME
            example_html = '''<div class="{css_class}">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi maximus vel tortor a dictum. Sed elit ipsum, consectetur quis dui vitae, pretium dapibus lorem. Duis mattis sagittis magna, suscipit cursus ante sodales sed. Sed id orci in ipsum laoreet maximus.</div>'''
            tag = 'div'
        else:
            styles_folder = STYLES_INLINE_FOLDER_NAME
            example_html = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. <span class="{css_class}">Morbi maximus vel tortor a dictum. Sed elit ipsum, consectetur quis dui vitae, pretium dapibus lorem.</span> Duis mattis sagittis magna, suscipit cursus ante sodales sed. Sed id orci in ipsum laoreet maximus.'''
            tag = 'span'

        dir_list = getSpecialDirList(styles_folder)
        styles = loadCustomStyles(dir_list)

        title = _('Advanced style...')
        mainWindow = self._application.mainWindow

        with StyleDialog(mainWindow, title, styles, example_html, tag) as dlg:
            dlg.setCustomTextColors(recent_text_colors)
            dlg.setCustomBackgroundColors(recent_background_colors)

            if dlg.ShowModal() == wx.ID_OK:
                color = dlg.getTextColor()
                background_color = dlg.getBackgroundColor()
                custom_style_name = dlg.getCustomStyleName()
                custom_css = dlg.getCustomCSS()

                begin = ''
                if custom_style_name:
                    begin += ' {}'.format(custom_style_name)

                if color:
                    color_str = self._color2str(color)
                    if (color_str.startswith('#') or
                            color_str.startswith('rgb(')):
                        begin += ' color="{}"'.format(color_str)
                    else:
                        begin += ' {}'.format(color_str)

                    recent_text_colors = update_recent(
                        recent_text_colors,
                        color.GetAsString(wx.C2S_HTML_SYNTAX).lower(),
                        RECENT_COLORS_COUNT
                    )
                    config.recentTextColors.value = recent_text_colors

                if background_color:
                    background_color_str = self._color2str(background_color)
                    if (background_color_str.startswith('#') or
                            background_color_str.startswith('rgb(')):
                        begin += ' bgcolor="{}"'.format(background_color_str)
                    else:
                        begin += ' bg-{}'.format(background_color_str)

                    recent_background_colors = update_recent(
                        recent_background_colors,
                        background_color.GetAsString(wx.C2S_HTML_SYNTAX).lower(),
                        RECENT_COLORS_COUNT)
                    config.recentBackgroundColors.value = recent_background_colors

                if custom_css:
                    begin += ' style="{}"'.format(custom_css.replace('\n', ' '))

                begin = '%' + begin.strip() + '%'
                end = '%%'
                turnBlockOrInline(editor, begin, end)
