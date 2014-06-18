# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly


class SetStyleToBranchAction (BaseAction):
    """
    Применить стиль ко всем страницам ветки
    """
    stringId = u"SetStyleToBranch"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Set Style to Branch…")


    @property
    def description (self):
        return _(u"Set Style to Branch")


    def run (self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return

        if self._application.selectedPage is None:
            self.addStyleToBranchGui (self._application.wikiroot,
                                      self._application.mainWindow)
        else:
            self.addStyleToBranchGui (self._application.selectedPage,
                                      self._application.mainWindow)


    @testreadonly
    def addStyleToBranchGui (self, page, parent):
        """
        Установить стиль для всей ветки, в том числе и для текущей страницы
        """
        print "Run!"
        # dlg = TagsDialog (parent, self._application)
        #
        # if dlg.ShowModal() == wx.ID_OK:
        #     self._application.onStartTreeUpdate(page.root)
        #
        #     try:
        #         tagBranch (page, dlg.tags)
        #     finally:
        #         self._application.onEndTreeUpdate(page.root)
        #
        # dlg.Destroy()
