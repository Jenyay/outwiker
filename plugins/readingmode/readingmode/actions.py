# -*- coding: utf-8 -*-

from outwiker.api.gui.actions import (
    BaseAction,
    ShowHideTreeAction,
    ShowHideTagsAction,
    ShowHideAttachesAction,
)

from .i18n import get_


class ReadingModeAction(BaseAction):
    """
    Перейти в Вид для чтения и обратно
    """

    stringId = "ReadingMode_Switch"

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    @property
    def title(self):
        return _("Reading Mode")

    @property
    def description(self):
        return _(
            """Reading Mode disables the panel "Tree", "Tag", "Attach Files" without changing the geometry of the main window."""
        )

    def run(self, params):
        if params:
            self._application.actionController.check(ShowHideTreeAction.stringId, False)
            self._application.actionController.check(ShowHideTagsAction.stringId, False)
            self._application.actionController.check(
                ShowHideAttachesAction.stringId, False
            )
        else:
            self._application.actionController.check(ShowHideTreeAction.stringId, True)
            self._application.actionController.check(ShowHideTagsAction.stringId, True)
            self._application.actionController.check(
                ShowHideAttachesAction.stringId, True
            )
