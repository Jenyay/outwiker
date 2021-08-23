# -*- coding=utf-8 -*-


class ActionInfo:
    def __init__(self, action_type, hotkey=None, area=None, hidden=False):
        self.action_type = action_type
        self.hotkey = hotkey
        self.area = area
        self.hidden = hidden

    def __str__(self):
        return '{} (hotkey: {}, area: {}, hidden: {})'.format(self.action_type.stringId,
                                                              str(self.hotkey),
                                                              self.area,
                                                              self.hidden)


class PolyactionInfo:
    def __init__(self, stringId, title, description, hotkey=None,
                 area=None, hidden=False):
        """
        area used for duplicate test only.
        hidden is not used now
        """
        self.stringId = stringId
        self.title = title
        self.description = description
        self.hotkey = hotkey
        self.area = area
        self.hidden = hidden

    def __str__(self):
        return '{} (hotkey: {}, area: {}, hidden: {})'.format(self.stringId,
                                                              str(self.hotkey),
                                                              self.area,
                                                              self.hidden)
