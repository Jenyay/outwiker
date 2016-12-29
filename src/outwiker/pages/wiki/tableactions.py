# -*- coding: UTF-8 -*-

import re

import wx

from outwiker.gui.tabledialog import TableDialog
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.pages.wiki.utils import getCommandsByPos
from outwiker.pages.wiki.tabledialogcontroller import (
    TableDialogController,
    TableRowsDialogController
)


def getTableByPos(text, position):
    """
    Return suffix for command name for most nested (:tableNN:) command in the position
    """
    regex = re.compile(r'table(?P<suffix>\d*)$', re.UNICODE)
    matches = getCommandsByPos(text, position)
    matches.reverse()

    for match in matches:
        name = match.groupdict()['name']
        tableMatch = regex.match(name)
        if tableMatch:
            return tableMatch.groupdict()['suffix']

    return None


def getInsertTableActionFunc (application, parent, pageView):
    def func (param):
        editor = pageView.codeEditor
        tableSuffix = getTableByPos (editor.GetText(),
                                     editor.GetCurrentPosition())
        if tableSuffix is None:
            suffix = u''
        elif tableSuffix == u'':
            suffix = u'2'
        else:
            try:
                suffix = unicode(int(tableSuffix) + 1)
            except ValueError:
                suffix = u''

        with TableDialog(parent) as dlg:
            controller = TableDialogController(dlg, suffix, application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText(result)

    return func


def getInsertTableRowsActionFunc (application, parent, pageView):
    def func (param):
        editor = pageView.codeEditor
        tableSuffix = getTableByPos (editor.GetText(),
                                     editor.GetCurrentPosition())
        if tableSuffix is None:
            suffix = u''
        else:
            try:
                suffix = unicode(int(tableSuffix))
            except ValueError:
                suffix = u''

        with TableRowsDialog (parent) as dlg:
            controller = TableRowsDialogController (dlg, suffix, application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText(result)

    return func


def getInsertTableCellActionFunc (application, parent, pageView):
    def func (param):
        editor = pageView.codeEditor
        tableSuffix = getTableByPos (editor.GetText(),
                                     editor.GetCurrentPosition())
        if tableSuffix is None:
            suffix = u''
        else:
            try:
                suffix = unicode(int(tableSuffix))
            except ValueError:
                suffix = u''

        text = u'(:cell{}:)'.format(suffix)
        editor.replaceText(text)

    return func
