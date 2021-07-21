# -*- coding=utf-8 -*-

from collections import namedtuple


ActionInfo = namedtuple('ActionInfo',
                        ['action_type', 'hotkey', 'area', 'hidden'],
                        defaults=[None, None, False])

PolyactionInfo = namedtuple('PolyactionInfo',
                            ['stringId', 'title', 'description', 'hotkey'],
                            defaults=[None])
