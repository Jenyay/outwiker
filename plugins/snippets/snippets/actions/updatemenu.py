# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction

from snippets.i18n import get_


EVENT_UPDATE_MENU = u'Snippets_UpdateMenu'


class UpdateMenuAction (BaseAction):
    stringId = u"snippets_update_menu"

    def __init__(self, application):
        super(UpdateMenuAction, self).__init__()
        self._application = application
        global _
        _ = get_()

    def run(self, params):
        self._application.customEvents(EVENT_UPDATE_MENU, None)

    @property
    def title(self):
        return _(u"Update snippets list")

    @property
    def description(self):
        return _(u'Snippets. Reload snippets list and update the menu.')
