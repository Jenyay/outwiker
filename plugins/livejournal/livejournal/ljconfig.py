# -*- coding: utf-8 -*-

from outwiker.api.core.config import ListOption


class LJConfig:
    SECTION = "Livejournal"
    USERS_PARAM = "users"
    COMMUNITY_PARAM = "communities"

    def __init__(self, config):
        self.users = ListOption(config, LJConfig.SECTION, LJConfig.USERS_PARAM, [])

        self.communities = ListOption(
            config, LJConfig.SECTION, LJConfig.COMMUNITY_PARAM, []
        )
