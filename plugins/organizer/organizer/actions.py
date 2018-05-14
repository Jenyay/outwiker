# -*- coding: utf-8 -*-

from datetime import datetime

from outwiker.gui.baseaction import BaseAction

from .config import OrganizerConfig
from .i18n import get_


class OrgAction (BaseAction):
    """
    Описание действия
    """

    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"Organizer_org"

    @property
    def title(self):
        return _(u"Insert (:org:) command")

    @property
    def description(self):
        return _(u"Description")

    def run(self, params):
        dateFormat = OrganizerConfig(
            self._application.config).dateTimeFormat.value

        leftText = u'(:org date="{date}":)\n'.format(
            date=datetime.now().strftime(dateFormat))
        rightText = u'\n(:orgend:)'

        self._getEditor().turnText(leftText, rightText)

    def _getEditor(self):
        return self._application.mainWindow.pagePanel.pageView.codeEditor
