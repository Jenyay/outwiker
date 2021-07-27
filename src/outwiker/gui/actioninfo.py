# -*- coding=utf-8 -*-

# Python 3.6 (?) does not support defaults parameter
# Old Python version used in a snap package
# from collections import namedtuple


# ActionInfo = namedtuple('ActionInfo',
                        # ['action_type', 'hotkey', 'area', 'hidden'],
                        # defaults=[None, None, False])

# PolyactionInfo = namedtuple('PolyactionInfo',
                            # ['stringId', 'title', 'description', 'hotkey'],
                            # defaults=[None])


class ActionInfo:
    def __init__(self, action_type, hotkey=None, area=None, hidden=None):
        self.action_type = action_type
        self.hotkey = hotkey
        self.area = area
        self.hidden = hidden


class PolyactionInfo:
    def __init__(self, stringId, title, description, hotkey=None):
        self.stringId = stringId
        self.title = title
        self.description = description
        self.hotkey = hotkey
