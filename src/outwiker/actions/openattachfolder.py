#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import MessageBox
from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS


class OpenAttachFolderAction (BaseAction):
    """
    Открыть папку с прикрепленными файлами в системном файловом менеджере
    """
    stringId = u"OpenAttachFolder"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Open Attachments Folder")


    @property
    def description (self):
        return _(u"Open folder with attached files")


    def run (self, params):
        if self._application.selectedPage != None:
            folder = Attachment (self._application.selectedPage).getAttachPath (create=True)
            try:
                getOS().startFile (folder)
            except OSError:
                text = _(u"Can't open folder '{}'".format (folder))
                MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)
