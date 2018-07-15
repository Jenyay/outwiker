# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.defines import (STYLES_BLOCK_FOLDER_NAME,
                                   STYLES_INLINE_FOLDER_NAME,
                                   )
from outwiker.core.system import getSpecialDirList

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
        return _(u"Text style")

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

        with wx.SingleChoiceDialog(mainWindow, message, title, styles) as dlg:
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
        return _(u"Advanced style")

    @property
    def description(self):
        return _(u"Show dialog for advanced text style settings")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        editor = self._application.mainWindow.pagePanel.pageView.codeEditor

        if isSelectedBlock(editor):
            styles_folder = STYLES_BLOCK_FOLDER_NAME
            example_html = '''<div class="{css_class}">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi maximus vel tortor a dictum. Sed elit ipsum, consectetur quis dui vitae, pretium dapibus lorem. Duis mattis sagittis magna, suscipit cursus ante sodales sed. Sed id orci in ipsum laoreet maximus. Sed commodo sem eget lacus porta dictum. Donec gravida laoreet nibh et elementum. Phasellus luctus quam metus, vel faucibus enim iaculis eget. Aenean dui ante, feugiat vitae varius at, ultricies eget est.</div>'''
            tag = 'div'
        else:
            styles_folder = STYLES_INLINE_FOLDER_NAME
            example_html = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. <span class="{css_class}">Morbi maximus vel tortor a dictum. Sed elit ipsum, consectetur quis dui vitae, pretium dapibus lorem.</span> Duis mattis sagittis magna, suscipit cursus ante sodales sed. Sed id orci in ipsum laoreet maximus. Sed commodo sem eget lacus porta dictum. Donec gravida laoreet nibh et elementum. Phasellus luctus quam metus, vel faucibus enim iaculis eget. Aenean dui ante, feugiat vitae varius at, ultricies eget est'''
            tag = 'span'

        dir_list = getSpecialDirList(styles_folder)
        styles = loadCustomStyles(dir_list)

        title = _('Advanced style')
        mainWindow = self._application.mainWindow

        with StyleDialog(mainWindow, title, styles, example_html, tag) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                pass
        #
        # with wx.SingleChoiceDialog(mainWindow, message, title, styles) as dlg:
        #     dlg.SetSize((300, 400))
        #     if dlg.ShowModal() == wx.ID_OK:
        #         style = dlg.GetStringSelection()
        #         text_begin = '%{style}%'.format(style=style)
        #         text_end = '%%'
        #         turnBlockOrInline(editor, text_begin, text_end)
