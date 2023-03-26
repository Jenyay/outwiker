# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.dialogs.messagebox import MessageBox

from .exportdialog import ExportDialog


class ExportPageDialog(ExportDialog):
    """
    Класс диалога для экспорта одной страницы
    """

    def __init__(self, parent, exporter, config):
        super().__init__(parent, config)
        self.__exporter = exporter

        from .i18n import _

        global _

    def _onOk(self):
        self._config.imagesOnly = self.imagesOnly
        self._config.overwrite = self.overwrite

        try:
            self.__exporter.export(
                self.path, self.__exporter.page.title, self.imagesOnly, self.overwrite
            )

        except BaseException as error:
            MessageBox(str(error), _("Error"), wx.OK | wx.ICON_ERROR)
            return

        self.EndModal(wx.ID_OK)
