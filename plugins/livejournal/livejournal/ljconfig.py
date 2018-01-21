# -*- coding: utf-8 -*-

from outwiker.core.config import ListOption


class LJConfig (object):
    SECTION = u"Livejournal"
    USERS_PARAM = u"users"
    COMMUNITY_PARAM = u"communities"

    def __init__(self, config):
        self.users = ListOption(
            config,
            LJConfig.SECTION,
            LJConfig.USERS_PARAM,
            []
        )

        self.communities = ListOption(
            config,
            LJConfig.SECTION,
            LJConfig.COMMUNITY_PARAM,
            []
        )
