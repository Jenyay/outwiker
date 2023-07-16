# -*- coding: utf-8 -*-


from outwiker.api.gui.actions import BaseAction


class DebugAction(BaseAction):
    """
    Класс действия, предназначенный для отладки действий
    с помощью плагина TestDebug
    """

    stringId = "plugin_debug_action"

    def __init__(self, application):
        super().__init__()
        self._application = application

    @property
    def title(self):
        return "DebugAction"

    @property
    def description(self):
        return "DebugAction"

    def run(self, params):
        print("DebugAction.run({0})".format(params))
